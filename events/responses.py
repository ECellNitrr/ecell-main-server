get_events_200 ={
  "message": "Events Fetched successfully.",
  "data": [
    {
    "id":0,
    "name": "test",
    "venue" : "test_venue",
    "date" : "2020-09-29T15:21:48.828+00:00",
    "time" : "test_time",
    "details": "test_details",
    "details_html" : "test.html",
    "cover_pic" : "test_cover.jpeg",
    "icon" : "test_icon.png",
    "email": "test@email.com",
    "flag" :True,
    "year" :2019,
    "ecell_user" :3,
    "created_at":"2020-09-29T15:21:48.828+00:00",
    "modified_at":"2020-09-29T15:21:48.828+00:00"
    }
  ]
}

events_not_found_404 = {
    "message": "Events couldn't be fetched."
}

event_registration_201 = {
    "message":"Registration Successful"
}

event_does_not_exist_404 = {
  "message": "Registration Failed. Event does not exist."
}

user_unauthorized_401 = {
  "message":"Please follow OTP verification before registering"
}

user_already_registered_event_200 = {
  "message":"You've already registered"
}

event_registration_deleted_200 = {
  "message" : "Event unregistered successfully"
}