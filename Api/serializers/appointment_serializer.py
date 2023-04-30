from django.conf import settings
from rest_framework import serializers
from Api.models import Appointment
import math

class AppointmentSerializer(serializers.ModelSerializer):
    # patient             = PatientSerializer()
    # doctor              = DoctorSerializer()
    # created_by          = UserSerializer(fields=('id', 'username', 'email'))
    # updated_by          = UserSerializer(fields=('id', 'username', 'email'))
    # consumer_number     = serializers.SerializerMethodField(read_only=True)

    # def to_representation(self, instance):
    #     hospital_name = instance.department.hospital.name
    #     instance=super().to_representation(instance)
    #     instance['hospital_name'] = hospital_name
    #     return instance

    class Meta:
        model = Appointment
        fields = '__all__'
    def validate(self, attrs):
        doctor = attrs.get('doctor')
        patient = attrs.get('patient')
        fees = attrs.get('fees')
        scheduled_date = attrs.get('scheduled_date')
        is_panel = attrs.get('is_panel')
        spec_share = attrs.get('spec_share')
        govt_share = attrs.get('govt_share')
        hosp_amenity_share = attrs.get('hosp_amenity_share')
        staff_share = attrs.get('staff_share')
        total_fees = attrs.get('total_fees')
        fee = total_fees
        print("*****")
        print(doctor)
        return super().validate(attrs)
    

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

#     def get_consumer_number(self, obj):
#         return obj.consumer_number

# class AppointmentCreateSerializer(serializers.ModelSerializer):
#     consumer_number = serializers.SerializerMethodField(read_only=True)
    
#     class Meta:
#         model = Appointment
#         fields = ['id', 'status', 'fees', 'is_paid', 'patient', 'doctor', 'scheduled_date', 'is_panel','panel', 'employment_number','created_at', 'created_by', 'updated_at', 'updated_by', 'consumer_number', 'department', 'spec_share', 'govt_share', 'hosp_amenity_share', 'staff_share', 'total_fees', 'approved_by']
#         read_only_fields = ['created_at', 'created_by', 'updated_at', 'updated_by', 'consumer_number', 'department']
#         extra_kwargs={"patient":{"required":True},"doctor":{"required":True},"fees":{"required":True},"scheduled_date":{"required":True}, "is_panel":{"required":False}, "panel":{"required":False}, "employment_number":{"required":False}}

#     def validate(self, attrs):
#         doctor = attrs.get('doctor')
#         patient = attrs.get('patient')
#         fees = attrs.get('fees')
#         scheduled_date = attrs.get('scheduled_date')
#         is_panel = attrs.get('is_panel')
#         spec_share = attrs.get('spec_share')
#         govt_share = attrs.get('govt_share')
#         hosp_amenity_share = attrs.get('hosp_amenity_share')
#         staff_share = attrs.get('staff_share')
#         total_fees = attrs.get('total_fees')
#         fee = total_fees
#         a_spec_share , a_govt_share , a_hosp_share , a_staff_share = get_department_appointment_shares()
#         if spec_share > 0:
#             spec_percentage = a_spec_share
#             spec_fee = (spec_percentage / 100) * fee
#             spec_fee = (spec_share / 100) * spec_fee
#             total_fees = total_fees - spec_fee
#         if govt_share > 0:
#             govt_percentage = a_govt_share
#             govt_fee = (govt_percentage / 100) * fee
#             govt_fee = (govt_share / 100) * govt_fee
#             total_fees = total_fees - govt_fee
#         if hosp_amenity_share > 0:
#             hosp_percentage = a_hosp_share
#             hosp_fee = (hosp_percentage / 100) * fee
#             hosp_fee = (hosp_amenity_share / 100) * hosp_fee
#             total_fees = total_fees - hosp_fee
#         if staff_share > 0:
#             staff_percentage = a_staff_share
#             staff_fee = (staff_percentage / 100) * fee
#             staff_fee = (staff_share / 100) * staff_fee
#             total_fees = total_fees - staff_fee
#         if math.ceil(total_fees) != math.ceil(fees) and int(total_fees) != int(fees):
#             raise serializers.ValidationError("Invalid Discounted fees")
#         if is_panel == True:
#             panel = attrs.get('panel')
#             employment_number = attrs.get('employment_number')
#             if panel == None or employment_number == None:
#                 raise serializers.ValidationError({'msg':'Enter Panel name and employment number'})
#         if DoctorLeave.objects.filter(leave_start_date__lte=scheduled_date.date(), leave_end_date__gte=scheduled_date.date(), doctor=doctor):
#             raise serializers.ValidationError({'msg':'Doctor is on leave on this date. Choose another date'})
#         if Appointment.objects.filter(doctor=doctor, patient=patient, scheduled_date__date=scheduled_date.date(), status__in=[0, 1,2] , deleted = False).exists():
#             raise serializers.ValidationError({'msg':'This Patient already has an appointment with this doctor on selected date'})
#         if doctor != None:
#             if doctor.is_available == False:
#                 raise serializers.ValidationError({'msg':'Doctor is not available'})
#             if doctor.consultant == False:
#                 raise serializers.ValidationError({'msg':'Doctor is not a consultant. you cannot book appointment with him. choose another doctor'})
#         return super().validate(attrs)
    
#     def get_consumer_number(self, obj):
#         return obj.consumer_number
                
