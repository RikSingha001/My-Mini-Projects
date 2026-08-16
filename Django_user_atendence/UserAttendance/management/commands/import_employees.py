import pandas as pd

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from UserAttendance.models import (
    Vendor,
    UserProfile,
    LeaveBalance
)


class Command(BaseCommand):

    help = "Import employee data from Excel into SQLite"

    def add_arguments(self, parser):

        parser.add_argument(
            "file_path",
            type=str
        )

    def handle(self, *args, **options):

        file_path = options["file_path"]

        # Read Excel
        df = pd.read_excel(
            file_path,
            sheet_name="Employee_Master_Data",
            header=3
        )

        # Rename columns
        df.columns = [
            "sl",
            "employee_id",
            "username",
            "password",
            "mobile",
            "dob",
            "employee_name",
            "department",
            "designation",
            "cl",
            "el",
            "sl_leave",
            "total_leave",
            "status"
        ]

        # Vendor
        vendor, created = Vendor.objects.get_or_create(
            name="Default Vendor"
        )

        for _, row in df.iterrows():

            username = str(row["username"]).strip()
            employee_id = str(row["employee_id"]).strip()

            if not username or not employee_id:
                continue

            # --------------------------------
            # Create Django User
            # --------------------------------

            user, created = User.objects.get_or_create(
                username=username
            )

            if created:

                password = str(row["password"]).strip()

                user.set_password(password)

                user.first_name = str(
                    row["employee_name"]
                )

                user.save()

            # --------------------------------
            # Date of Birth
            # --------------------------------

            dob = pd.to_datetime(
                row["dob"],
                dayfirst=True,
                errors="coerce"
            )

            if pd.isna(dob):
                dob = None
            else:
                dob = dob.date()

            # --------------------------------
            # User Profile
            # --------------------------------

            profile, _ = UserProfile.objects.update_or_create(

                user=user,

                defaults={
                    "employee_id": employee_id,
                    "employee_name": str(
                        row["employee_name"]
                    ),
                    "mobile": str(
                        row["mobile"]
                    ),
                    "date_of_birth": dob,
                    "department": str(
                        row["department"]
                    ),
                    "designation": str(
                        row["designation"]
                    ),
                    "vendor": vendor,
                    "status": str(
                        row["status"]
                    ),
                }
            )

            # --------------------------------
            # Leave Balance
            # --------------------------------

            cl = int(row["cl"]) if pd.notna(row["cl"]) else 0
            el = int(row["el"]) if pd.notna(row["el"]) else 0
            sl = int(row["sl_leave"]) if pd.notna(row["sl_leave"]) else 0

            total = cl + el + sl

            LeaveBalance.objects.update_or_create(

                user=user,

                defaults={
                    "cl": cl,
                    "el": el,
                    "sl": sl,
                    "total_leave": total,
                }
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Imported: {employee_id} - {username}"
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Employee import completed successfully."
            )
        )


        