from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.conf import settings

from .managers import UserManager

import requests

class GithubUser(AbstractBaseUser):
    username = models.CharField(max_length=90)
    email = models.CharField(max_length=90, unique=True)
    first_name = models.CharField(max_length=90, null=True, blank=True)
    avatar_url = models.URLField(max_length=200, null=True, blank=True)
    profile_url = models.URLField(max_length=200, null=True, blank=True)
    access_token = models.CharField(max_length=300, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def get_access_token(self, code):
        url = "https://github.com/login/oauth/access_token"
        headers = {'Accept': 'application/json'}
        data = {'client_id':settings.CLIENT_ID,'client_secret':settings.CLIENT_SECRET, 'code':code}
        r = requests.post(url, data, headers=headers)
        if r.status_code == 200:
            try:
                access_token = r.json().get('access_token')
                return access_token
            except:
                return

    def get_user_details(self, access_token):
        url = "https://api.github.com/user"
        headers = {"Authorization": "token %s" %access_token, 'Accept': 'application/json'}
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            return r.json()
        else:
            return

    @classmethod
    def create_github_repo(cls, repo_name, repo_descripiton, repo_type, user):
        url = "https://api.github.com/user/repos"
        access_token = cls.objects.get(email=user.email).access_token
        print "access_token", access_token
        headers = {"Authorization": "token %s" %access_token, 'Accept': 'application/json'}
        print headers
        data = '{"name":"%s", "description":"%s", "private":%s}' %(repo_name, repo_descripiton, repo_type)
        print data
        r = requests.post(url, headers=headers, data=data)
        if r.status_code == 201:
            return True
        else:
            print r.status_code, r.json()
            print r.json().get('errors')
            try:
                message = r.json().get('errors')[0]['message']
                return message
            except:
                message = r.json().get('message')
                return message
                