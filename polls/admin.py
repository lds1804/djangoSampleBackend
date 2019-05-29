from django.contrib import admin

# Register your models here.


from django.contrib import admin

from .models import Provider
from .models import Polygon

admin.site.register(Provider)
admin.site.register(Polygon)