user_registration_400 = {
    "email": [
        "This field may not be blank.",
        "Kindly enter a Valid Email Address",
        "This email is already registered with us.",
    ],
    "first_name": [
        "Name field is required.",
        "This field may not be blank."
    ],
    "password": [
        "Password cannot be empty.",
        "Password must be atleast 8 characters.",
    ],
    "last_name": [
        "This field may not be blank."
    ],
    "contact": [
        "This field may not be blank."
    ],
}

login_401 = {
    "detail": "Credentials did not match"
}

login_400 = {
    "email": [
        "This field is required.",
        "Enter a valid email address."
    ],
    "password": [
        "This field is required."
    ]
}

login_404 = {
    "detail": "User not found"
}

login_202 = {
    "token": "Token 9935a8b04f2de7f5dec8f9e92a1893822b034dc7"
}

verify_otp_200 = {
  "message": "Account verified successfully"
}

verify_otp_400 = {
  "message": [
      "Please enter OTP to verify your account",
      "Account already verified",
      "Invalid OTP"
  ],
}

verify_otp_401 = {
  "detail": "Authentication credentials were not provided."
}

forget_password_200 = {
    'detail': 'An OTP has been sent to your email.'
}

forget_password_400 = {
  "email": [
    "Enter a valid email address.",
    "This field is required."
  ]
}

forget_password_404 = {
    'detail': 'User does not exist.'
}

change_password_200 = {
    'detail': 'Password changed successfully'
}

change_password_400 = {
  "email": [
    "Enter a valid email address.",
    "This field is required."
  ]
}

change_password_404 = {
    'detail': "Account with this email id doesn't exists. Kindly signup."
}

change_password_401 = {
    'detail': 'Invalid otp'
}