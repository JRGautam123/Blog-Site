from django.contrib import admin
from .models import Category,Post,Comments,Like
# Register your models here.


admin.site.register([Category,Post,Comments,Like])