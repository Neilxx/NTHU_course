"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from course.views import home, search_result, course_detail, add_course, add_teacher_1, add_teacher_2, teacher_detail, add_comment_to_course, post_rating_to_course


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'home/', home, name='home'),
    url(r'^course/(?P<pk>\d+)/$', course_detail, name='course_detail'),
    url(r'^teacher/(?P<pk>\d+)/$', teacher_detail, name='teacher_detail'),
    url(r'add_course/', add_course),
    url(r'add_teacher_1/', add_teacher_1),   
    url(r'add_teacher_2/', add_teacher_2), 
    url(r'^course/(?P<pk>\d+)/comment/$', add_comment_to_course, name='add_comment_to_course'),
    url(r'^course/(?P<pk>\d+)/rating/$', post_rating_to_course),
    url (r'^search/$', search_result), 
]
