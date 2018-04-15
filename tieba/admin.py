from django.contrib import admin
from tieba import models

# Register your models here.

admin.site.register(models.UserProfile)
admin.site.register(models.Role)
admin.site.register(models.Article)
admin.site.register(models.Comment)
admin.site.register(models.Permission)
admin.site.register(models.TieBa)
