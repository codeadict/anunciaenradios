from django.contrib import admin
from django.forms import ModelForm
from wysiwyg import ElrteWidget
from models import Estacion

from django.db import models
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin as FlatPageAdminOld

class FlatPageAdmin(FlatPageAdminOld):
    formfield_overrides = {
        models.TextField: {'widget': ElrteWidget()},
    }

class EstacionAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': ElrteWidget()},
    }
    
    
admin.site.register(Estacion, EstacionAdmin)

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)

