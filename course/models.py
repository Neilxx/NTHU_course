from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Teacher(models.Model):
    name = models.TextField()
    title = models.TextField()
    department = models.TextField()
    experiences = models.TextField()
    field = models.TextField(default='None')
    email = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

#    def publish(self):
 #       self.published_date = timezone.now()
  #      self.save()

    def __str__(self):
        return self.name

class Course(models.Model):
    course_id = models.TextField()
    course_ch = models.TextField()
    course_en = models.TextField()
    category = models.TextField()
    time = models.TextField()
    teacher_ch = models.TextField()
    teacher_en = models.TextField()
    teacher_id = models.ForeignKey(Teacher)
    created_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.course_ch

class Comment(models.Model):
    course = models.ForeignKey(Course, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

#    def approve(self):
#        self.approved_comment = True
#        self.save()

    def __str__(self):
        return self.text

class Rating(models.Model):
    course_id = models.ForeignKey(Course,related_name='ratings')
    user_id = models.CharField(max_length=50)
    _score0 = models.IntegerField(default=0)
    _score1 = models.IntegerField(default=0)
    _score2 = models.IntegerField(default=0)
    
    def __str__(self):
        return self.user_id