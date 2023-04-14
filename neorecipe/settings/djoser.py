import os
import environ

base = environ.Path(__file__) - 3
env = environ.Env()
environ.Env.read_env(os.path.join(base(), '.env'))

DJOSER = {
    "USER_CREATE_PASSWORD_RETYPE": True,
    "SET_USERNAME_RETYPE": True,
    "SET_PASSWORD_RETYPE": True,
    "SEND_ACTIVATION_EMAIL": True,
    "ACTIVATION_URL": "activate/{uid}/{token}",
    "PASSWORD_RESET_CONFIRM_URL": "reset-password/{uid}/{token}"
}
