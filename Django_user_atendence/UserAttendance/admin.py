from time import timezone

from django.contrib import admin
from django.db import transaction
from django.utils import timezone 

from .models import (
    Vendor,
    UserProfile,
    UserAttendance,
    LeaveBalance,
    LoginLogoutLog,
    LeaveApplication,
    ResignationApplication,
)


# =========================================================
# Vendor
# =========================================================

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
    )

    search_fields = (
        "name",
    )


# =========================================================
# User Profile
# =========================================================

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    list_display = (
        "employee_id",
        "employee_name",
        "user",
        "mobile",
        "department",
        "designation",
        "vendor",
        "status",
    )

    list_filter = (
        "department",
        "designation",
        "vendor",
        "status",
    )

    search_fields = (
        "employee_id",
        "employee_name",
        "user__username",
        "mobile",
    )

    ordering = (
        "employee_id",
    )


# =========================================================
# User Attendance
# =========================================================

@admin.register(UserAttendance)
class UserAttendanceAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "date",
        "time",
        "out_at",
        "status",
        "latitude",
        "longitude",
        "out_latitude",
        "out_longitude",
        "out_location",
        "blink_verified",
        "confidence",
        "created_at",
    )

    list_filter = (
        "status",
        "date",
        "blink_verified",
    )

    search_fields = (
        "user__username",
        "location",
        "out_location",
    )

    readonly_fields = (
        "date",
        "time",
        "created_at",
    )

# =========================================================
# Leave Balance
# =========================================================

@admin.register(LeaveBalance)
class LeaveBalanceAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "cl",
        "el",
        "sl",
        "total_leave",
    )

    search_fields = (
        "user__username",
    )


# =========================================================
# Login / Logout Log
# =========================================================

@admin.register(LoginLogoutLog)
class LoginLogoutLogAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "action",
        "timestamp",
        "ip_address",
    )

    list_filter = (
        "action",
        "timestamp",
    )

    search_fields = (
        "user__username",
        "ip_address",
    )

    readonly_fields = (
        "user",
        "action",
        "timestamp",
        "ip_address",
        "user_agent",
    )

    ordering = (
        "-timestamp",
    )


# =========================================================
# Leave Application
# =========================================================


@admin.register(LeaveApplication)
class LeaveApplicationAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "leave_type",
        "start_date",
        "end_date",
        "days",
        "status",
        "applied_at",
        "approved_at",
    )

    list_filter = (
        "leave_type",
        "status",
        "start_date",
    )

    search_fields = (
        "user__username",
        "user__first_name",
        "reason",
    )

    readonly_fields = (
        "user",
        "applied_at",
        "approved_at",
    )

    ordering = (
        "-applied_at",
    )

    @transaction.atomic
    def save_model(self, request, obj, form, change):

        # ==========================================
        # NEW APPLICATION
        # ==========================================

        if not change:

            # New application normally starts as Pending
            if obj.status == "Approved":

                balance = LeaveBalance.objects.select_for_update().get(
                    user=obj.user
                )

                # ------------------------------
                # CL
                # ------------------------------

                if obj.leave_type == "CL":

                    if balance.cl < obj.days:
                        raise ValueError(
                            "Not enough CL balance."
                        )

                    balance.cl -= obj.days

                # ------------------------------
                # EL
                # ------------------------------

                elif obj.leave_type == "EL":

                    if balance.el < obj.days:
                        raise ValueError(
                            "Not enough EL balance."
                        )

                    balance.el -= obj.days

                # ------------------------------
                # SL
                # ------------------------------

                elif obj.leave_type == "SL":

                    if balance.sl < obj.days:
                        raise ValueError(
                            "Not enough SL balance."
                        )

                    balance.sl -= obj.days

                # Recalculate total

                balance.total_leave = (
                    balance.cl +
                    balance.el +
                    balance.sl
                )

                balance.save()

                obj.approved_at = timezone.now()

        # ==========================================
        # EXISTING APPLICATION
        # ==========================================

        else:

            old_obj = LeaveApplication.objects.get(
                pk=obj.pk
            )

            # --------------------------------------
            # PENDING -> APPROVED
            # --------------------------------------

            if (
                old_obj.status != "Approved"
                and obj.status == "Approved"
            ):

                balance = LeaveBalance.objects.select_for_update().get(
                    user=obj.user
                )

                # CL

                if obj.leave_type == "CL":

                    if balance.cl < obj.days:
                        raise ValueError(
                            "Not enough CL balance."
                        )

                    balance.cl -= obj.days

                # EL

                elif obj.leave_type == "EL":

                    if balance.el < obj.days:
                        raise ValueError(
                            "Not enough EL balance."
                        )

                    balance.el -= obj.days

                # SL

                elif obj.leave_type == "SL":

                    if balance.sl < obj.days:
                        raise ValueError(
                            "Not enough SL balance."
                        )

                    balance.sl -= obj.days

                balance.total_leave = (
                    balance.cl +
                    balance.el +
                    balance.sl
                )

                balance.save()

                obj.approved_at = timezone.now()

            # --------------------------------------
            # APPROVED -> REJECTED
            # --------------------------------------

            elif (
                old_obj.status == "Approved"
                and obj.status in ["Rejected", "Cancelled"]
            ):

                balance = LeaveBalance.objects.select_for_update().get(
                    user=obj.user
                )

                # Return the previously deducted leave

                if old_obj.leave_type == "CL":

                    balance.cl += old_obj.days

                elif old_obj.leave_type == "EL":

                    balance.el += old_obj.days

                elif old_obj.leave_type == "SL":

                    balance.sl += old_obj.days

                balance.total_leave = (
                    balance.cl +
                    balance.el +
                    balance.sl
                )

                balance.save()

                obj.approved_at = None

        # ==========================================
        # SAVE APPLICATION
        # ==========================================

        super().save_model(
            request,
            obj,
            form,
            change
        )

# =========================================================
# Resignation Application
# =========================================================

@admin.register(ResignationApplication)
class ResignationApplicationAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "resignation_date",
        "status",
        "applied_at",
    )

    list_filter = (
        "status",
    )

    actions = [
        "accept_resignation",
        "reject_resignation",
    ]

    @admin.action(description="Accept selected resignation")
    def accept_resignation(self, request, queryset):

        queryset.filter(
            status="Pending"
        ).update(status="Accepted")

    @admin.action(description="Reject selected resignation")
    def reject_resignation(self, request, queryset):

        queryset.filter(
            status="Pending"
        ).update(status="Rejected")