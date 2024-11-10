from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register_view, name="register"),
    path("user_exists", views.user_exists_view, name="user_exists"),
    path(
        "send_direct_message",
        views.send_direct_message_view,
        name="send_direct_message",
    ),
    path(
        "get_direct_messages",
        views.get_direct_messages_view,
        name="get_direct_messages",
    ),
    path("add_contact", views.add_contact_view, name="add_contact"),
    path("remove_contact", views.remove_contact_view, name="remove_contact"),
    path("get_contacts", views.get_contacts_view, name="get_contacts"),
]
