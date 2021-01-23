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
  "detail": [
      "Authentication credentials were not provided.",
      "Invalid token."
  ]
}

get_user_details_200 = {
  "first_name": "Sahil",
  "last_name": "Silare",
  "email": "sahil@gmail.com",
  "verified": False,
  "contact": "",
  "bquiz_score": 0,
  "user_type": "GST",
  "linkedin": "https://www.linkedin.com/in/anshsrtv",
  "facebook": "https://www.facebook.com/ansh.srivastava.77/",
  "applied": True,
  "id": 1
}

resend_otp_200 = {
    "message": "An otp has been sent to your mail id."
}

change_mail_200= {
    "message": "An otp has been sent to new mail id"
}

check_otp_400 = {
  "message": {
    "email": [
      "Enter a valid email address.",
      "Email field is required.",
      "User account with this email id doesn't exist"
    ],
    "otp": [
      "Ensure this field has no more than 4 characters.",
      "Ensure this field has at least 4 characters."
      "Invalid OTP!"
    ]
  },
  "verified": False
}

check_otp_404 = {
    "message": "User account with this email id doesn't exist",
    "verified": False
}

check_otp_200 = {
    "message":[
        "Mail verified",
        "Account already verified"
    ],
    "verified": True
}

apply_for_ca_200 = {
    "message": [
        "Congratulations! Applied for CA successfully.",
        "Already applied!"
    ]
}
forget_password_200 = {
    "detail": "An OTP has been sent to your email."
}

forget_password_400 = {
  "email": [
    "Enter a valid email address.",
    "This field is required."
  ]
}

forget_password_404 = {
    "detail": "User does not exist."
}

change_password_200 = {
    "detail": "Password changed successfully"
}

change_password_400 = {
  "email": [
    "Enter a valid email address.",
    "This field is required."
  ],
  "otp": [
      "OTP field is required.",
  ],
  "password": [
      "Password cannot be empty.",
      "Password must be atleast 8 characters."
  ]
}

change_password_404 = {
    "detail": "Account with this email id doesn't exists. Kindly signup."
}

change_password_401 = {
    "detail": "Invalid otp"
}
