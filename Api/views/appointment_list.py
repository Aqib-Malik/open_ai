from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from Api.models import Appointment
from Api.serializers import AppointmentSerializer
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework import viewsets
    
    
    

class AppointmentListView(ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Appointment.objects.filter(fees__lt=2000).filter(status=0)
        return queryset

# class AppointmentListView(ListAPIView):

#     serializer_class = AppointmentSerializer

#     # def get(self, request, *args, **kwargs):
#     #     return super().get(request, *args, **kwargs)

#     def get_queryset(self):
        
        
#         appointments = Appointment.objects.all()
        
#         for a in appointments:
#             if a<200: 
            
#                 print(a.fees)

#         return appointments
