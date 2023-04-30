from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.db import transaction
from Api.models import Role, User, Patient
from Api.util import extract_patient_role
from django.db import IntegrityError

class PatientRegistrationView(APIView):

    permission_classes = (AllowAny, )

    def post(self, request, format=None):
        try:
            data = request.data
            email = data.get('email', None)
            first_name = data.get('first_name', None)
            last_name = data.get('last_name', None)
            dob = data.get('dob', None)
            blood_group = data.get('blood_group', None)
            cnic = data.get('cnic', None)
            mobile = data.get('mobile', None)
            next_of_kin_name = data.get('next_of_kin_name', None)
            next_of_kin_mobile = data.get('next_of_kin_mobile', None)
            password = data.get('password', None)
            gender = data.get('gender', None)
            profile_image = data.get('profile_image', None)
            if not first_name or not last_name or not cnic or not password:
                return Response({'msg': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():
                try:
                    user = User.objects.get(cnic=cnic)
                    role, roles = extract_patient_role(user.roles.all())
                    if role:
                        return Response({'msg': 'Patient with this cnic already exists'}, status=status.HTTP_400_BAD_REQUEST)
                except User.DoesNotExist:
                    user = None

                if not user:
                    user = User.objects.create_user(username=cnic, email=email, first_name=first_name, last_name=last_name, cnic=cnic, password=password)
                if gender != None:
                    user.gender = gender
                if dob != None:
                    user.dob = dob
                if next_of_kin_name != None:
                    user.next_of_kin_name = next_of_kin_name
                if next_of_kin_mobile != None:
                    user.next_of_kin_mobile = next_of_kin_mobile
                if profile_image:
                    user.profile_image = profile_image
                if mobile != None:
                    user.mobile = mobile

                user.save()

                role = Role.objects.get(code_name='pt')
                user.roles.add(role)

                user.save()
                patient = Patient.objects.create(patient_name=first_name+' '+last_name, blood_group=blood_group, relation='Self', user=user, created_by=user)
                if profile_image:
                    patient.profile_image = profile_image
                if dob != None:
                    patient.patient_dob = dob
                if gender != None:
                    patient.gender = gender
                patient.save()
            hosp_name = ''
            if hasattr(request.user, 'hospital'):
                hosp_name = request.user.hospital.name
            data = {'name':first_name+' '+last_name,
            'mr_number':patient.mr_number,
            'cnic':cnic,
            'hospital_name': hosp_name,
            'type':'Registeration'}
            
            return Response({'msg': 'Patient sign-up successfully', 'data':data}, status=status.HTTP_200_OK)
        except IntegrityError as e:
            if 'UNIQUE constraint failed: api_user.mobile' in e.args:
                return Response({'msg':'User with this mobile number already exists'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'msg': 'Integrity Error'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'msg': 'Server error'}, status=status.HTTP_400_BAD_REQUEST)
