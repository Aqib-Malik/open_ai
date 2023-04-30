# from os import path,include
from django.urls import path, include

from Api.views import AppointmentListView,PatientRegistrationView,BasicGenerationView



urlpatterns = [
    path('appointment',                                         AppointmentListView.as_view()),
    path('patient/register',                                    PatientRegistrationView.as_view()),
    path('basic-generation/',                                   BasicGenerationView.as_view(), name='basic-generation'),

]




