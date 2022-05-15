from django.contrib import admin
from .models import Flight, User, Book
from django.contrib.admin.models import LogEntry

LogEntry.objects.all().delete()

# Register your models here.

admin.site.register(Flight)
admin.site.register(User)
admin.site.register(Book)


