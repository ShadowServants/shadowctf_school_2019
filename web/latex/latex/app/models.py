from django.contrib.auth.models import User
from django.db import models


class Document(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    rendered_file = models.FileField(upload_to='rendered_docs/', null=True)
    owner_id = models.IntegerField()
