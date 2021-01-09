# EcellWeb2k20

**(nice EcellWeb2k19 is very cluttered with old builds and huge repo size this repo is created)**
API for ECell NIT Raipur android application and website.

## Setup

To Setup this Project and contribute follow below guidelines.

1. First fork the repo and clone it using

   `https://github.com/<Your-Username>/ecell-main-server.git`

2. Change the CWD to the project folder

   `cd ecell-main-server/`

3. Make virtual Environment (Python version recommeded = v3.6)

   `virtualenv --python=/usr/bin/python<version> myenv`

4. Activate the Virtual Environment

   `source myenv/bin/activate`

5. Install requirements.txt

   `pip install -r requirements.txt`

6. Make a copy of `.env.save` to `.env` and change the values of variables with original values.

7. Setup MYSQL Database with given credentials

   > DATABASE NAME : ecelldb

   > USERNAME : root

   > PASSWORD : datapostgres

8. Make all the Migrations

   `python manage.py makemigrations`

9. Run Migration command

   `python manage.py migrate`

10. Make a superuser for admin panel

   `python manage.py createsuperuser`

11. Run the server

    `python manage.py runserver`
