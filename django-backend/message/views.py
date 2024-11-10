from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
import json


def index(request):
    return JsonResponse({"status": "success"})


def login_view(request):
    post_data = json.loads(request.body.decode())
    username = post_data.get("username", "")
    password = post_data.get("password", "")

    user = authenticate(request, username=username, password=password)
    if user is not None:
        return JsonResponse({"status": "failed", "message": "Unable to login."})
    res = login(request, user)
    return JsonResponse({"status": "success", "data": res})


def register_view(request):
    post_data = json.loads(request.body.decode())
    username = post_data.get("username", "")
    password = post_data.get("password", "")

    user = authenticate(request, username=username, password=password)
    if user is not None:
        return {"status": "failed", "message": "User already exists."}

    User.objects.create_user(
        username,
        "",
        password,
    )  # Note, setting e-mail to "" to avoid overriding User class, no time for that
    return {}
