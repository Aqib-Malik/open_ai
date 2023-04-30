from django.conf import settings
from django.http import Http404

from rest_framework.response import Response
from rest_framework import pagination
from PIL import Image, ImageDraw, ImageFont, ImageOps
from datetime import datetime, timedelta
from django.core.mail import send_mail,EmailMessage
from Api.models.hospital import Hospital
from Api.models.patient import Patient
from Api.models.appointment import Appointment
from asgiref.sync import async_to_sync
from datetime import datetime
from django.utils import timezone
import math, random
from Api.models.user import User

def generateOTP() :
    digits = "0123456789"
    OTP = ""
    for i in range(6) :
        OTP += digits[math.floor(random.random() * 10)]
    return OTP

# def send_otp(number, otp):
#     number = '92'+ number[1:]
#     params = {
#         'user':'dha.isl',
#         'password':'Dh@i98Acc',
#         'mask':'8016',
#         'to':str(number),
#         'message':'Your O.T.P for Military Hospital is '+str(otp)

#     }
#     url = "https://cp.otp.com.pk/api/quick/message/"
#     r = requests.get(url=url, params=params)
#     if r.status_code == 200:
#         return True
#     else:
#         return False


# https://cp.otp.com.pk/api/quick/message?user=dha.isl&password=Dh@i98Acc&mask=8016&to=923409201671&message=TestMessage
def send_email(message,subject,recipient):
    try:
        send_mail(subject, '', settings.EMAIL_HOST_USER, [recipient], fail_silently=False,html_message=message )
        return True
    except Exception as e:
        print(e)
        return False

def send_email_with_attachment(message,subject,recipient,filename):
    try:
        email = EmailMessage(
        subject, message, settings.EMAIL_HOST_USER, [recipient])
        email.get_connection(True)
        email.attach_file(filename)
        email.send()
        return True
    except Exception as e:
        print("Exception : ", e)
        return False

def verify_hospital(id):
    try:
        Hospital.objects.get(id=id)
    except Hospital.DoesNotExist:
        raise Http404

# def get_tokens_for_user(user, is_patient):
#     refresh = RefreshToken.for_user(user)
#     refresh['isPatient'] = is_patient
#     return {
#         'refresh': str(refresh),
#         'access': str(refresh.access_token),
#     }


def set_access_cookies(response, access_token):
    response.set_cookie(
        key=settings.SIMPLE_JWT['AUTH_ACCESS_COOKIE'],
        value=access_token,
        expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
        secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
        samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
    )



def set_refresh_cookies(response, refresh_token):
    response.set_cookie(
        key=settings.SIMPLE_JWT['AUTH_REFRESH_COOKIE'],
        value=refresh_token,
        expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
        secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
        samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
    )


def unset_cookies(response):
    response.delete_cookie(settings.SIMPLE_JWT['AUTH_ACCESS_COOKIE'])
    response.delete_cookie(settings.SIMPLE_JWT['AUTH_REFRESH_COOKIE'])
    response.delete_cookie(settings.CSRF_COOKIE_NAME)


def combine_role_permissions(roles):
    permissions = {}

    for role in roles:
        role_permissions = role.permissions.all()
        for permission in role_permissions:
            permissions[permission.code_name] = True

    return permissions


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def extract_patient_role(roles):
    patient_role = None
    other_roles = []
    for role in roles:
        if role.code_name == 'pt':
            patient_role = role
        else:
            other_roles.append(role)
    return patient_role, other_roles

def check_user_has_role(user , code_name):
    for role in user.roles.all():
        if role.code_name == code_name:
            return True
    return False

    

class CustomPagination(pagination.PageNumberPagination):
    
    def get_from(self):
        return int((self.page.paginator.per_page * self.page.number) - self.page.paginator.per_page + 1)

    def get_to(self):
        return self.get_from() + int(len(self.page.object_list)) - 1

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'page_number': self.page.number,
            'per_page': self.page.paginator.per_page,
            'from': self.get_from(),
            'to': self.get_to(),
            'results': data
        })
        

# def generate_qr(**kwargs):
#     size = kwargs.pop("size")
#     qr = qrcode.QRCode(box_size=size)
#     data = json.dumps(kwargs)
#     qr.make(data)
#     qr.add_data(data)
#     img = qr.make_image() 
#     return img

# def generate_create_appointment_receipt(data):
#     patient = Patient.objects.get(id=data.get('patient'))
#     doctor = Doctor.objects.get(id=data.get('doctor'))
#     try:
#         procedure = Procedures.objects.get(id=data.get('procedure'))
#         type = procedure.name
#         department = procedure.department.name
#     except :
#         type = 'Appointment'
#         department = doctor.department.name
#     created_by = User.objects.get(id=data['created_by'])
#     created_by = created_by.first_name + " " + created_by.last_name
#     panel = data.get('is_panel')
#     receipt_data = {}
#     receipt_data['hospital_name'] = doctor.user.hospital.name
#     receipt_data['doctor_name'] = doctor.user.full_name
#     receipt_data['patient_name'] = patient.patient_name
#     receipt_data['fee'] = data['fees']
#     receipt_data['mr_number'] = patient.mr_number
#     receipt_data['consumer_number'] = data['consumer_number']
#     receipt_data['type'] = type
#     receipt_data['status'] = 'Paid' if data['is_paid'] == True else 'Unpaid'
#     receipt_data['scheduled_date'] = data['scheduled_date'] if type == 'Appointment' else data['scheduled_time']
#     receipt_data['department'] = department
#     receipt_data['panel'] = panel
#     receipt_data['operator'] = created_by
#     return receipt_data

# def generate_appointment_receipt(data):
#     patient = data.get('patient')
#     doctor = Doctor.objects.get(id=data.get('doctor').get('id'))
#     department = Department.objects.get(id=data['department'])
#     appointment = Appointment.objects.get(id=data['id'])
#     created_by = User.objects.get(id=data['created_by']['id'])
#     appointment_type = data.get('type', None)
#     receipt_data = {}
#     receipt_data['department'] = department.name
#     receipt_data['patient_name'] = patient['patient_name']
#     receipt_data['appointment_type'] = appointment_type
#     receipt_data['fee'] = data['fees']
#     receipt_data['mr_number'] = patient['mr_number']
#     receipt_data['doctor_name'] = doctor.user.full_name
#     receipt_data['consumer_number'] = data['consumer_number']
#     receipt_data['status'] = 'Paid' if data['is_paid'] == True else 'Unpaid'
#     receipt_data['scheduled_date'] = data['scheduled_date'] if appointment_type == 'Appointment' else data['scheduled_time']
#     receipt_data['scheduled_date'] = str(receipt_data['scheduled_date'])
#     receipt_data['created_by'] = created_by.first_name + ' ' + created_by.last_name
#     receipt_data['panel'] = appointment.is_panel
#     if appointment.is_paid:
#         receipt_data['duplicate'] = 'yes'
#     return receipt_data


# def generate_letter_head(appointment, **kwargs):
#     try:
#         from api.serializers.doctor_serializer import DoctorSerializer
#         from api.serializers.patient_serializer import PatientSerializer
#         duplicate = kwargs.get('duplicate')
#         doctor = appointment.doctor
#         patient = appointment.patient
#         doctor_name = doctor.user.first_name + " " + doctor.user.last_name
#         doctor_specialization = doctor.expertise
#         doctor_qualification = doctor.qualification
#         rank_prefix = doctor.rank.name + ', ' + doctor.prefix
        
#         if not doctor_qualification:
#             doctor_qualification = "MBBS FCPS"
#         if not doctor_specialization:
#             doctor_specialization = "Specialization XYZ"
            
        
        
#         doctor_data = doctor_specialization + '\n' + doctor_qualification
        
#         letter_date = str(datetime.now().strftime("%d-%m-%Y"))  
#         patient_name = patient.patient_name
        
#         patient_dob = patient.patient_dob
#         if patient_dob != None:
#             patient_age = str(datetime.today().year - patient_dob.year)
#         else:
#             patient_age = ''
#         bld_group = patient.blood_group
#         mr_num = patient.mr_number
#         data = {}
#         data['duplicate'] = duplicate
#         data['doctor'] = DoctorSerializer(doctor).data
#         data['patient'] = PatientSerializer(patient).data
#         data['letter_date'] = letter_date
#         data['patient_age'] = patient_age
#         data['rank_prefix'] = rank_prefix
#         return data

#     except Exception as e:
#         print(e) 
        
        
        

# def generate_letter_head_1(appointment):
#     try:
#         doctor = appointment.doctor
#         patient = appointment.patient
#         doctor_name = "Dr."
#         doctor_name += doctor.user.first_name + " " + doctor.user.last_name
#         doctor_specialization = doctor.expertise
#         doctor_qualification = doctor.qualification
        
#         if not doctor_qualification:
#             doctor_qualification = "MBBS FCPS"
#         if not doctor_specialization:
#             doctor_specialization = "Specialization XYZ"
        
#         doctor_data = doctor_specialization + '\n' + doctor_qualification
        
#         letter_date = str(datetime.now().strftime("%d-%m-%Y"))  
#         patient_name = patient.patient_name
        
#         patient_dob = patient.patient_dob
#         patient_age = str(datetime.today().year - patient_dob.year)
#         token_number = Appointment.objects.filter(doctor = appointment.doctor, scheduled_date = appointment.scheduled_date, status = 2).count() + 1
        
        
#         qr = generate_qr(doctor_name=doctor_name, patient_name = patient_name, time = str(datetime.now()), size = 9)
        
#         img = Image.open("./media/letter-head2.png")
#         draw = ImageDraw.Draw(img)
#         font = ImageFont.truetype("bahnschrift.ttf", 110)
#         draw.text((208, 128),doctor_name,(0,0,0), font=font)
#         font = ImageFont.truetype("bahnschrift.ttf", 60)
#         draw.multiline_text((208,300), doctor_data,(0,0,0), font=font,spacing=30)
#         font = ImageFont.truetype("arial.ttf", 50)
#         draw.text((1080,3330), letter_date,(0,0,0), font=font,spacing=30)
#         draw.text((410,645), patient_name,(0,0,0), font=font,spacing=30)
#         draw.text((1377,645), patient_age,(0,0,0), font=font,spacing=30)
#         draw.text((1995,645), str(token_number),(0,0,0), font=font,spacing=30)
        
#         img.paste(qr, (2200, 170))  
#         return img
#     except Exception as e:
#         print(e) 
        

# def create_card(data):
#     cnic = data.get('cnic')
#     phone = data.get('phone')
#     relation = data.get('relation')
#     blood_group = data.get('blood_group')
#     issue_date = data.get('issue_date')
#     name = data.get('name')
#     mr_number = data.get('mr_number')
#     profile_image = data.get('profile_image')
#     address = data.get('address')
#     if address == None:
#         address = ""
#     phone = data.get('phone')
#     nok_phone = data.get('nok_phone')
#     mr_number = data.get('mr_number')


#     mobile_start = phone[:4]+'-'
#     mobile_end = phone[4:]
#     qr = generate_qr(mr_number = mr_number,size = 4)
#     profile_img = Image.open(profile_image)
#     profile_img = profile_img.resize((250, 277))
#     img = Image.open("./media/patient1.png")
#     draw = ImageDraw.Draw(img)
#     fontforName = ImageFont.truetype("bahnschrift.ttf", 45)
#     font = ImageFont.truetype("bahnschrift.ttf", 25)
#     fontforMr = ImageFont.truetype("bahnschrift.ttf", 17)
#     draw.text((323,127), name,(0,0,0), font=fontforName,spacing=30, stroke_width=0, stroke_fill="black")
#     draw.text((420,200), cnic,(0,0,0), font=font,spacing=30, stroke_width=0, stroke_fill="black")
#     draw.text((328,310), mobile_start,(0,0,0), font=font,spacing=30, stroke_width=0, stroke_fill="black")
#     draw.text((328,340), mobile_end,(0,0,0), font=font,spacing=30, stroke_width=0, stroke_fill="black")
#     draw.text((500,310), relation,(0,0,0), font=font,spacing=30, stroke_width=0, stroke_fill="black")
#     draw.text((654,315), "MR- "+mr_number,(103,30,18), font=fontforMr,spacing=30, stroke_width=0, stroke_fill="black")
#     draw.text((498,425), issue_date,(0,0,0), font=font,spacing=30, stroke_width=0, stroke_fill="black")
#     draw.text((328,425), blood_group,(0,0,0), font=font,spacing=30, stroke_width=0, stroke_fill="black")
#     img.paste(qr, (640, 330))
#     img.paste(profile_img, (50, 131))
#     font = ImageFont.truetype("arial.ttf", 20)
#     qr = generate_qr(mr_number = mr_number,size = 5)
#     img2 = Image.open("./media/patient2.png")
#     draw = ImageDraw.Draw(img2)
#     font = ImageFont.truetype("bahnschrift.ttf", 25)
#     if len(address) >40:
#         address1 = address[:40]
#         address2 = address[40:]
#         draw.text((50,350), address1+'-',(0,0,0), font=font,spacing=30)
#         draw.text((50,373), address2,(0,0,0), font=font,spacing=30)
#     else:
#         draw.text((50,350), address,(0,0,0), font=font,spacing=30)
#     draw.text((50,440), phone,(0,0,0), font=font,spacing=30, stroke_width=0, stroke_fill="black")
#     draw.text((273,440), nok_phone,(0,0,0), font=font,spacing=30, stroke_width=0, stroke_fill="black")
#     draw.text((630,304), "MR- "+mr_number,(103,30,18), font=fontforMr,spacing=30, stroke_width=0, stroke_fill="black")
#     img2.paste(qr, (600, 318))
#     font = ImageFont.truetype("arial.ttf", 20)
#     return img, img2


# def generate_topup_receipt(data):
#     patient = Patient.objects.get(id=data.get('patient'))
#     type = 'Account Recharge'
#     receipt_data = {}
#     receipt_data['patient_name'] = patient.patient_name
#     receipt_data['fee'] = data['fees']
#     receipt_data['mr_number'] = patient.mr_number
#     receipt_data['consumer_number'] = data['consumer_number']
#     receipt_data['type'] = type
#     receipt_data['status'] = 'Paid' if data['status'] == 1 else 'Unpaid'
#     return receipt_data
        

# def get_department_appointment_shares():
#     spec_share = 51
#     govt_share = 15
#     hosp_share = 28
#     staff_share = 6
#     return spec_share , govt_share , hosp_share , staff_share

# def get_indoor_consultation_share(department=None):
#     if department == 'Oncology' or department == 'Radiation Oncology':
#         spec_share = 35
#         govt_share = 20
#         hosp_share = 33
#         staff_share = 12
#     else:
#         spec_share = 39
#         govt_share = 15
#         hosp_share = 38
#         staff_share = 8
#     return spec_share , govt_share , hosp_share , staff_share

# def get_department_procedure_shares(treatment):
#     percentage_spec_share = treatment.procedure.department.spec_share
#     percentage_govt_share = treatment.procedure.department.govt_share
#     percentage_hosp_amenity_share = treatment.procedure.department.hosp_amenity_share
#     percentage_staff_share = treatment.procedure.department.staff_share

#     spec_share_val = (treatment.procedure_fee * percentage_spec_share ) / 100
#     spec_share_percentage = 100 - treatment.spec_share
#     spec_share = (spec_share_val * spec_share_percentage ) / 100
    
#     hosp_share_val = (treatment.procedure_fee * percentage_hosp_amenity_share ) / 100
#     hosp_share_percentage = 100 - treatment.hosp_amenity_share
#     hosp_share = (hosp_share_val * hosp_share_percentage ) / 100

#     staff_share_val = (treatment.procedure_fee * percentage_staff_share ) / 100
#     staff_share_percentage = 100 - treatment.staff_share
#     staff_share = (staff_share_val * staff_share_percentage ) / 100

#     govt_share_val = (treatment.procedure_fee * percentage_govt_share ) / 100
#     govt_share_percentage = 100 - treatment.govt_share
#     govt_share = (govt_share_val * govt_share_percentage ) / 100

#     return spec_share , govt_share , hosp_share , staff_share

# def get_indoor_visit_amount(doc):
#     spec_share , govt_share , hosp_share , staff_share = get_indoor_consultation_share()
#     if doc.department.hospital.hospital_type == 0 or doc.department.hospital.hospital_type == 1:
#         total_amount = 0
#         if doc.doctor_type == 0:
#             total_amount = 500
#         else:
#             total_amount = 300
#         spec_share_visit =  (total_amount * spec_share) / 100 
#         govt_share_visit =  (total_amount * govt_share) / 100 
#         hosp_share_visit =  (total_amount * hosp_share) / 100 
#         staff_share_visit =  (total_amount * staff_share) / 100
#     elif doc.department.hospital.hospital_type == 2:
#         total_amount = 0
#         if doc.doctor_type == 0:
#             total_amount = 350
#         else:
#             total_amount = 250
#         spec_share_visit =  (total_amount * spec_share) / 100 
#         govt_share_visit =  (total_amount * govt_share) / 100 
#         hosp_share_visit =  (total_amount * hosp_share) / 100 
#         staff_share_visit =  (total_amount * staff_share) / 100
#     else:
#         total_amount = 0
#         if doc.doctor_type == 0:
#             total_amount = 250
#         else:
#             total_amount = 150
#         spec_share_visit =  (total_amount * spec_share) / 100 
#         govt_share_visit =  (total_amount * govt_share) / 100 
#         hosp_share_visit =  (total_amount * hosp_share) / 100 
#         staff_share_visit =  (total_amount * staff_share) / 100

#     return spec_share_visit , govt_share_visit , hosp_share_visit , staff_share_visit

# def create_notification(user, title, description):
#     notification = Notification.objects.create(user=user, title=title, description=description)
#     return notification

# def send_notification(user, msg, description):
#     channel_layer = get_channel_layer()
#     for i in user:
#         create_notification(i, title=msg, description=description)
#         async_to_sync(channel_layer.group_send)(
#             str(i.pk),  # Channel Name, Should always be string
#             {
#                 "type": "notify",   # Custom Function written in the consumers.py
#                 "text": msg,
#                 "user_id":i.pk,
#                 "description":description
#             },
#         )          
# from api.models import Doctor
# def getDoctorPoolingShare(docID, month = None):
#     from api.serializers import DoctorDashboardSerializer
#     month = timezone.now().date().month
#     prev_month = timezone.now().date().month - 1
#     doc = Doctor.objects.get(user__id = docID)
#     doctors = Doctor.objects.filter(user__hospital=doc.user.hospital, department = doc.department)
#     previous_month_pooling_data = DoctorDashboardSerializer(doctors, many=True, context = {"month":prev_month}).data
#     current_month_pooling_data = DoctorDashboardSerializer(doctors, many=True, context = {"month":month}).data
#     doc_revenue_pooling_data = DoctorDashboardSerializer(doctors, many=True, context = {"month":None}).data
    
#     # prev month
#     finalDepReports = []
#     for dep in previous_month_pooling_data:
#         finalDepReports.append({
#         'user' : dep.get('user'),
#         'revenue' : dep.get('revenue'),
#         'rankPoints' : dep.get('rankPoints'),
#         'IncentivePoints' : dep.get('IncentivePoints'),
#         'totalPoints' : int(dep.get('rankPoints')) + int(dep.get('IncentivePoints'))
#         })
#     totalRevenue = 0
#     totalPoints = 0
#     for res in finalDepReports:
#         totalPoints += res['totalPoints']
#         totalRevenue += res['revenue']
    
#     rsPerPoint = float(totalRevenue /  totalPoints) 
#     for res in finalDepReports:
#         res['finalRevenue'] = int(rsPerPoint * res['totalPoints'])
#     doc_pooling_share_prev_month = next((item for item in finalDepReports if item['user'] == docID), None)

#     # current month
#     finalDepReports2 = []
#     for dep in current_month_pooling_data:
#         finalDepReports2.append({
#         'user' : dep.get('user'),
#         'revenue' : dep.get('revenue'),
#         'rankPoints' : dep.get('rankPoints'),
#         'IncentivePoints' : dep.get('IncentivePoints'),
#         'totalPoints' : int(dep.get('rankPoints')) + int(dep.get('IncentivePoints'))
#         })
#     totalRevenue2 = 0
#     totalPoints2 = 0
#     for res in finalDepReports2:
#         totalRevenue2 += res['revenue']
#         totalPoints2 += res['totalPoints']
    
#     rsPerPoint2 = float(totalRevenue2 /  totalPoints2) 
#     for res in finalDepReports2:
#         res['finalRevenue'] = int(rsPerPoint2 * res['totalPoints'])
#     doc_pooling_share_current_month = next((item for item in finalDepReports2 if item['user'] == docID), None)

#     # Doc revenue
#     finalDepReports3 = []
#     for dep in doc_revenue_pooling_data:
#         finalDepReports3.append({
#         'user' : dep.get('user'),
#         'revenue' : dep.get('revenue'),
#         'rankPoints' : dep.get('rankPoints'),
#         'IncentivePoints' : dep.get('IncentivePoints'),
#         'totalPoints' : int(dep.get('rankPoints')) + int(dep.get('IncentivePoints'))
#         })
#     totalRevenue3 = 0
#     totalPoints3 = 0
#     for res in finalDepReports3:
#         totalRevenue3 += res['revenue']
#         totalPoints3 += res['totalPoints']
    
#     rsPerPoint3 = float(totalRevenue3 /  totalPoints3) 

#     for res in finalDepReports3:
#         res['finalRevenue'] = int(rsPerPoint3 * res['totalPoints'])
#     doc_pooling_share_doc_revenue = next((item for item in finalDepReports3 if item['user'] == docID), None)
#     return doc_pooling_share_prev_month['finalRevenue'] , doc_pooling_share_current_month['finalRevenue'] , doc_pooling_share_doc_revenue['finalRevenue']


# def get_appointment_share_percentages():
#     spec_share_percentage = 51
#     govt_share_percentage = 15
#     hosp_share_percentage = 28
#     staff_share_percentage = 6
#     return {
#         'spec' : spec_share_percentage,
#         'govt' : govt_share_percentage,
#         'hosp' : hosp_share_percentage,
#         'staff' : staff_share_percentage
#     }


# def get_doctor_appointment_shares(appointment):
#     spec_share_percentage = 51
#     govt_share_percentage = 15
#     hosp_share_percentage = 28
#     staff_share_percentage = 6
#     fees = appointment.fees
#     if appointment.spec_share > 0 or appointment.govt_share > 0 or appointment.hosp_amenity_share > 0 or appointment.staff_share > 0:
#         total_fee = appointment.total_fees
#         spec_share_val = (total_fee * spec_share_percentage ) / 100
#         spec_share_percentage = 100 - appointment.spec_share
#         spec_share = (spec_share_val * spec_share_percentage ) / 100

#         hosp_share_val = (total_fee * hosp_share_percentage ) / 100
#         hosp_share_percentage = 100 - appointment.hosp_amenity_share
#         hosp_share = (hosp_share_val * hosp_share_percentage ) / 100

#         staff_share_val = (total_fee * staff_share_percentage ) / 100
#         staff_share_percentage = 100 - appointment.staff_share
#         staff_share = (staff_share_val * staff_share_percentage ) / 100

#         govt_share_val = (total_fee * govt_share_percentage ) / 100
#         govt_share_percentage = 100 - appointment.govt_share
#         govt_share = (govt_share_val * govt_share_percentage ) / 100

#     else:
#         spec_share = (spec_share_percentage * fees) / 100
#         govt_share = (govt_share_percentage * fees) / 100
#         hosp_share = (hosp_share_percentage * fees) / 100
#         staff_share = (staff_share_percentage * fees) / 100
#     return spec_share , govt_share , hosp_share , staff_share

# def get_indoor_consultation_shares(visit):
#     if visit.doctor.department.name == 'Oncology':
#         spec_share_percentage = 35
#         govt_share_percentage = 20
#         hosp_share_percentage = 33
#         staff_share_percentage = 12
#     else:
#         spec_share_percentage = 39
#         govt_share_percentage = 15
#         hosp_share_percentage = 38
#         staff_share_percentage = 8
#     fees = visit.visit_fee
#     spec_share = (spec_share_percentage * fees) / 100
#     govt_share = (govt_share_percentage * fees) / 100
#     hosp_share = (hosp_share_percentage * fees) / 100
#     staff_share = (staff_share_percentage * fees) / 100
#     return spec_share , govt_share , hosp_share , staff_share

def get_doctor_procedure_shares(procedure):
    if procedure.doctor != None:
        percentage_spec_share = procedure.doctor.department.spec_share
        percentage_govt_share = procedure.doctor.department.govt_share
        percentage_hosp_amenity_share = procedure.doctor.department.hosp_amenity_share
        percentage_staff_share = procedure.doctor.department.staff_share
    else:
        percentage_spec_share = procedure.procedure.department.spec_share
        percentage_govt_share = procedure.procedure.department.govt_share
        percentage_hosp_amenity_share = procedure.procedure.department.hosp_amenity_share
        percentage_staff_share = procedure.procedure.department.staff_share

    spec_share_val = (procedure.procedure_fee * percentage_spec_share ) / 100
    spec_share_percentage = 100 - procedure.spec_share
    spec_share = (spec_share_val * spec_share_percentage ) / 100
    
    hosp_share_val = (procedure.procedure_fee * percentage_hosp_amenity_share ) / 100
    hosp_share_percentage = 100 - procedure.hosp_amenity_share
    hosp_share = (hosp_share_val * hosp_share_percentage ) / 100

    staff_share_val = (procedure.procedure_fee * percentage_staff_share ) / 100
    staff_share_percentage = 100 - procedure.staff_share
    staff_share = (staff_share_val * staff_share_percentage ) / 100

    govt_share_val = (procedure.procedure_fee * percentage_govt_share ) / 100
    govt_share_percentage = 100 - procedure.govt_share
    govt_share = (govt_share_val * govt_share_percentage ) / 100

    return spec_share , govt_share , hosp_share , staff_share

def get_doctor_procedure_shares_indoor(procedure):
    if procedure.doctor != None:
        percentage_spec_share = procedure.doctor.department.spec_share_indoor
        percentage_govt_share = procedure.doctor.department.govt_share_indoor
        percentage_hosp_amenity_share = procedure.doctor.department.hosp_amenity_share_indoor
        percentage_staff_share = procedure.doctor.department.staff_share_indoor
    else:
        percentage_spec_share = procedure.procedure.department.spec_share_indoor
        percentage_govt_share = procedure.procedure.department.govt_share_indoor
        percentage_hosp_amenity_share = procedure.procedure.department.hosp_amenity_share_indoor
        percentage_staff_share = procedure.procedure.department.staff_share_indoor

    spec_share_val = (procedure.procedure_fee * percentage_spec_share ) / 100
    spec_share_percentage = 100 - procedure.spec_share
    spec_share = (spec_share_val * spec_share_percentage ) / 100
    
    hosp_share_val = (procedure.procedure_fee * percentage_hosp_amenity_share ) / 100
    hosp_share_percentage = 100 - procedure.hosp_amenity_share
    hosp_share = (hosp_share_val * hosp_share_percentage ) / 100

    staff_share_val = (procedure.procedure_fee * percentage_staff_share ) / 100
    staff_share_percentage = 100 - procedure.staff_share
    staff_share = (staff_share_val * staff_share_percentage ) / 100

    govt_share_val = (procedure.procedure_fee * percentage_govt_share ) / 100
    govt_share_percentage = 100 - procedure.govt_share
    govt_share = (govt_share_val * govt_share_percentage ) / 100

    return spec_share , govt_share , hosp_share , staff_share

# def get_ward_charges_shares(amount):
#     spec_share_percentage = 0
#     govt_share_percentage = 20
#     hosp_share_percentage = 70
#     staff_share_percentage = 10
#     fees = amount
#     spec_share = (spec_share_percentage * fees) / 100
#     govt_share = (govt_share_percentage * fees) / 100
#     hosp_share = (hosp_share_percentage * fees) / 100
#     staff_share = (staff_share_percentage * fees) / 100
#     return spec_share , govt_share , hosp_share , staff_share

# def get_moic_charges_shares(amount):
#     spec_share_percentage = 39
#     govt_share_percentage = 15
#     hosp_share_percentage = 38
#     staff_share_percentage = 8
#     fees = amount
#     spec_share = (spec_share_percentage * fees) / 100
#     govt_share = (govt_share_percentage * fees) / 100
#     hosp_share = (hosp_share_percentage * fees) / 100
#     staff_share = (staff_share_percentage * fees) / 100
#     return spec_share , govt_share , hosp_share , staff_share

def get_ward_charges_shares_percentages():
    spec_share_percentage = 0
    govt_share_percentage = 20
    hosp_share_percentage = 70
    staff_share_percentage = 10
    return spec_share_percentage , govt_share_percentage, hosp_share_percentage,staff_share_percentage

def get_moic_charges_shares_percentages():
    spec_share_percentage = 39
    govt_share_percentage = 15
    hosp_share_percentage = 38
    staff_share_percentage = 8
    return spec_share_percentage , govt_share_percentage , hosp_share_percentage , staff_share_percentage

def get_moic_charges_shares(ward_charge_obj):
    percentage_spec_share = 39
    percentage_govt_share = 15
    percentage_hosp_amenity_share = 38
    percentage_staff_share = 8

    total_moic_charges = ward_charge_obj.ward.moic_charges * ward_charge_obj.days

    moic_spec_share_val = (total_moic_charges * percentage_spec_share ) / 100
    spec_share_percentage = 100 - ward_charge_obj.spec_share
    moic_spec_share = (moic_spec_share_val * spec_share_percentage ) / 100

    moic_govt_share_val = (total_moic_charges * percentage_govt_share ) / 100
    govt_share_percentage = 100 - ward_charge_obj.govt_share
    moic_govt_share = (moic_govt_share_val * govt_share_percentage ) / 100

    moic_hosp_share_val = (total_moic_charges * percentage_hosp_amenity_share ) / 100
    hosp_share_percentage = 100 - ward_charge_obj.hosp_amenity_share
    moic_hosp_share = (moic_hosp_share_val * hosp_share_percentage ) / 100

    moic_staff_share_val = (total_moic_charges * percentage_staff_share ) / 100
    staff_share_percentage = 100 - ward_charge_obj.staff_share
    moic_staff_share = (moic_staff_share_val * staff_share_percentage ) / 100
    return moic_spec_share , moic_govt_share , moic_hosp_share , moic_staff_share

def get_ward_charges_shares(ward_charge_obj):
    percentage_spec_share = 0
    percentage_govt_share = 20
    percentage_hosp_amenity_share = 70
    percentage_staff_share = 10

    total_fees = ward_charge_obj.total_fees
    if total_fees == 0:
        total_fees = ward_charge_obj.amount

    ward_spec_share_val = (total_fees * percentage_spec_share ) / 100
    spec_share_percentage = 100 - ward_charge_obj.spec_share
    ward_spec_share = (ward_spec_share_val * spec_share_percentage ) / 100

    ward_govt_share_val = (total_fees * percentage_govt_share ) / 100
    govt_share_percentage = 100 - ward_charge_obj.govt_share
    ward_govt_share = (ward_govt_share_val * govt_share_percentage ) / 100

    ward_hosp_share_val = (total_fees * percentage_hosp_amenity_share ) / 100
    hosp_share_percentage = 100 - ward_charge_obj.hosp_amenity_share
    ward_hosp_share = (ward_hosp_share_val * hosp_share_percentage ) / 100

    ward_staff_share_val = (total_fees * percentage_staff_share ) / 100
    staff_share_percentage = 100 - ward_charge_obj.staff_share
    ward_staff_share = (ward_staff_share_val * staff_share_percentage ) / 100
    return ward_spec_share , ward_govt_share , ward_hosp_share , ward_staff_share