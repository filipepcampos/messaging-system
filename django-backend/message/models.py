from django.db import models
from django.contrib.auth.models import User


class Channel(models.Model):
    channel_id = models.AutoField(primary_key=True)
    start_date = models.DateTimeField(auto_now_add=True)
    participants = models.ManyToManyField(User)
    direct_message = models.BooleanField()


class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    sent_date = models.DateTimeField(auto_now_add=True)

    author_id = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
    )  # Do not delete messages from deleted users
    channel_id = models.ForeignKey(Channel, on_delete=models.CASCADE)

    text = models.CharField(max_length=4096)  # TODO: Hardcoded max-len
    seen_by = models.ManyToManyField(User, related_name="seen_by")


class Contact(
    models.Model,
):  # Uni-directional contact (I might want a contact that doesn't have me as a contact)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    contact = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contact")
