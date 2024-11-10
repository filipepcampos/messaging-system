from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
import json

from message.models import Channel, Contact, Message


def index(request):
    return JsonResponse({"status": "success"})


def unpack_request(request):
    post_data = json.loads(request.body.decode())
    username = post_data.get("username", "")
    password = post_data.get("password", "")

    return post_data, username, password


def login_view(request):
    _, username, password = unpack_request(request)

    user = authenticate(request, username=username, password=password)
    if user is not None:
        return JsonResponse({"status": "failed", "message": "Unable to login."})
    res = login(request, user)
    return JsonResponse({"status": "success", "data": res})


def register_view(request):
    _, username, password = unpack_request(request)

    user = authenticate(request, username=username, password=password)
    if user is not None:
        return JsonResponse({"status": "failed", "message": "User already exists."})

    User.objects.create_user(
        username,
        "",
        password,
    )  # Note, setting e-mail to "" to avoid overriding User class, no time for that
    return JsonResponse({"status": "success"})


# Design decision:
# - I'm authenticating the user in **every** request.
# on typical browser apps this wouldn't be an issue because we'd be using cookies
# to maintain auth state. Doing it for a CLI would require a fair amount of additional
# effort for a manual implementation.
def authed_user_decorator(func):  # TODO: Use this
    def wrapper(request):
        post_data, username, password = unpack_request(request)

        user = authenticate(request, username=username, password=password)
        if user is None:
            return JsonResponse(
                {
                    "status": "failed",
                    "message": "You must be authenticated to perform this action.",
                },
            )

        return func(request, post_data, user)

    return wrapper


@authed_user_decorator
def user_exists_view(request, post_data, user):
    target_user = post_data["target_user"]
    target_user = User.objects.get(username=target_user)
    if target_user is None:
        return JsonResponse({"status": "success", "data": False})

    return JsonResponse({"status": "success", "data": True})


@authed_user_decorator
def add_contact_view(request, post_data, user):
    target_user = post_data["target_user"]
    target_user = User.objects.get(username=target_user)
    if target_user is None:
        return JsonResponse({"status": "failed", "message": "Target user not found."})

    Contact.objects.create(user=user, contact=target_user)
    return JsonResponse({"status": "success"})


@authed_user_decorator
def remove_contact_view(request, post_data, user):
    target_user = post_data["target_user"]
    target_user = User.objects.get(username=target_user)
    if target_user is None:
        return JsonResponse({"status": "failed", "message": "Target user not found."})

    Contact.objects.filter(user=user, contact=target_user).delete()
    return JsonResponse({"status": "success"})


@authed_user_decorator
def get_contacts_view(request, post_data, user):
    contacts = Contact.objects.filter(user=user).values("contact__username")

    serialized = json.dumps(list(contacts), cls=DjangoJSONEncoder)

    return JsonResponse({"status": "success", "data": serialized})


@authed_user_decorator
def send_direct_message_view(request, post_data, user):
    message = post_data["message"]
    target_user = post_data["target_user"]

    target_user = User.objects.get(username=target_user)
    if target_user is None:
        return JsonResponse({"status": "failed", "message": "Target user not found."})

    if not message:
        return JsonResponse({"status": "failed", "message": "Message cannot be empty."})

    if len(message) > 4096:
        return JsonResponse(
            {
                "status": "failed",
                "message": "Message cannot be longer than 4096 characters.",
            },
        )

    # Find or create a direct message channel
    channel = Channel.objects.filter(
        direct_message=True,
        participants__in=[user, target_user],
    ).first()

    if not channel:
        channel = Channel.objects.create(direct_message=True)
        channel.participants.set([user, target_user])
        channel.save()

    msg = Message.objects.create(
        author_id=user,
        channel_id=channel,
        text=message,
    )
    msg.seen_by.add(user)
    msg.save()

    return JsonResponse({"status": "success"})


@authed_user_decorator
def get_direct_messages_view(request, post_data, user):
    target_user = post_data["target_user"]

    target_user = User.objects.get(username=target_user)
    if target_user is None:
        return JsonResponse({"status": "failed", "message": "Target user not found."})

    channel = Channel.objects.filter(
        direct_message=True,
        participants__in=[user, target_user],
    ).first()

    messages = []
    if channel is not None:
        messages_qs = Message.objects.filter(channel_id=channel)

        for message in messages_qs:
            message.seen_by.add(user)

        messages = messages_qs.values(
            "text",
            "sent_date",
            "author_id__username",
        )

        # Annotate if messages were seen by target user
        for message in messages:
            message["seen"] = (
                target_user
                in Message.objects.get(
                    channel_id=channel,
                    text=message["text"],
                ).seen_by.all()
            )

    serialized = json.dumps(list(messages), cls=DjangoJSONEncoder)
    return JsonResponse({"status": "success", "data": serialized})
