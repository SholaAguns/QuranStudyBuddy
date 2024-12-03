from django.contrib import auth
from django.db import models


class User(auth.models.User, auth.models.PermissionsMixin):
    slug = models.SlugField(allow_unicode=True, unique=True, max_length=200)
    created_dt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "@{}".format(self.username)