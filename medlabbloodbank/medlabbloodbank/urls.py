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
from website.views import index, about,  service, testimonial, contact, loginn, register_donor, donatenow, registerasdonor
from website.views import registereddonorresponse, registereddonortodonatenow, notificationfordonation, send_sms, uploadresult, uploadresult2
from website.views import homebloodbank, appointmentschedule, register, loggout
from django.contrib.auth import views as auth_views
from website.views import adminindex, activities, appointments, doctors, departments, employees, profile1, editprofile,requestsent
from website.views import registereddonortable, search_by_name, search_by_place, search_by_blood_group, addhospitals, hospitalregistration,waitforemail
from website.views import hospital_registration, registeredhospitaltable, bloodrequest, registeredstafftable, staff_registration,getlaboratories,send_confirmation_email
from website.views import bloodinventory, addnewgroup, addblood, requests, requestblood,appointmentsstaff,hospitalhome, bloodavailability, hospitalabout, blood_request_list, verify_hospital, staffindex,validate_assign_grampanchayat
from website.views import registereddonortablestaff, departmentsstaff, assign_staff, listgps, addgps, grampanchayat_registration, grampanchayat_list,addlab,update_status

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
    path('donatenow',donatenow, name='donatenow'),
    path('appointmentschedule',appointmentschedule, name='appointmentschedule'),
    path('homebloodbank',homebloodbank, name='homebloodbank'),
    path('registration',register, name='registration'),
    path('register/', register_donor, name='register_donor'),
    path('registereddonortodonatenow', registereddonortodonatenow, name='registereddonortodonatenow'),
    path('registereddonorresponse/', registereddonorresponse, name='registereddonorresponse'),
    path('notificationfordonation', notificationfordonation, name='notificationfordonation'),
    path('getlaboratories',getlaboratories,name='getlaboratories'),
    path('send_sms/', send_sms, name='send_sms'),
    path('uploadresult', uploadresult, name='uploadresult'),
    path('uploadresult2/<str:lab_selection_timestamp>/', uploadresult2, name='uploadresult2'),
    path('waitforemail',waitforemail,name='waitforemail'),

    # path('uploadresult2/<path:lab_selection_timestamp>/', uploadresult2, name='uploadresult2'),
    path('loggout', loggout, name='loggout'),
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
    path('profile1', profile1, name='profile1'),
    path('editprofile', editprofile, name='editprofile'),
    path('registereddonortable', registereddonortable, name='registereddonortable'),
    path('addhospitals', addhospitals, name='addhospitals'),
    path('hospitalregistration', hospitalregistration, name='hospitalregistration'),
    path('hospital-registration/', hospital_registration, name='hospital_registration'),
    path('registeredstafftable/', registeredstafftable, name='registeredstafftable'),
    path('search-by-name/', search_by_name, name='search_by_name'),
    path('search-by-place/', search_by_place, name='search_by_place'),
    path('search-by-blood-group/', search_by_blood_group, name='search_by_blood_group'),
    path('registeredhospitaltable/', registeredhospitaltable, name='registeredhospitaltable'),
    path('bloodinventory', bloodinventory, name='bloodinventory'),
    path('addnewgroup', addnewgroup, name='addnewgroup'),
    path('addblood/', addblood, name='addblood'),
    path('requests', requests, name='requests'),
    path('blood_request_list', blood_request_list, name='blood_request_list'),
    path('staff_registration', staff_registration, name='staff_registration'),
    path('assign_staff', assign_staff, name='assign_staff'),
    path('listgps', listgps, name='listgps' ),
    path('addgps', addgps, name='addgps' ),
    path('grampanchayat_registration', grampanchayat_registration, name='grampanchayat_registration' ),
    path('validate-assign-grampanchayat/', validate_assign_grampanchayat, name='validate_assign_grampanchayat'),
    path('api/grampanchayats/', grampanchayat_list, name='grampanchayat_list'),
    path('edit_grampanchayat/<int:pk>/', views.edit_grampanchayat, name='edit_grampanchayat'),
    path('addlab',addlab,name='addlab'),
    path('update_status/', update_status, name='update_status'),
    path('send_confirmation_email',send_confirmation_email,name='send_confirmation_email'),
   

   
    
    #hospital
    path('hospitalhome', hospitalhome, name='hospitalhome'),
    path('requestblood', requestblood, name='requestblood'),  
    path('bloodavailability', bloodavailability, name='bloodavailability'),
    path('hospitalabout', hospitalabout, name='hospitalabout'),
    path('bloodrequest/<str:is_immediate>/', bloodrequest, name='bloodrequest'),
    path('verify_hospital', verify_hospital, name='verify_hospital'),
    path('requestsent',requestsent,name='requestsent'),

    
  
    #staff

    path('staffindex', staffindex, name='staffindex'),
    path('activities', activities, name='activities'),
    path('appointmentsstaff', appointmentsstaff, name='appointmentsstaff'),
    path('departmentsstaff', departmentsstaff, name='departmentsstaff'),
    path('doctors', doctors, name='doctors'),
    path('employees', employees, name='employees'),
    path('profile1', profile1, name='profile1'),
    path('editprofile', editprofile, name='editprofile'),
    path('registereddonortablestaff', registereddonortablestaff, name='registereddonortablestaff'),
    path('addhospitals', addhospitals, name='addhospitals'),
   
    path('search-by-name/', search_by_name, name='search_by_name'),
    path('search-by-place/', search_by_place, name='search_by_place'),
    path('search-by-blood-group/', search_by_blood_group, name='search_by_blood_group'),
    path('registeredstafftable/', registeredstafftable, name='registeredstafftable'),
    path('bloodinventory', bloodinventory, name='bloodinventory'),
    path('addnewgroup', addnewgroup, name='addnewgroup'),
    path('addblood/', addblood, name='addblood'),
   
    path('blood_request_list', blood_request_list, name='blood_request_list'),
 
]
