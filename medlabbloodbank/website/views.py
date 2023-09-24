from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages,auth
from django.contrib.auth import get_user_model
from .models import Donor
from django.contrib.auth.decorators import login_required


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
from .models import CustomUser 

def loginn(request):
    if request.method == "POST":
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.is_superadmin:  # Check if the user is a superuser (admin)
                return redirect('adminindex')  # Redirect to the admin dashboard
            elif user.role == CustomUser.HOSPITAL:
                return redirect('hospitalhome')
            else:
                return redirect('index')  # Redirect to the custom dashboard for non-admin users
        else:
            messages.error(request, "Invalid Login")
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
                print('Enydsgv')
                user = User(email=email, phone=phone, role=role)
                user.set_password(password)  # Set the password securely
                user.save()
                return redirect('loginn')  
            
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
        donor = request.user.donor
        return render(request, 'donatenow.html', {'donor':donor})
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

# def registereddonorresponse(request):
#     if request.method == 'POST':
#         form = DonorForm(request.POST)  # Create a form instance with POST data
#         if form.is_valid():
#             form.save()  # Save the data to the database
#             # You can add a success message or redirect to a thank you page here.
#             return redirect('notificationfordonation')
#     else:
#         form = DonorForm()  # Create an empty form instance for GET requests

#     return render(request, 'donatenow.html', {'form': form})

# def notificationfordonation(request):
#     return render(request, 'notificationfordonation.html')


def registereddonorresponse(request):
    donor = request.user.donor
    print(donor)
    if request.method == 'POST':
        form = DonorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('notificationfordonation')
    else:
        # Fetch the data from the database (assuming you want to prefill the last entry)
        latest_entry = DonorResponse.objects.last()
        initial_data = {
            'name': latest_entry.name,
            'bloodType': latest_entry.bloodType,
            # Add other fields as needed
        }
        form = DonorForm(initial=initial_data)

    return render(request, 'donatenow.html', {'form': form, 'donor': donor})


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

from twilio.rest import Client
from django.conf import settings
from django.http import HttpResponse

def send_sms(request):
    if request.method == 'POST':
        phone_number = request.POST['phone']
        message = "Get your sample test done and upload your results on the website.HAPPY DONATION.."

        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        try:
            message = client.messages.create(
                body=message,
                from_=settings.TWILIO_PHONE_NUMBER,
                to=phone_number
            )
            return HttpResponse("SMS sent successfully!")
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

def notificationfordonation(request):
    return render(request, 'notificationfordonation.html')


def hospitalhome(request):
    return render(request, 'hospital/hospitalhome.html')


def requestblood(request):
    return render(request, 'hospital/requestblood.html')



from .models import BloodType
def bloodavailability(request):
    blood_types = BloodType.objects.all()

    # Pass the blood_types to the template context
    return render(request, 'hospital/bloodavailability.html', {'blood_types': blood_types})

def hospitalabout(request):
    return render(request, 'hospital/hospitalabout.html')


from django.shortcuts import render, redirect


# def hospital_registration(request):
#     if request.method == 'POST':
#         hospitalName = request.POST.get('hospitalName')
#         contactPerson = request.POST.get('contactPerson')
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')
#         location = request.POST.get('location')
#         gpsCoordinates = request.POST.get('gpsCoordinates')
#         ownership = request.POST.get('ownership')
#         hospitalURL = request.POST.get('hospitalURL')
#         password = request.POST.get('password')
        
#         roles = CustomUser.HOSPITAL
#         print(roles)
#         if CustomUser.objects.filter(email=email,role=roles).exists():
#             return render(request, 'mainuser/hospitalregistration.html')
#         else:
#             user=CustomUser.objects.create_user(email=email,phone=phone,password=password,role=roles)
#             hospitalRegister = HospitalRegister(user=user,hospitalName=hospitalName, contactPerson=contactPerson, location=location,gpsCoordinates=gpsCoordinates,ownership=ownership,hospitalURL=hospitalURL)
#             hospitalRegister.save()

#             return redirect('registeredhospitaltable')

def hospital_registration(request):
    if request.method == 'POST':
        hospitalName = request.POST.get('hospitalName')
        contactPerson = request.POST.get('contactPerson')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        location = request.POST.get('location')
        gpsCoordinates = request.POST.get('gpsCoordinates')
        ownership = request.POST.get('ownership')
        hospitalURL = request.POST.get('hospitalURL')
        password = request.POST.get('password')
        
        roles = CustomUser.HOSPITAL
        print(roles)
        if CustomUser.objects.filter(email=email,role=CustomUser.HOSPITAL).exists():
            return render(request, 'mainuser/hospitalregistration.html')
        else:
            user=CustomUser.objects.create_user(email=email,phone=phone,password=password)
            user.role = CustomUser.HOSPITAL
            user.save()
            hospitalRegister = HospitalRegister(user=user,hospitalName=hospitalName, contactPerson=contactPerson, location=location,gpsCoordinates=gpsCoordinates,ownership=ownership,hospitalURL=hospitalURL)
            hospitalRegister.save()

            return redirect('registeredhospitaltable')

        
    else:
        return render(request, 'mainuser/hospitalregistration.html')
    



from django.shortcuts import render
from .models import HospitalRegister

def registeredhospitaltable(request):
    hospitals = HospitalRegister.objects.all()
    return render(request, 'mainuser/registeredhospitaltable.html', {'hospitals': hospitals})







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


from django.shortcuts import render, redirect
from .models import BloodRequest  # Import your model
from datetime import datetime 

from django.contrib import messages
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt



@csrf_exempt  # Use csrf_exempt for simplicity; consider proper CSRF protection in production

def bloodrequest(request, is_immediate):
    print(f"is_immediate: {is_immediate}")  # Debug statement

    if request.method == 'POST':
        user = request.user
        blood_group = request.POST.get('blood_group')
        quantity = request.POST.get('quantity')
        purpose = request.POST.get('purpose')


        otp = get_random_string(length=6, allowed_chars='1234567890')
        
        print(f"OTP: {otp}")

        request.session['hospital_otp'] = otp
        
        subject = 'Your OTP for Blood Request: Medlab Blood Bank'
        message = f'Your OTP is: {otp}'
        from_email = 'adhilaismail2@gmail.com'  # Replace with your email
        recipient_list = [user.email]  # Assuming you want to send the OTP to the user's email address

        # Use send_mail to send the OTP email
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        requested_date = datetime.now().date()
        requested_time = datetime.now().time()

        is_immediate = is_immediate.lower() == 'true'
        # Create and save a new BloodRequest instance
        blood_request = BloodRequest(user=user, blood_group=blood_group,quantity=quantity, purpose=purpose,  requested_date=requested_date, requested_time=requested_time, is_immediate=is_immediate)
        blood_request.save()

        return redirect('verify_hospital')


    return render(request, 'hospital/requestblood.html', {'is_immediate': is_immediate})


from django.shortcuts import render, redirect
from django.contrib import messages
# Assuming you have stored the OTP in the session as 'hospital_otp'
from django.shortcuts import render, redirect
from django.core.mail import send_mail  # Import send_mail
from django.utils.crypto import get_random_string

def verify_hospital(request):
    if request.method == 'POST':
        # Get the entered OTP from the form
        entered_otp = request.POST.get('otp')
        
        # Get the OTP stored in the session
        stored_otp = request.session.get('hospital_otp')

        if entered_otp == stored_otp:
            # OTP is correct, clear it from the session
            del request.session['hospital_otp']

            # Redirect to the hospital home page
            return redirect('hospitalhome')
        else:
            # OTP is incorrect, display an error message
            messages.error(request, 'Invalid OTP. Please try again.')

    # Render the OTP verification page
    return render(request, 'hospital/verify_otp.html')


def requests(request):
    return render(request, 'mainuser/viewrequests.html')



from django.shortcuts import render
from .models import BloodRequest  # Import the BloodRequest model

def blood_request_list(request):
    blood_requests = BloodRequest.objects.all()  # Retrieve all BloodRequest objects from the database
    return render(request, 'mainuser/viewrequests.html', {'blood_requests': blood_requests})




