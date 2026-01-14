from django.contrib.auth.backends import ModelBackend, BaseBackend

from django.contrib.auth import get_user_model
from django.db.models import Q

import math

import string


import random

import yahooquery


User = get_user_model()


class EmailBackend(BaseBackend):
    def authenticate(self, request, username = None, password = None, **kwargs):
        email = username or kwargs.get('email')
        if email is None:
            return None # This is my version of ensuring that email is required for login
        else:
            try:
                user = User.objects.get(Q(username__iexact=email) | Q(email__iexact=email))
                # This will ensure that our password is secure "password123" would
                # turn into a convoluted mess

                if user.check_password(password): 
                    return user
                else:
                    return None

            except User.DoesNotExist:
                return  None
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
            


            

def service():
    ACCEPTED_MAIL_FREE_SERVICE = ["@ucalgary.ca"]
    # We need to get user's email, and we can use string concetation to find the email, or endswith "@Ucalgary.ca"
    # if EmailBackEnd(email).endswith("@ucalgary.ca"):
    #     pass

def verification():
    # We'll send a verifcation code, and use randomized letter, numbers, and symbols to create a code. We'll check if the user's verification code matches in our database. #Send via: Google, Yahoo, Outlook, etc.


    LENGTH_OF_CODE = 8

    letters = [
    # Uppercase A–Z
    'A','B','C','D','E','F','G','H','I','J','K','L','M',
    'N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
    'a','b','c','d','e','f','g','h','i','j','k','l','m',
    'n','o','p','q','r','s','t','u','v','w','x','y','z',
]
    numbers = ['0','1','2','3','4','5','6','7','8','9',]

    symbols = [ '!','"', '#','$','%','&',"'",'(',')','*','+',
    ',','-','.','/',';',':','<','=','>','?','@',
    '[','\\',']','^','_','`','{','|','}','~']

    for i in range(LENGTH_OF_CODE):
        pass
    return 0








# Create Exception handling



