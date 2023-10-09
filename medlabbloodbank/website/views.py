from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages,auth
from django.contrib.auth import get_user_model
from .models import Donor
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST




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
from django.shortcuts import render, redirect
from .models import CustomUser,LabSelection
from datetime import timedelta
from .models import CustomUser, LabSelection, UploadedFile
from django.utils import timezone

def loginn(request):
    if request.method == "POST":
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.role == CustomUser.REGISTEREDDONOR:
                lab_selection = LabSelection.objects.filter(donor=user).order_by('-timestamp').first()
                if lab_selection and lab_selection.timestamp + timedelta(days=3) > timezone.now():
                    return redirect('uploadresult2', lab_selection_timestamp=str(lab_selection.timestamp))
                else:
                    # Check if the user has already uploaded a file within the 3-day limit
                    if UploadedFile.objects.filter(donor=user, timestamp__gte=timezone.now() - timedelta(days=3)).exists():
                        return redirect('waitforemail')
                    else:
                        messages.warning(request, 'The three-day window for uploading results has expired.')
                        return redirect('donatenow')

            if user.is_superadmin:  # Check if the user is a superuser (admin)
                return redirect('adminindex')  # Redirect to the admin dashboard
            elif user.role == CustomUser.HOSPITAL:
                return redirect('hospitalhome')
            elif user.role == CustomUser.STAFF:
                return redirect('staffindex')
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
        donor = Donor.objects.get(user=request.user)
        print(donor)
        return render(request, 'donatenow.html', {'donor':donor})
    else:
        # Redirect or render the "Register as Donor" page for others
        return redirect('registerasdonor') 
    

def registereddonortodonatenow(request):
    return render(request, 'registereddonortodonatenow.html')




def register_donor(request):
    if request.method == 'POST':
        # Handle form submission and validation here
        form = DonorRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Update the user fields
            request.user.email = form.cleaned_data['email']
            request.user.phone = form.cleaned_data['phone']
            request.user.save(update_fields=['email', 'phone'])

            # Save the form data to create a new Donor record
            donor = form.save(commit=False)
            donor.user = request.user  # Automatically associates with CustomUser
            donor.save()

            # Update the user's role to "Registered Donor"
            if request.user.role == CustomUser.DONOR:
                request.user.role = CustomUser.REGISTEREDDONOR
                request.user.save()

            # Redirect to a success page or perform other actions
            return redirect('registereddonortodonatenow')  # Change to your actual success page URL

    else:
        form = DonorRegistrationForm()

    return render(request, 'registerasdonor.html', {'form': form})



from django.shortcuts import render, redirect
from .models import DonorResponse



def registereddonorresponse(request):
    donor = request.user.donor
    print(donor)
    if request.method == 'POST':
        name = request.POST.get('name')
        user = request.user
        age = request.POST.get('age')
        bloodType = request.POST.get('bloodType')
        weight = request.POST.get('weight')
        donorHistory = request.POST.get('donorHistory')
        difficulty = request.POST.get('difficulty')
        donated = request.POST.get('donated')
        allergies = request.POST.get('allergies')
        alcohol = request.POST.get('alcohol')
        jail = request.POST.get('jail')
        surgery = request.POST.get('surgery')
        diseased = request.POST.get('diseased')
        hivaids = request.POST.get('hivaids')
        pregnant = request.POST.get('pregnant')
        child = request.POST.get('child')
        feelgood = request.POST.get('feelgood')

        # Create a DonorResponse instance and populate it with the data
        donor_response = DonorResponse(name=name,user=user,age=age,bloodType=bloodType,weight=weight,donorHistory=donorHistory,difficulty=difficulty,donated=donated,allergies=allergies,alcohol=alcohol,jail=jail,surgery=surgery,diseased=diseased,hivaids=hivaids,pregnant=pregnant,child=child,feelgood=feelgood)

        # Save the DonorResponse instance to the database
        donor_response.save()

        return redirect('notificationfordonation')
   

    return render(request, 'donatenow.html', {'donor': donor})

from django.shortcuts import render, redirect
from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from .models import LabSelection, Laboratory
from django.utils import timezone
from datetime import datetime
from django.contrib import messages

def send_sms(request):
    if request.method == 'POST':
        # Handle the form submission and extract necessary data
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        lab_id = request.POST.get('nearestLab')  # Assuming this is the lab ID
        nearest_lab_name = request.POST.get('nearestLabName')

        # Retrieve the Laboratory instance based on the lab ID
        selected_lab = get_object_or_404(Laboratory, id=lab_id)

        # Your logic to process the form data...
        lab_selection = LabSelection.objects.create(
            donor=request.user,
            selected_lab=selected_lab,
        )

        # Set session variable for lab selection timestamp
        request.session['lab_selection_timestamp'] = str(lab_selection.timestamp)
        
        # Compose the email content
        email_content = f"Greetings From Medlab Blood bank,\nFor proceeding with donation, get a sample blood test done and upload the result.\n\nSelected Lab: {nearest_lab_name}"

        # Send the email
        send_mail(
            'Blood Donation Instructions',
            email_content,
            'adhilaismail2@gmail.com',  # Sender's email address
            [email],  # Recipient's email address
            fail_silently=False,
        )

        # Your logic to handle the rest of the form submission...

        # Redirect to uploadresult and pass the timestamp of the lab selection
        return redirect('uploadresult2', lab_selection_timestamp=str(lab_selection.timestamp))

        # return redirect('uploadresult2', lab_selection_timestamp=lab_selection.timestamp)
    else:
        # Handle GET requests or other cases...
        return render(request, 'notificationfordonation.html')


from django.shortcuts import render,redirect
from django.utils import timezone
from datetime import timedelta, datetime
from .forms import UploadFileForm
from django.contrib import messages
from .models import LabSelection
from urllib.parse import unquote


# def uploadresult2(request, lab_selection_timestamp):
#     # Convert the lab_selection_timestamp string to a datetime object
#     # lab_selection_timestamp = datetime.strptime(lab_selection_timestamp, '%Y-%m-%d %H:%M:%S.%f%z')
#     lab_selection_timestamp = unquote(lab_selection_timestamp)
#     print(lab_selection_timestamp)
#     # Convert the lab_selection_timestamp string to a datetime object
#     lab_selection_timestamp = datetime.strptime(lab_selection_timestamp, '%Y-%m-%d %H:%M:%S.%f%z')
#     # Calculate the target date (3 days from the lab selection date)
#     target_date = lab_selection_timestamp + timedelta(days=3)
    
#     # Calculate the remaining time
#     current_time = timezone.now()
#     remaining_time = target_date - current_time
    
#     if remaining_time.total_seconds() <= 0:
#         messages.error(request, 'The three-day window for uploading results has expired.')
#         return redirect('donatenow')

#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             uploaded_file = form.cleaned_data['result_file']
            
#             # Save the uploaded file to your database
#             new_upload = UploadedFile(file=uploaded_file)
#             new_upload.save()

#             # Provide feedback to the user
#             messages.success(request, 'File uploaded successfully.')

#             # Redirect to a success page or do something else
#             return redirect('waitforemail')

#         else:
#             # Provide feedback to the user about form validation errors
#             messages.error(request, 'Please correct the errors in the form.')

#     else:
#         form = UploadFileForm()

#     # Pass the timestamp, target date, and remaining time to the template
#     context = {
#         'lab_selection_timestamp': lab_selection_timestamp.strftime("%Y-%m-%d %H:%M:%S.%f%z"),
#         'target_date': target_date.strftime("%Y-%m-%d %H:%M:%S.%f%z"),
#         'remaining_time_seconds': remaining_time.total_seconds(),
#         'form': form,
#     }
    
#     return render(request, 'uploadresult.html', context)

def uploadresult2(request, lab_selection_timestamp):
    # Convert the lab_selection_timestamp string to a datetime object
    lab_selection_timestamp = unquote(lab_selection_timestamp)
    print(lab_selection_timestamp)
    # Convert the lab_selection_timestamp string to a datetime object
    lab_selection_timestamp = datetime.strptime(lab_selection_timestamp, '%Y-%m-%d %H:%M:%S.%f%z')
    
    # Calculate the target date (3 days from the lab selection date)
    target_date = lab_selection_timestamp + timedelta(days=3)
    
    # Calculate the remaining time
    current_time = timezone.now()
    remaining_time = target_date - current_time
    
    if remaining_time.total_seconds() <= 0:
        messages.error(request, 'The three-day window for uploading results has expired.')
        return redirect('donatenow')

    # Check if the user has already submitted results
    user_has_submitted_results = UploadedFile.objects.filter(user=request.user).exists()

    # If the user has already submitted results, redirect or display a message
    if user_has_submitted_results:
        messages.info(request, 'You have already submitted your lab results.')
        return redirect('waitforemail')

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['result_file']
            
            # Save the uploaded file to your database
            new_upload = UploadedFile(file=uploaded_file, user=request.user)
            new_upload.save()

            # Provide feedback to the user
            messages.success(request, 'File uploaded successfully.')

            # Redirect to a success page or do something else
            return redirect('waitforemail')

        else:
            # Provide feedback to the user about form validation errors
            messages.error(request, 'Please correct the errors in the form.')

    else:
        form = UploadFileForm()

    # Pass the timestamp, target date, and remaining time to the template
    context = {
        'lab_selection_timestamp': lab_selection_timestamp.strftime("%Y-%m-%d %H:%M:%S.%f%z"),
        'target_date': target_date.strftime("%Y-%m-%d %H:%M:%S.%f%z"),
        'remaining_time_seconds': remaining_time.total_seconds(),
        'form': form,
    }
    
    return render(request, 'uploadresult.html', context)

def waitforemail(request):
    return render(request,'waitforemail.html')

# views.py
from django.http import JsonResponse
from .models import Laboratory

def getlaboratories(request):
    laboratories = Laboratory.objects.values('id', 'laboratoryName')
    return JsonResponse(list(laboratories), safe=False)


def notificationfordonation(request):
    return render(request, 'notificationfordonation.html')

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



from django.shortcuts import render

from django.contrib.auth.decorators import login_required

@login_required
def addlab(request):
    return render(request, 'mainuser/addlab.html')


# def assign_staff(request):

#     staff_members = Staff.objects.all()
#     grampanchayats = Grampanchayat.objects.all()
#     context = {
#         'staff_members': staff_members,
#         'grampanchayats': grampanchayats,
#     }
#     return render(request, 'mainuser/assigninggptostaff.html', context)
#.....................................
from django.shortcuts import render, redirect
from .models import Staff, Grampanchayat, AssignGrampanchayat

def assign_staff(request):
    if request.method == 'POST':
        staff_id = request.POST.get('staffName')
        grampanchayat1_id = request.POST.get('grampanchayat1')
        grampanchayat2_id = request.POST.get('grampanchayat2')
        grampanchayat3_id = request.POST.get('grampanchayat3')
        grampanchayat4_id = request.POST.get('grampanchayat4')
        grampanchayat5_id = request.POST.get('grampanchayat5')

        # Create AssignGrampanchayat objects
        staff = Staff.objects.get(pk=staff_id)
        grampanchayat1 = Grampanchayat.objects.get(pk=grampanchayat1_id)
        grampanchayat2 = Grampanchayat.objects.get(pk=grampanchayat2_id)
        grampanchayat3 = Grampanchayat.objects.get(pk=grampanchayat3_id)
        grampanchayat4 = Grampanchayat.objects.get(pk=grampanchayat4_id)
        grampanchayat5 = Grampanchayat.objects.get(pk=grampanchayat5_id)

        # Create AssignGrampanchayat instances
        assignment = AssignGrampanchayat.objects.create(
            staff=staff,
            grampanchayat1=grampanchayat1,
            grampanchayat2=grampanchayat2,
            grampanchayat3=grampanchayat3,
            grampanchayat4=grampanchayat4,
            grampanchayat5=grampanchayat5,
        )

        # Redirect to a success page or perform any other action
        return redirect('adminindex')  # Replace 'success_page' with the actual URL

    # If the request is not POST, render the form
    staff_members = Staff.objects.all()
    grampanchayats = Grampanchayat.objects.all()
    context = {
        'staff_members': staff_members,
        'grampanchayats': grampanchayats,
    }
    return render(request, 'mainuser/assigninggptostaff.html', context)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import AssignGrampanchayat, Grampanchayat
from django.db.models import Q
@csrf_exempt
@require_POST
def validate_assign_grampanchayat(request):
    grampanchayat_name = request.POST.get('grampanchayatName')

    # Check if the Grampanchayat exists in AssignGrampanchayat model
    try:
        AssignGrampanchayat.objects.get(
            Q(grampanchayat1__name_of_grampanchayat=grampanchayat_name) |
            Q(grampanchayat2__name_of_grampanchayat=grampanchayat_name) |
            Q(grampanchayat3__name_of_grampanchayat=grampanchayat_name) |
            Q(grampanchayat4__name_of_grampanchayat=grampanchayat_name) |
            Q(grampanchayat5__name_of_grampanchayat=grampanchayat_name)
        )
        exists = True
    except AssignGrampanchayat.DoesNotExist:
        exists = False

    return JsonResponse({'exists': exists})



from django.http import JsonResponse
from .models import Grampanchayat

def grampanchayat_list(request):
    grampanchayats = Grampanchayat.objects.all()
    data = [{'id': gp.id, 'name_of_grampanchayat': gp.name_of_grampanchayat} for gp in grampanchayats]
    return JsonResponse(data, safe=False)






#......................................................................................






def employees(request):
    return render(request, 'mainuser/employees.html')

def profile1(request):
    donor = Donor.objects.get(user=request.user)  # Adjust this based on your logic

    return render(request, 'mainuser/donorprofile.html', {'donor': donor})
    # return render(request, 'mainuser/donorprofile.html')

def editprofile(request):
    return render(request, 'mainuser/edit-profile.html')

def registereddonortable(request):
    donors = Donor.objects.all()
    donor_count = donors.count()  
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

def registeredstafftable(request):
    return render(request, 'mainuser/registeredstafftable.html')

# def listgps(request):
#     return render(request, 'mainuser/listgps.html')


from django.shortcuts import render
from .models import Grampanchayat

def listgps(request):
    grampanchayats = Grampanchayat.objects.all()
    return render(request, 'mainuser/listgps.html', {'grampanchayats': grampanchayats})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Grampanchayat

def edit_grampanchayat(request, pk):
    grampanchayat = get_object_or_404(Grampanchayat, pk=pk)

    if request.method == 'POST':
        grampanchayat.grampanchayat_id = request.POST.get('grampanchayat_id')
        grampanchayat.name_of_grampanchayat = request.POST.get('name_of_grampanchayat')
        # Update other fields as needed
        grampanchayat.save()
        return redirect('listgps')  # Redirect to the list view after successful edit

    return render(request, 'mainuser/edit-grampanchayat.html', {'grampanchayat': grampanchayat})



def addgps(request):
    return render(request, 'mainuser/add-grampanchayat.html')

from .models import Grampanchayat
from django.shortcuts import render, redirect

def grampanchayat_registration(request):
    error_message_id = ''
    error_message_name = ''
    
    if request.method == 'POST':
        grampanchayat_id = request.POST['grampanchayat_id']
        name_of_grampanchayat = request.POST['name_of_grampanchayat']
        
        # Check if a Grampanchayat with the given ID already exists
        if Grampanchayat.objects.filter(grampanchayat_id=grampanchayat_id).exists():
            error_message_id = 'Grampanchayat with this ID already exists'
        # Check if a Grampanchayat with the given name already exists
        if Grampanchayat.objects.filter(name_of_grampanchayat=name_of_grampanchayat).exists():
            error_message_name = 'Grampanchayat with this name already exists'
        # If no errors, create a new Grampanchayat
        if not error_message_id and not error_message_name:
            grampanchayat = Grampanchayat(
                grampanchayat_id=grampanchayat_id,
                name_of_grampanchayat=name_of_grampanchayat
            )
            grampanchayat.save()
            return redirect('adminindex')  # Redirect to a success page or list view

    return render(request, 'mainuser/add-grampanchayat.html', {'error_message_id': error_message_id, 'error_message_name': error_message_name})


def addnewgroup(request):
    return render(request, 'mainuser/addnewgroup.html')

def hospital_registration(request):
    if request.method == 'POST':
        hospitalName = request.POST.get('hospitalName')
        contactPerson = request.POST.get('contactPerson')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        location = request.POST.get('location')
        # gpsCoordinates = request.POST.get('gpsCoordinates')
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
            hospitalRegister = HospitalRegister(user=user,hospitalName=hospitalName, contactPerson=contactPerson, location=location,ownership=ownership,hospitalURL=hospitalURL)
            hospitalRegister.save()

            return redirect('registeredhospitaltable')

        
    else:
        return render(request, 'mainuser/hospitalregistration.html')

from django.shortcuts import render
from .models import HospitalRegister

def registeredhospitaltable(request):
    hospitals = HospitalRegister.objects.all()
    return render(request, 'mainuser/registeredhospitaltable.html', {'hospitals': hospitals})

from .models import Staff  # Import the Staff model
def registeredstafftable(request):
    # Retrieve the staff data from the database
    staff_list = Staff.objects.all()
    # Pass the staff data to the template
    context = {'staff_list': staff_list}
    return render(request, 'mainuser/registeredstafftable.html', context)



#hospital
def hospitalhome(request):
    return render(request, 'hospital/hospitalhome.html')

def requestblood(request):
    return render(request, 'hospital/requestblood.html')

from .models import BloodType
def bloodavailability(request):
    blood_types = BloodType.objects.all()
    return render(request, 'hospital/bloodavailability.html', {'blood_types': blood_types})

def hospitalabout(request):
    return render(request, 'hospital/hospitalabout.html')

def staff_registration(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        
        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'staff_registration.html', {'error_message': 'Email address already exists.'})
        
        if not name or not age or not gender or not dob or not email or not phone or not password:
            return render(request, 'staff_registration.html', {'error_message': 'Please fill in all required fields.'})
        
        try:
            # Create a CustomUser instance
            user = CustomUser.objects.create_user(email=email, phone=phone, password=password)
            user.role = CustomUser.STAFF
            user.save()

            # Create a Staff instance and associate it with the user
            staff = Staff(name=name, age=age, user=user, gender=gender, dob=dob)
            staff.save()

            return redirect('registeredstafftable')
        
        except IntegrityError as e:
            return render(request, 'mainuser/staffregistration.html', {'error_message': 'An error occurred during registration.'})
        
    else:
        return render(request, 'mainuser/staffregistration.html')


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
            return redirect('requestsent')
        else:
            # OTP is incorrect, display an error message
            messages.error(request, 'Invalid OTP. Please try again.')

    # Render the OTP verification page
    return render(request, 'hospital/verify_otp.html')






from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.utils.html import strip_tags  # Import the strip_tags function
from .models import BloodRequest

@csrf_exempt
def update_status(request):
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        new_status = request.POST.get('new_status')

        blood_request = get_object_or_404(BloodRequest, id=request_id)
        blood_request.status = new_status
        blood_request.save()

        # Send email to the user
        send_confirmation_email(blood_request.user.email, new_status)

        return JsonResponse({'requests': True})

    return JsonResponse({'requests': False})

def send_confirmation_email(to_email, status):
    subject = 'Blood Request Status Update'
    html_message = render_to_string('mainuser/email_template.html', {'status': status})
    plain_message = strip_tags(html_message)  # Create a plain text version of the email

    from_email = 'adhilaismail2@gmail.com'
    recipient_list = [to_email]

    # Set the content_type parameter to 'html'
    send_mail(subject, plain_message, from_email, recipient_list, fail_silently=False, html_message=html_message)




def requests(request):
    return render(request, 'mainuser/viewrequests.html')

def requestsent(request):
    return render(request,'hospital/requestsent.html')


from django.shortcuts import render
from .models import BloodRequest  # Import the BloodRequest model

def blood_request_list(request):
    blood_requests = BloodRequest.objects.all()  # Retrieve all BloodRequest objects from the database
    return render(request, 'mainuser/viewrequests.html', {'blood_requests': blood_requests})



#staff
def staffindex(request):
    return render(request, 'staff/index.html')

def activities(request):
    return render(request, 'staff/activities.html')

def appointmentsstaff(request):
    return render(request, 'staff/appointments.html')

def bloodbankcamps(request):
    return render(request, 'staff/bloodbankcamps.html')



def addhospitals(request):
    return render(request, 'staff/add-hospitals.html')

# def hospitalregistration(request):
#     return render(request, 'staff/hospitalregistration.html')

def employees(request):
    return render(request, 'staff/employees.html')

def profile(request):
    return render(request, 'staff/profile.html')

def editprofile(request):
    return render(request, 'staff/edit-profile.html')

def registereddonortablestaff(request):
    donors = Donor.objects.all()
    donor_count = donors.count()  
    return render(request, 'staff/registereddonortable.html', {'donors': donors, 'donor_count': donor_count})

def search_by_name(request):
    name = request.GET.get('name', '')
    donors = Donor.objects.filter(full_name__icontains=name)
    return render(request, 'staff/registereddonortable.html', {'donors': donors})

def search_by_place(request):
    place = request.GET.get('place', '')
    donors = Donor.objects.filter(place__icontains=place)
    return render(request, 'staff/registereddonortable.html', {'donors': donors})

def search_by_blood_group(request):
    blood_group = request.GET.get('blood_group', '')
    donors = Donor.objects.filter(blood_group__iexact=blood_group)
    return render(request, 'staff/registereddonortable.html', {'donors': donors})



from django.shortcuts import render
from .models import HospitalRegister






# from django.shortcuts import render
# from .models import BloodType

# def bloodinventory(request):
#     blood_types = BloodType.objects.all()
#     return render(request, 'staff/bloodinventory.html', {'blood_types': blood_types})


#schedule camp view
from django.shortcuts import render, redirect
from .models import BloodCamp, Staff
from django.contrib.auth.decorators import login_required

@login_required
def create_blood_camp(request):
    if request.method == 'POST':
        camp_date = request.POST.get('campDate')
        camp_name = request.POST.get('campName')
        camp_address = request.POST.get('campAddress')
        conducted_by = request.POST.get('conductedBy')
        gram_panchayat = request.POST.get('gramPanchayat')
        start_time = request.POST.get('startTime')
        end_time = request.POST.get('endTime')

        # Get the logged-in user
        user = request.user

        # Get the Staff object based on the logged-in user
        staff_member = Staff.objects.get(user=user)

        # Create a new BloodCamp object
        blood_camp = BloodCamp.objects.create(
            campDate=camp_date,
            campName=camp_name,
            campAddress=camp_address,
            user=user,
            conductedBy=conducted_by,
            organizedBy=staff_member,  # Set the organizedBy field here
            gramPanchayat=gram_panchayat,
            startTime=start_time,
            endTime=end_time,
        )
        blood_camp.save()
        # Redirect to a success page or another view
        return redirect('staffindex')

    # Render the template if it's a GET request
    return render(request, 'staff/bloodbankcamps.html')




from django.shortcuts import render
from .models import BloodCamp
def view_camp_schedules(request):
    camps = BloodCamp.objects.all()
    BloodCamp.objects.all().count()
    return render(request, 'staff/viewcampschedules.html', {'schedules': camps})



def viewlabresults(request):
    return render(request, 'mainuser/viewlabresults.html')

# views.py
# from django.shortcuts import render
# from .models import UploadedFile

# def view_uploaded_files(request):
#     uploaded_files = UploadedFile.objects.filter(user=request.user)
#     context = {'uploaded_files': uploaded_files}
#     return render(request, 'mainuser/viewlabresults.html', context)


from django.shortcuts import render
from .models import UploadedFile

def view_uploaded_files(request):
    uploaded_files = UploadedFile.objects.all()
    context = {'uploaded_files': uploaded_files}
    return render(request, 'mainuser/viewlabresults.html', context)


from django.http import FileResponse
from django.shortcuts import get_object_or_404
from .models import UploadedFile

def download_file(request, file_id):
    uploaded_file = get_object_or_404(UploadedFile, pk=file_id)
    file_path = uploaded_file.file.path
    response = FileResponse(open(file_path, 'rb'))
    return response

# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import UploadedFile

@csrf_exempt  # Use csrf_exempt for simplicity in this example; in a real project, use a proper csrf protection method
def update_approval_status(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        file_id = data.get('fileId')
        new_status = data.get('newStatus')

        try:
            uploaded_file = UploadedFile.objects.get(pk=file_id)
            uploaded_file.approval_status = new_status
            uploaded_file.save()

            # Send email notification
            user_email = uploaded_file.user.email
            subject = 'Medlab Blood Bank : Lab Results Update'
            if new_status == 'Approved':
                # Include a link for booking a camp
                booking_link = 'https://example.com/book-camp'
                message = (
                    f'Congratulations! Your lab results have been {new_status.lower()}. '
                    f'We invite you to book a camp using the following link: {booking_link}'
                )
            elif new_status == 'Rejected':
                message = f'We regret to inform you that your lab results have been {new_status.lower()}.'
            else:
                message = f'Your lab results have been updated to {new_status.lower()}.'

           

            send_mail(subject, message, 'your_email@example.com', [user_email])

            return JsonResponse({'message': 'Approval status updated successfully.'})
        except UploadedFile.DoesNotExist:
            return JsonResponse({'message': 'File not found.'}, status=404)

    return JsonResponse({'message': 'Invalid request.'}, status=400)