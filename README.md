# Installation Pre-Requisites

You will need the following packages to abe able to run things properly.

```
Python 3 (version 3.5 and above)
Python-pip
virtualenv (optional but recommended)
```

# Installation instructions

The project needs a few pre-requisite python packages. To install them use (It is recommended that you run all these commands in a virtual environment):

```
(BASE_DIR) $ pip install -r requirements.txt
(BASE_DIR) $ python3 manage.py makemigrations   // python vs python3 will depend on the virtual environment configuration
(BASE_DIR) $ python3 manage.py migrate
(BASE_DIR) $ python3 manage.py createsuperuser  // Create a super user to get access to the admin panel
(BASE_DIR) $ python3 manage.py runserver    // Add a Port or IP, it will default to localhost:8000
```
