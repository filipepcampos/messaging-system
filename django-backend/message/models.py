from django.db import models


class Message(models.Model):
    message_id = models.UUIDField()
    pub_date = models.DateTimeField("date published")
