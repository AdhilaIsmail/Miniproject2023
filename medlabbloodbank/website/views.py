from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages,auth
from django.contrib.auth import get_user_model
from .models import Donor

# from django.core.mail import send_mail
# from django.shortcuts import redirect
# from django.contrib.auth.decorators import login_required

# from .models import Donor
User = get_user_model()

def index(request):
    return render(request, 'index.html')
def about(request):
    return render(request, 'about.html')
def contact(request):
    return render(request, 'contact.html')
def service(request):
    return render(request, 'service.html')

def registerasdonor(request):
    return render(request, 'registerasdonor.html')
# def donatenow(request):
#     return render(request, 'donatenow.html')
def appointmentschedule(request):
    return render(request, 'appointmentschedule.html')
def homebloodbank(request):
    return render(request, 'homebloodbank.html')
def testimonial(request):
    return render(request, 'testimonial.html')
# def loginn(request):
#     if request.method == "POST":
#         username=request.POST['email']
#         password=request.POST['password']
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('/')
#         else:
#             messages.info(request, "Invalid Login")
#             return redirect('loginn')
#     else:
#         return render(request, 'login.html')  

##checking
from django.contrib.auth import authenticate, login

def loginn(request):
    if request.method == "POST":
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.is_superuser:  # Check if the user is a superuser (admin)
                return redirect('adminindex')  # Redirect to the admin dashboard
            else:
                return redirect('index')  # Redirect to the custom dashboard for non-admin users
        else:
            messages.info(request, "Invalid Login")
            return redirect('loginn')
    else:
        return render(request, 'login.html')
  

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email', None)
        phone = request.POST.get('phone', None)
        password = request.POST.get('pass', None)
        role=User.DONOR

        if email and phone and password and role:
            if User.objects.filter(email=email).exists():
                error_message = "Email is already registered."
                return render(request, 'registration.html', {'error_message': error_message})
            
            else:
                user = User(email=email, phone=phone, role=role)
                user.set_password(password)  # Set the password securely
                user.save()
                return redirect('login')  
            
    return render(request, 'registration.html')

#this is for normal registratio
def registration(request):
    messages=""
    if request.method == "POST":
        # fullName = request.POST['fullName']
        username = request.POST['email']
        password = request.POST['password']
        confirmPassword = request.POST['confirmPassword']

        if password == confirmPassword:
            # if User.objects.filter(fullName=fullName).exists():
            #     return render(request, 'registration.html', {'fullName_exists': True})
            if User.objects.filter(username=username).exists():
                return render(request, 'registration.html', {'username_exists': True})


            # elif User.objects.filter(email=email).exists():
            #     messages.info(request, 'Email already exists')
            #     return redirect('registration')
            
            else:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                # messages.success(request, 'Registration successful. You can now log in.')
                return redirect('loginn')

        else:
            messages.error(request, 'Password confirmation does not match')
            return redirect('registration')
    else:
        return render(request, 'registration.html')

def loggout(request):
    auth.logout(request)
    return redirect('/')

#this is for register as donor
from django.shortcuts import render, redirect
from .forms import DonorRegistrationForm




from .models import CustomUser

def donatenow(request):
    if request.user.is_authenticated and request.user.role == CustomUser.REGISTEREDDONOR:
        # Render the "Donate Now" page for Registered Donors
        return render(request, 'donatenow.html')
    else:
        # Redirect or render the "Register as Donor" page for others
        return redirect('registerasdonor') 
    
    
def register_donor(request):
    

    if request.method == 'POST':
        # Handle form submission and validation here
        form = DonorRegistrationForm(request.POST)
        if form.is_valid():
            # Save the form data to create a new Donor record
            donor = form.save(commit=False)


            
            donor.email = request.user.email  # Set the email based on the logged-in user
            donor.save()

            # Update the user's role to "Registered Donor"
            if request.user.role == CustomUser.DONOR:
                request.user.role = CustomUser.REGISTEREDDONOR
                request.user.save()

            # Redirect to a success page or perform other actions
            return redirect('donatenow')  # Change 'success_page' to the actual success page URL

    else:
        # form = DonorRegistrationForm()
        form = DonorRegistrationForm()

    return render(request, 'registerasdonor.html', {'form': form})



from django.shortcuts import render, redirect
from .models import DonorResponse
from .forms import DonorForm  # Import the DonorForm

def registereddonorresponse(request):
    if request.method == 'POST':
        form = DonorForm(request.POST)  # Create a form instance with POST data
        if form.is_valid():
            form.save()  # Save the data to the database
            # You can add a success message or redirect to a thank you page here.
            return redirect('notificationfordonation')
    else:
        form = DonorForm()  # Create an empty form instance for GET requests

    return render(request, 'donatenow.html', {'form': form})

def notificationfordonation(request):
    return render(request, 'notificationfordonation.html')


# from twilio.rest import Client
# from django.conf import settings
# from django.http import HttpResponse

# def send_sms(request):
#     if request.method == 'POST':
#         phone_number = request.POST['phone']
#         message = "Get a blood sample test"

#         client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
#         try:
#             message = client.messages.create(
#                 body=message,
#                 from_=settings.TWILIO_PHONE_NUMBER,
#                 to=phone_number
#             )
#             return HttpResponse("SMS sent successfully!")
#         except Exception as e:
#             return HttpResponse(f"SMS failed to send: {str(e)}")

#     return HttpResponse("Invalid request method")


from django.shortcuts import render, redirect
from django.http import HttpResponse
from twilio.rest import Client
from django.conf import settings

def send_sms(request):
    if request.method == 'POST':
        phone_number = request.POST['phone']
        message = "Get a free sample blood test and upload the results in the site."

        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        try:
            message = client.messages.create(
                body=message,
                from_=settings.TWILIO_PHONE_NUMBER,
                to=phone_number
            )
            # If the SMS is sent successfully, redirect to another page
            return redirect('uploadresult')  # Replace 'success_page' with the URL name of the page you want to redirect to
        except Exception as e:
            return HttpResponse(f"SMS failed to send: {str(e)}")

    return HttpResponse("Invalid request method")

# def uploadresult(request):
#     return render(request, 'uploadresult.html')


from .forms import UploadFileForm
from .models import UploadedFile


def uploadresult(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['result_file']
            # Save the uploaded file to your database
            new_upload = UploadedFile(file=uploaded_file)
            new_upload.save()
            # Redirect to a success page or do something else
            return redirect('homebloodbank')
    else:
        form = UploadFileForm()

    return render(request, 'uploadresult.html', {'form': form})



#admin dashboard

def adminindex(request):
    return render(request, 'mainuser/index.html')

def activities(request):
    return render(request, 'mainuser/activities.html')

def appointments(request):
    return render(request, 'mainuser/appointments.html')

def departments(request):
    return render(request, 'mainuser/departments.html')

def doctors(request):
    return render(request, 'mainuser/doctors.html')

def addhospitals(request):
    return render(request, 'mainuser/add-hospitals.html')

def hospitalregistration(request):
    return render(request, 'mainuser/hospitalregistration.html')

def employees(request):
    return render(request, 'mainuser/employees.html')

def profile(request):
    return render(request, 'mainuser/profile.html')

def editprofile(request):
    return render(request, 'mainuser/edit-profile.html')

def registereddonortable(request):
    donors = Donor.objects.all()
    donor_count = donors.count()  # Get the count of registered donors
    # return render(request, 'donor_table.html', {'donors': donors, 'donor_count': donor_count})
    return render(request, 'mainuser/registereddonortable.html', {'donors': donors, 'donor_count': donor_count})




def search_by_name(request):
    name = request.GET.get('name', '')
    donors = Donor.objects.filter(full_name__icontains=name)
    return render(request, 'mainuser/registereddonortable.html', {'donors': donors})

def search_by_place(request):
    place = request.GET.get('place', '')
    donors = Donor.objects.filter(place__icontains=place)
    return render(request, 'mainuser/registereddonortable.html', {'donors': donors})

def search_by_blood_group(request):
    blood_group = request.GET.get('blood_group', '')
    donors = Donor.objects.filter(blood_group__iexact=blood_group)
    return render(request, 'mainuser/registereddonortable.html', {'donors': donors})


def bloodinventory(request):
    return render(request, 'mainuser/bloodinventory.html')

def addnewgroup(request):
    return render(request, 'mainuser/addnewgroup.html')




def hospitalhome(request):
    return render(request, 'hospital/hospitalhome.html')


def requestblood(request):
    return render(request, 'hospital/requestblood.html')

def bloodavailability(request):
    return render(request, 'hospital/bloodavailability.html')

def hospitalabout(request):
    return render(request, 'hospital/hospitalabout.html')


from django.shortcuts import render, redirect
from .forms import HospitalRegisterForm

def hospital_registration(request):
    if request.method == 'POST':
        form = HospitalRegisterForm(request.POST)
        if form.is_valid():
            form.save()  # Save the data to the database
            # Redirect to a success page or do something else
            return redirect('adminindex')  # Replace with your success page URL name
    else:
        form = HospitalRegisterForm()

    return render(request, 'mainuser/hospitalregistration.html', {'form': form})


#neededone
#hospital registration
# from django.shortcuts import render, redirect
# from .forms import HospitalForm

# def hospitalregister(request):
#     if request.method == 'POST':
#         form = HospitalForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('registeredhospitaltable')  # Redirect to a success page
#     else:
#         form = HospitalForm()
#     return render(request, 'mainuser/hospitalregister.html', {'form': form})



# views.py
#needed one
from django.shortcuts import render
from .models import HospitalRegister

def registeredhospitaltable(request):
    hospitals = HospitalRegister.objects.all()
    return render(request, 'mainuser/registeredhospitaltable.html', {'hospitals': hospitals})



# views.py

# views.py
#needd one
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from .models import HospitalRegister

# @csrf_exempt  # Use csrf_exempt for simplicity. You may want to implement CSRF protection properly in your project.
# def update_hospital_status(request, hospital_id):
#     if request.method == 'POST':
#         try:
#             hospital = HospitalRegister.objects.get(pk=hospital_id)
#             hospital.status = 'Inactive'
#             hospital.save()
#             return JsonResponse({'message': 'Hospital status updated successfully'})
#         except HospitalRegister.DoesNotExist:
#             return JsonResponse({'error': 'Hospital not found'}, status=404)
#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=400)


# from django.shortcuts import render, get_object_or_404
# from .models import HospitalRegister  # Import your Hospital model

# def edit_hospital(request, hospital_id):
#     hospital = get_object_or_404(HospitalRegister, id=hospital_id)  # Replace 'Hospital' with your actual model name
#     context = {'hospital': hospital}
#     return render(request, 'mainuser/hospitalregistration.html', context)

# from django.shortcuts import render, redirect, get_object_or_404
# from .models import HospitalRegister
# from .forms import HospitalForm

# def edit_hospital(request, hospital_id):
#     hospital = get_object_or_404(HospitalRegister, pk=hospital_id)
    
#     if request.method == 'POST':
#         form = HospitalForm(request.POST, instance=hospital)
#         if form.is_valid():
#             form.save()  # This will update the existing hospital record
#             return redirect('registeredhospitaltable')  # Redirect to the hospital list view or another appropriate page
#     else:
#         form = HospitalForm(instance=hospital)
    
#     return render(request, 'mainuser/hospitalregistration.html', {'form': form, 'hospital': hospital})

# views.py

from django.shortcuts import render, redirect
from .forms import BloodTypeForm
from django.db import IntegrityError  # Import IntegrityError

def addblood(request):
    if request.method == 'POST':
        form = BloodTypeForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('bloodinventory')
            except IntegrityError:
                form.add_error('blood_type', 'Blood type already exists.')  # Add a form error
    else:
        form = BloodTypeForm()
    return render(request, 'mainuser/addnewgroup.html', {'form': form})


# views.py

from django.shortcuts import render
from .models import BloodType

def bloodinventory(request):
    blood_types = BloodType.objects.all()
    return render(request, 'mainuser/bloodinventory.html', {'blood_types': blood_types})







