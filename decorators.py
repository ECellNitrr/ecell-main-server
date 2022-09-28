import jwt
from decouple import config
from users.models import CustomUser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

NO_TOKEN = Response({
                "message":"No Token Provided!"
            }, status=status.HTTP_401_UNAUTHORIZED)

DOES_NOT_EXIST = Response({
                    "message":"User does not exist!"
            }, status=status.HTTP_404_NOT_FOUND)

ACCESS_ERROR = Response({
                    "message": "You are not authorized to use this API"
            }, status=status.HTTP_401_UNAUTHORIZED)
PREFIX = 'Token'

def get_token(header):
    bearer, _, token = header.partition(' ')
    if bearer != PREFIX:
        raise ValueError('Invalid token')

    return token
def ecell_user(function):
    def wrap(request, *args, **kwargs):
        token = request.META.get("HTTP_AUTHORIZATION", None)
        token = get_token(token)
        if token is not None: 
            try:
                payload = Token.objects.get(key=token).user
            except:
                return DOES_NOT_EXIST
            else:
                ecell_user_email = payload.email
                try:
                    ecell_user = CustomUser.objects.get(email=ecell_user_email)
                except:
                    DOES_NOT_EXIST['message'] = 'The account has been deleted or banned'
                    return DOES_NOT_EXIST
                else:
                    request.ecelluser = ecell_user
        else:
            print('no token')
            return NO_TOKEN

        return function(request, *args, **kwargs)
        wrap.__doc__ = function.__doc__
        wrap.__name__ = function.__name__
    return wrap

def client_check(function):
    def wrap(request, *args, **kwargs):
        # print(request.META['Access'])
        token = request.META.get("HTTP_ACCESS", None)
        token = get_token(token)
        # print(token)
        if token is not None: 
            try:
                payload = Token.objects.get(key=token).user
            except Exception as e:
                return ACCESS_ERROR
            else:
                print(payload)
                client = payload.client
                organization = payload.organization
                
                if client!='android' or organization!='ECell':
                    return ACCESS_ERROR
                    
        else:
            print('no toen')
            return NO_TOKEN

        return function(request, *args, **kwargs)
        wrap.__doc__ = function.__doc__
        wrap.__name__ = function.__name__
    return wrap

def get_user(token):
    try:
        payload = Token.objects.get(key=token).user
    except Exception as e:
        return DOES_NOT_EXIST
    else:
        ecell_user_email = payload.email
        ecell_user = CustomUser.objects.get(email=ecell_user_email)
        return ecell_user

def relax_ecell_user(function):
    def wrap(request, *args, **kwargs):

        # hack to make ca portal work
        # authenticate the post request via hidden input field
        token = request.POST.get('token') or request.POST.get('Token')  
        token = request.META.get("HTTP_AUTHORIZATION", None) if not token else token
        token = get_token(token)
        if token is not None: 
            request.ecelluser = get_user(token)

        return function(request, *args, **kwargs)
        wrap.__doc__ = function.__doc__
        wrap.__name__ = function.__name__
    return wrap