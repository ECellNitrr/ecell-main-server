from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegistrationSerializer, LoginSerializer
from utils.auth_utils import send_otp, send_email_otp
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from decorators import ecell_user, client_check
from random import randint
from .models import CustomUser
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    
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

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            found_email =  serializer.data['email']
            print(serializer.data)
            user = authenticate(
                username=serializer.data['email'],
                password=serializer.data['password']
            )    
            print(user)
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



@api_view(['POST'])
@client_check
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


@api_view(['POST',])
@permission_classes([IsAuthenticated])
def verify_otp(request):
    res_status = status.HTTP_400_BAD_REQUEST
    user = request.user
    req_data = request.data

    if 'otp' not in req_data:
        message ='Please enter otp to verify your account'
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
            message = 'Invalid otp'

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
