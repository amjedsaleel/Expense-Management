from django.contrib import admin

# Local Django
from . models import UserIncome, Source

# Register your models here.

admin.site.register(UserIncome)
admin.site.register(Source)