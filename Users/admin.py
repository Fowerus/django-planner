from django.contrib import admin
from . import models


admin.site.register(models.User)
admin.site.register(models.Team)
admin.site.register(models.Proposal)