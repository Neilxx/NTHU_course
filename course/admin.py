from django.contrib import admin

# Register your models here.
from .models import Teacher, Course, Comment, Rating


admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(Comment)
admin.site.register(Rating)