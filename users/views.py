from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegistrationSerializer, LoginSerializer, VerifyOTPSerializer
from utils.auth_utils import send_otp, send_email_otp
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from decorators import ecell_user, client_check
from random import randint
from .models import CustomUser
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from drf_yasg.utils import swagger_auto_schema
from utils.swagger import set_example
from . import responses

class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    
    @swagger_auto_schema(
        operation_id='create_user',
        request_body=RegistrationSerializer,
        responses={
            '201': set_example({}),
            '400': set_example(responses.user_registration_400)
        },
    )
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            otp = str(randint(1000, 9999))
            user = serializer.save(otp)
            send_email_otp(recipient_list=[user.email], otp=otp)
            return Response({}, status.HTTP_201_CREATED)
        else:
            data = serializer.errors
            return Response(data, status.HTTP_400_BAD_REQUEST)



class LoginAPIView(APIView):
    serializer_class = LoginSerializer

    @swagger_auto_schema(
        operation_id='login_user',
        request_body=LoginSerializer,
        responses={
            '202': set_example(responses.login_202),
            '400': set_example(responses.login_400),
            '401': set_example(responses.login_401),
            '404': set_example(responses.login_404)
        },
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            found_email =  serializer.data['email']
            user = authenticate(
                username=serializer.data['email'],
                password=serializer.data['password']
            )    
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': f"Token {token.key}"}, status.HTTP_202_ACCEPTED)
            else:
                try:
                    if CustomUser.objects.get(email=found_email):
                        return Response({'detail': 'Credentials did not match'}, status.HTTP_401_UNAUTHORIZED)
                    
                except CustomUser.DoesNotExist:
                    return Response({"detail": "User not found"}, status.HTTP_404_NOT_FOUND)     
        else:
            data = serializer.errors
            return Response(data, status.HTTP_400_BAD_REQUEST)



class ForgetPasswordView(APIView):
    @swagger_auto_schema(
        operation_id='forget_password',
        request_body=ForgetPasswordSerializer,
        responses={
            '200': set_example(responses.forget_password_200),
            '400': set_example(responses.forget_password_400),
            '404': set_example(responses.login_404),
        },
    )
    def post(self, request):
        """
        Forgot Password API where the email is posted and OTP is sent to the user.
        """

        serializer = ForgetPasswordSerializer(data=request.data)

        # Checking if the email entered is valid.
        if serializer.is_valid():
            valid_data = serializer.validated_data

            # Check if such a user exists.
            try:
                user = User.objects.get(email=valid_data['email'])
            except User.DoesNotExist:
                return Response("Account with this email id doesn't exists. Kindly signup.", status.HTTP_404_NOT_FOUND)
            else:
                # Setting Variables to check the time lapse.
                time_now = datetime.datetime.now()
                otp_created_at = user.otp_created_at
                one_hour = datetime.timedelta(hours = 1)

                # Mail Variables
                subject = 'OTP to Reset your Password'
                body = "Dear user,</br></br>\
                <b>The OTP to reset your password is {}</b>.</br>\
                Please do not share it with anyone.</br>\
                </br>\
                Best Regards,</br>\
                Teesco (Volunteer Management System)"

                # Check if OTP was ever generated for this user.
                if user.otp == None:
                    self.generate_otp(user)
                    print(user.otp) #printing the otp in the terminal for now. we will integrate once we get a provider

                # Check if the time lapse is greater than 1 hour.
                elif time_now-otp_created_at.replace(tzinfo=None)>one_hour:
                    self.generate_otp(user)
                    print(user.otp) #printing the otp in the terminal for now. we will integrate once we get a provider

                else:
                    print(user.otp) #printing the otp in the terminal for now. we will integrate once we get a provider

                return Response("An otp has been sent to your mobile no to reset your password", status.HTTP_200_OK)

        # If the email entered was invalid or empty.
        else:
            data = serializer.errors
            return Response(data, status.HTTP_400_BAD_REQUEST)

    def generate_otp(self, user):
        """
        Method to generate OTPs and save it in OTP field.
        """
        user.otp = get_random_string(5, allowed_chars='0123456789')
        user.otp_created_at = timezone.now()
        user.save()

@api_view(['POST'])
@client_check    #to be seen
def forgot_password(request):
    res_status = status.HTTP_400_BAD_REQUEST
    req_data = request.data
    email = req_data['email']
    print(email)
    try:
        user = CustomUser.objects.get(email=email)
        print(user)
    except:
        message = "Account with this email id doesn't exists. Kindly signup."
    else:
        email = user.email
        otp = send_email_otp([email])
        user.otp = otp
        user.save()
        message = "An otp has been sent to your mobile no to reset your password"
        res_status = status.HTTP_200_OK

    return Response({
            "message": message,
        }, status=res_status)

@swagger_auto_schema(
    operation_id='verify_otp',
    request_body=VerifyOTPSerializer,
    method='post',
    responses={
        '200': set_example(responses.verify_otp_200),
        '400': set_example(responses.verify_otp_400),
        '401': set_example(responses.verify_otp_401),
    },
)
@api_view(['POST',])
@permission_classes([IsAuthenticated])
def verify_otp(request):
    res_status = status.HTTP_400_BAD_REQUEST
    user = request.user
    req_data = request.data

    if 'otp' not in req_data:
        message ='Please enter OTP to verify your account'
    elif user.verified==True:
        message = 'Account already verified'
    else:
        otp = req_data['otp']
        if str(otp)==user.otp:
            user.verified=True
            user.save()
            message = 'Account verified successfully'
            res_status = status.HTTP_200_OK
        else:
            message = 'Invalid OTP'

    return Response({
            "message": message,
        }, status=res_status)
    
    
# TODO: write unittests
@api_view(['POST'])
@client_check
def check_otp(request):
    res_status = status.HTTP_400_BAD_REQUEST
    req_data = request.data 
    verified = False
    email = req_data['email']
    otp = req_data['otp']
    try:
        user = CustomUser.objects.get(email=email)
    except:
        message = "User account with this email id doesn't exist"
    else:
        user_otp = user.otp
        if str(otp)==user_otp:
            verified = True
            message = 'Otp verified'
            res_status = status.HTTP_200_OK
        else:
            message = 'Invlaid Otp'
    return Response({
        "message":message,
        "verified":verified
    }, status=res_status)



@api_view(['POST'])
@client_check
def change_password(request):
    res_status = status.HTTP_400_BAD_REQUEST
    req_data = request.data
    email = req_data['email']
    otp = req_data['otp']
    password = req_data['password']
    try:
        user = CustomUser.objects.get(email=email)
    except:
        message = "Account with this email id doesn't exists. Kindly signup."
    else:
        user_otp = user.otp
        if str(otp)==user_otp:
            user.set_password(password)
            user.save()
            message = 'Password changed successfully'
            res_status = status.HTTP_200_OK
        else:
            message = 'Invalid otp'
            
    return Response({
            "message": message,
        }, status=res_status)

# TODO: remove all the instance of ecell_user and relaxed_ecell_user with teesco style auth
# TODO: remove /decorators.py after convertion to teesco style auth 
@api_view(['GET'])
@ecell_user
def resend_otp(request):
    res_status = status.HTTP_400_BAD_REQUEST
    user = request.ecelluser
    otp = user.otp
    email = user.email
    if otp:
        duration = user.last_modified
        if duration<=1200:
            otp = send_email_otp([email], otp=otp)
        else:
            otp = send_email_otp([email])
            user.otp = otp
            user.save()
        message = "An otp has been sent to your mobile no to reset your password"
        res_status = status.HTTP_200_OK

    return Response({
            "message": message,
        }, status=res_status)

# TODO: remove ecell_user and client_check
@api_view(['POST'])
@ecell_user
@client_check
def change_contact(request):
    res_status = status.HTTP_400_BAD_REQUEST
    req_data = request.data
    new_email = req_data['email']
    user = request.ecelluser
    otp = send_email_otp([new_email])
    user.otp = otp
    user.email = new_email
    user.verified = False
    user.save()
    message = "An otp has been sent to new mobile no."
    res_status = status.HTTP_200_OK
    return Response({
            "message": message,
        }, status=res_status)
    
# TODO: remove ecell_user and client_check and use teesco auth
@api_view(['GET'])
@ecell_user
@client_check
def is_user_verified(request):
    user = request.ecelluser
    verified = user.verified
    res_status = status.HTTP_200_OK
    return Response({
        "verified":verified,
    }, status=res_status)



# TODO: remove ecell_user and client_check and use teesco auth
@api_view(['GET'])
@ecell_user
def request_ca_approval(request):
    res_status = status.HTTP_400_BAD_REQUEST
    user = request.ecelluser
    user.applied = True
    user.save()
    message = "Congradulations. Applied for CA successfully"
    res_status = status.HTTP_200_OK
    return Response({
            "message": message,
        }, status=res_status)



# TODO: remove ecell_user and client_check and use teesco auth
@api_view(['GET'])
@ecell_user
def get_user_details(request):
    res_status = status.HTTP_400_BAD_REQUEST
    user = request.ecelluser
    
    res_status = status.HTTP_200_OK
    return Response({
        'first_name' : user.first_name,
        'last_name' : user.last_name,
        'email' : user.email,
        'verified' : user.verified,
        'contact' : user.contact,
        'bquiz_score' : user.bquiz_score,
        'user_type' : user.user_type,
        'linkedin' : user.linkedin,
        'facebook' : user.facebook,
        'applied' : user.applied,
        'id': user.id
    }, status=res_status)
