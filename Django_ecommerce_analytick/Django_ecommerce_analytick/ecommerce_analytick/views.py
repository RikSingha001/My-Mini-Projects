from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .forms import UserRegisterForm
from django.contrib.auth import login
from .models import DataAnalysisWithWeb

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UploadedFile
import pandas as pd
import matplotlib
matplotlib.use('Agg') # GUI ছাড়া ব্যাকএন্ডে ইমেজ সেভ করার জন্য এটি জরুরি
import matplotlib.pyplot as plt
import io
import urllib, base64
# Create your views here.
#this webside to emulate the e-commerce website and to test the analytics and data visualization features of the project. It will have a simple interface where users can browse products, add them to their cart, and make purchases. The website will also include a dashboard for administrators to view sales data and customer behavior analytics.

def index(request):
    return render(request, 'index.html')

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegisterForm

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')

    else:
        form = UserRegisterForm()

    return render(
        request,
        'registration/register.html',
        {'form': form}
    )






@login_required
def dashboard(request):
    chart_image = None
    columns = []
    message = ""

    # Step 1: Handle File Upload
    if request.method == "POST" and request.FILES.get('user_file'):
        uploaded_file = UploadedFile.objects.create(
            user=request.user,
            file=request.FILES['user_file']
        )
        return redirect('dashboard')

    # Get the latest uploaded file for this user
    latest_file = UploadedFile.objects.filter(user=request.user).order_by('-uploaded_at').first()

    if latest_file:
        try:
            # Step 2: Scan the file using Pandas
            file_path = latest_file.file.path
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)
            
            columns = df.columns.tolist() # Get all column names for the user to choose

            # Step 3: Handle User's Chart Request (Dynamic Visualization)
            if request.method == "POST" and 'generate_chart' in request.POST:
                x_axis = request.POST.get('x_axis')
                y_axis = request.POST.get('y_axis')
                chart_type = request.POST.get('chart_type')

                # Clear previous plots
                plt.clf()
                plt.figure(figsize=(10, 8))

                # Generate charts dynamically based on user selection
                if chart_type == 'bar':
                    df.groupby(x_axis)[y_axis].sum().plot(kind='bar', color='skyblue')
                elif chart_type == 'line':
                    df.groupby(x_axis)[y_axis].sum().plot(kind='line', marker='o', color='orange')
                elif chart_type == 'scatter':
                    plt.scatter(df[x_axis], df[y_axis], color='green')
                    plt.xlabel(x_axis)
                    plt.ylabel(y_axis)

                plt.title(f"{chart_type.capitalize()} Chart: {x_axis} vs {y_axis}")
                plt.tight_layout()

                # Step 4: Convert Matplotlib Plot to Base64 String to show in HTML
                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                buf.seek(0)
                string = base64.b64encode(buf.read())
                chart_image = urllib.parse.quote(string)

        except Exception as e:
            message = f"Error scanning file: {str(e)}"

    context = {
        'columns': columns,
        'chart_image': chart_image,
        'message': message,
        'latest_file': latest_file
    }
    return render(request, 'dashboard.html', context)