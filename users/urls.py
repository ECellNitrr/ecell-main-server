from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegistrationAPIView.as_view(), name="sign_up"),
    path('login/', views.LoginAPIView.as_view(), name="sign_in"),
    path('verify_otp/', views.verify_otp, name="verify_otp"),
    path('forgot_password/', views.ForgetPasswordView.as_view(), name="forgot_password"),
    path('change_password/', views.ChangePasswordView.as_view(), name="change_password"),
    path('resend_otp/', views.resend_otp, name="resend_otp"),
    path('change_mail/', views.change_mail, name="change_contact"),
    path('is_user_verified/', views.is_user_verified, name="is_verified"),
    path('check_otp/', views.check_otp, name="check_otp"),
    path('get_user_details/',views.get_user_details, name="get_user_details"),
    path('request_ca_approval/',views.request_ca_approval, name="request_ca_approval"),
]
