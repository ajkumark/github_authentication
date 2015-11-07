from django.shortcuts import render, render_to_response, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login, authenticate
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from .models import GithubUser

import requests
import json

def home(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('profile'))
    else:
        return render_to_response('home.html', context=RequestContext(request, {'client_id':settings.CLIENT_ID}))

def github_oauth(request):
    """
    Method which authenticate a user using github and creates a django user
    """
    token = request.GET.get('code')
    github_user = GithubUser()
    access_token = github_user.get_access_token(token)
    if access_token:
        try:
            data = github_user.get_user_details(access_token)
            email = data.get('email')
            user = GithubUser.objects.get(email=email)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
        except ObjectDoesNotExist:
            email = data.get('email')
            first_name = data.get('name')
            avatar_url = data.get('avatar_url')
            profile_url = data.get('html_url')
            username = data.get('login')
            user = GithubUser.objects.create_user(email=email, username=username, first_name=first_name, avatar_url=avatar_url,
                profile_url=profile_url, access_token=access_token)
            user.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
    return HttpResponseRedirect(reverse('profile'))

@login_required(login_url='/')
def profile(request):
    """
    View which shows user profile and allows user to create repository
    """
    return render_to_response('profile.html', context=RequestContext(request, {}))

@login_required
def create_repo(request):
    """
    Service which creates a Github repo
    """
    repo_name = request.POST.get('repo_name')
    repo_description = request.POST.get('repo_description')
    repo_type = request.POST.get('repo_type')
    github_user = GithubUser()
    repo = github_user.create_github_repo(repo_name, repo_description, repo_type, request.user)
    if repo == True:
        return HttpResponse(json.dumps({"result":"success", "message":"success"}))
    else:
        return HttpResponse(json.dumps({"result":"fail", "message":repo}))

@login_required
def logout_view(request):
    """
    Logouts current user
    """
    logout(request)
    return HttpResponseRedirect(reverse('home'))

