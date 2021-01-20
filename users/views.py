from random import randint
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from utils.swagger import set_example
from utils.auth_utils import send_email_otp
from .models import CustomUser
from .serializers import *
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
            # Creating random OTP & saving it in user model.
            otp = str(randint(1000, 9999))
            user = serializer.save(otp)
            # Sending the OTP in a mail.
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
            # Authenticating the user.
            found_email =  serializer.data['email']
            user = authenticate(
                username=serializer.data['email'],
                password=serializer.data['password']
            )    
            if user:
                # Assigning the user, a token if not already assigned and returning it.
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': f"Token {token.key}"}, status.HTTP_202_ACCEPTED)
            else:
                # Trying to check if there exists a user with the email.
                try:
                    if CustomUser.objects.get(email=found_email):
                        return Response({'detail': 'Credentials did not match'}, status.HTTP_401_UNAUTHORIZED)

                except CustomUser.DoesNotExist:
                    return Response({"detail": "User not found"}, status.HTTP_404_NOT_FOUND)
        else:
            # Returning errors in case the email is invalid or empty.
            data = serializer.errors
            return Response(data, status.HTTP_400_BAD_REQUEST)



class ForgetPasswordView(APIView):

    serializer_class = ForgetPasswordSerializer

    @swagger_auto_schema(
        operation_id='forget_password',
        request_body=ForgetPasswordSerializer,
        responses={
            '200': set_example(responses.forget_password_200),
            '400': set_example(responses.forget_password_400),
            '404': set_example(responses.forget_password_404),
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
                user = CustomUser.objects.get(email=valid_data['email'])
            except CustomUser.DoesNotExist:
                return Response(responses.forget_password_404, status.HTTP_404_NOT_FOUND)
            else:
                #Generate OTP
                otp = str(randint(1000, 9999))

                #Update OTP
                user.otp = otp
                user.save()

                #Send OTP
                send_email_otp(recipient_list=[user.email], otp=otp)

                return Response(responses.forget_password_200, status.HTTP_200_OK)

        # If the email entered was invalid or empty.
        else:
            data = serializer.errors
            return Response(data, status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(APIView):

    serializer_class = ChangePasswordSerializer

    @swagger_auto_schema(
        operation_id='change_password',
        request_body=ChangePasswordSerializer,
        responses={
            '200': set_example(responses.change_password_200),
            '400': set_example(responses.change_password_400),
            '404': set_example(responses.change_password_404),
            '401': set_example(responses.change_password_401),
        },
    )

    def post(self, request):
        '''
        Change password API is where the email, otp and password is posted and password is changed
        '''

        serializer = ChangePasswordSerializer(data=request.data)

        #checking if entered data is valid
        if serializer.is_valid():
            valid_data = serializer.validated_data

            # Check if such a user exists.
            try:
                user = CustomUser.objects.get(email=valid_data['email'])
            except CustomUser.DoesNotExist:
                return Response(responses.change_password_404, status.HTTP_404_NOT_FOUND)

            #Checking is vorrect otp is entered
            if valid_data['otp'] == user.otp:

                #Update Password
                user.set_password(valid_data['password'])
                user.save()
                return Response(responses.change_password_200, status.HTTP_200_OK)
            return Response(responses.change_password_401, status.HTTP_401_UNAUTHORIZED)

        data = serializer.errors
        return Response(data, status.HTTP_400_BAD_REQUEST)



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
    '''
    After Signup Login, Verify OTP using this API. 
    '''
    res_status = status.HTTP_400_BAD_REQUEST
    user = request.user
    req_data = request.data
    # No OTP entered 400
    if 'otp' not in req_data:
        message ='Please enter OTP to verify your account'
    # User already Verfied 400
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
@swagger_auto_schema(
    operation_id='check_otp',
    method= 'post',
    request_body= CheckOTPSerializer,
    responses={
        '200': set_example(responses.check_otp_200),
        '400': set_example(responses.check_otp_400),
        '404': set_example(responses.check_otp_404)
    },
)
@api_view(['POST'])
def check_otp(request):
    '''
    After change mail, send request to this API to verify new email id.
    '''
    # As the email changed, verified is set to false in every other case.
    verified = False
    serializer = CheckOTPSerializer(data= request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']
        try:
            user = CustomUser.objects.get(email=email)
        except:
            message = "User account with this email id doesn't exist"
            res_status = status.HTTP_404_NOT_FOUND
        else:
            print(user.verified)
            if user.verified==True:
                message = 'Account already verified'
                res_status = status.HTTP_400_BAD_REQUEST
                verified = True
            elif str(otp)==user.otp:
                verified = True
                message = 'Mail verified'
                user.verified = True
                user.save()
                res_status = status.HTTP_200_OK
            else:
                message = 'Invalid OTP!'
                res_status = status.HTTP_400_BAD_REQUEST
    else:
        message = serializer.errors
        res_status = status.HTTP_400_BAD_REQUEST
    return Response({
        "message":message,
        "verified":verified
    }, status=res_status)




@swagger_auto_schema(
    operation_id='resend_otp',
    method= 'get',
    responses={
        '200': set_example(responses.resend_otp_200),
        '401': set_example(responses.verify_otp_401)
    },
)
@api_view(['get'])
@permission_classes([IsAuthenticated])
def resend_otp(request):
    '''
    Use me if you want to send the OTP again to your email.
    '''
    res_status = status.HTTP_400_BAD_REQUEST
    user = request.user
    otp = user.otp
    email = user.email
    duration = user.last_modified 
    # if not older than 20 minutes (1200 seconds), sending the same OTP
    if duration<=1200 and otp:
        send_email_otp([email], otp=otp)
    else:
        otp = send_email_otp([email])
        user.otp = otp
        user.save()
    message = responses.resend_otp_200
    res_status = status.HTTP_200_OK

    return Response(responses.resend_otp_200, status=res_status)

@swagger_auto_schema(
    operation_id='change_mail',
    method= 'post',
    request_body= ChangeMailSerializer,
    responses={
        '200': set_example(responses.change_mail_200),
        '400': set_example(responses.forget_password_400),
        '401': set_example(responses.verify_otp_401)
    },
)
@api_view(['post'])
@permission_classes([IsAuthenticated])
def change_mail(request):
    '''
    To change the mail of the current authenticated user. OTP Verfication to be done in check_otp. 
    '''
    serializer = ChangeMailSerializer(data=request.data)
    user = request.user

    if serializer.is_valid():
        new_email = serializer.validated_data['email']
        # Changing the OTP and removing the verified status.
        otp = send_email_otp([new_email])
        user.otp = otp
        user.email = new_email
        user.username = new_email
        user.verified = False
        user.save()
        # Verification to be done in check_otp.
        return Response(responses.change_mail_200, status=status.HTTP_200_OK)

    data = serializer.errors
    return Response(data, status.HTTP_400_BAD_REQUEST)
    


@swagger_auto_schema(
    operation_id='is_user_verified',
    method= 'get',
    responses={
        '200': set_example({
                    "verified": False,
                }),
        '401': set_example(responses.verify_otp_401)
    },
)
@api_view(['get'])
@permission_classes([IsAuthenticated])
def is_user_verified(request):
    '''
    An API to check if the current user is verified or not.
    '''
    user = request.user
    verified = user.verified
    res_status = status.HTTP_200_OK

    return Response(
        {
            "verified":verified,
        }, 
        status=res_status
    )



@swagger_auto_schema(
    operation_id='apply_for_ca',
    method= 'get',
    responses={
        '200': set_example(responses.apply_for_ca_200),
        '401': set_example(responses.verify_otp_401),

    },
)
@api_view(['get'])
@permission_classes([IsAuthenticated])
def request_ca_approval(request):
    '''
    API for current user to apply for Campus Ambassador program.
    '''
    user = request.user
    if user.applied == True:
        return Response({'message':'Already applied!'}, status.HTTP_200_OK)
    user.applied = True
    user.save()
    res_status = status.HTTP_200_OK
    return Response({"message":"Congratulations! Applied for CA successfully."}, status=res_status)



@swagger_auto_schema(
    operation_id='get_user_details',
    method= 'get',
    responses={
        '200': set_example(responses.get_user_details_200),
        '401': set_example(responses.verify_otp_401)
    },
)
@api_view(['get'])
@permission_classes([IsAuthenticated])
def get_user_details(request):
    '''
    API to fetch the details of the current authenticated user.
    '''
    user = request.user
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
