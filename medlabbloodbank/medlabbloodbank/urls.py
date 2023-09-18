"""
URL configuration for medlabbloodbank project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include
from website import views
from website.views import index, about,  service, testimonial, contact, loginn, register_donor, donatenow, registerasdonor, registereddonorresponse, notificationfordonation, send_sms, uploadresult, homebloodbank, appointmentschedule, register, loggout
from django.contrib.auth import views as auth_views
from website.views import adminindex, activities, appointments, doctors, departments, employees, profile, editprofile, registereddonortable
from website.views import search_by_name, search_by_place,search_by_blood_group, addhospitals, hospitalregistration, hospital_registration, registeredhospitaltable
from website.views import bloodinventory, addnewgroup, addblood
from website.views import hospitalhome, requestblood, bloodavailability, hospitalabout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index, name='index'),
    path('about',about, name='about'),
    path('service',service, name='service'),
    path('testimonial',testimonial, name='testimonial'),
    path('contact',contact, name='contact'),
    path('loginn', loginn, name='loginn'),
    path('registerasdonor',registerasdonor, name='registerasdonor'),
    path('register_donor/', register_donor, name='register_donor'),
    # path('questionnaire/', questionnaire, name='questionnaire'),
    path('donatenow',donatenow, name='donatenow'),
    path('appointmentschedule',appointmentschedule, name='appointmentschedule'),
    path('homebloodbank',homebloodbank, name='homebloodbank'),
    path('registration',register, name='registration'),
    path('register/', register_donor, name='register_donor'),
    path('registereddonorresponse/', registereddonorresponse, name='registereddonorresponse'),
    path('notificationfordonation', notificationfordonation, name='notificationfordonation'),
    path('send_sms/', send_sms, name='send_sms'),
    path('uploadresult', uploadresult, name='uploadresult'),


    #  path('successful-login/', successful_login, name='successful_login'),
    # path('register_donor/', views.register_donor, name='register_donor'),
    
    
    path('loggout', loggout, name='loggout'),
    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path("",include("allauth.urls")),


    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),


    #admindashboard
    path('adminindex', adminindex, name='adminindex'),
    path('activities', activities, name='activities'),
    path('appointments', appointments, name='appointments'),
    path('departments', departments, name='departments'),
    path('doctors', doctors, name='doctors'),
    path('employees', employees, name='employees'),
   
    path('profile', profile, name='profile'),
    path('editprofile', editprofile, name='editprofile'),
    path('registereddonortable', registereddonortable, name='registereddonortable'),
    path('addhospitals', addhospitals, name='addhospitals'),
    path('hospitalregistration', hospitalregistration, name='hospitalregistration'),
    path('hospital-registration/', hospital_registration, name='hospital_registration'),
    path('search-by-name/', search_by_name, name='search_by_name'),
    path('search-by-place/', search_by_place, name='search_by_place'),
    path('search-by-blood-group/', search_by_blood_group, name='search_by_blood_group'),
    path('registeredhospitaltable/', registeredhospitaltable, name='registeredhospitaltable'),
    # path('update_hospital_status/<int:hospital_id>/', update_hospital_status, name='update_hospital_status'),
    path('bloodinventory', bloodinventory, name='bloodinventory'),
    path('addnewgroup', addnewgroup, name='addnewgroup'),
    path('addblood/', addblood, name='addblood'),
  
    

   
    

    #hospital
    path('hospitalhome', hospitalhome, name='hospitalhome'),
    path('requestblood', requestblood, name='requestblood'),
    path('bloodavailability', bloodavailability, name='bloodavailability'),
    path('hospitalabout', hospitalabout, name='hospitalabout'),

  

  
 
]
