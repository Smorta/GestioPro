from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Responsable)
admin.site.register(models.Phase)
admin.site.register(models.User)
admin.site.register(models.Chantier)
admin.site.register(models.Modification)