from django.shortcuts import render
from .models import Teacher, Course, Rating
from .forms import CommentForm
from django.shortcuts import get_object_or_404, redirect
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def home(request):
    if request.GET.get('search_box', None): # If the form is submitted
        key_word = request.GET.get('search_box', None)
        if Course.objects.filter(teacher_ch__contains=key_word):
            course_list = Course.objects.filter(teacher_ch__contains=key_word) 
        else:
          print('course')
          course_list = Course.objects.filter(course_ch__contains=key_word)
        return render(request, 'home.html', {'course_list': course_list})
    else:
        return render(request, 'home.html')

def search_result(request):
  pass

def course_detail(request, pk):
    course = Course.objects.get(pk=pk)
    image = course.teacher_id.name + '.jpg'
    year = course.course_id[:3] + '學年度'
    # 目前還沒做紀錄每一個user各自的分數
    ratings0 = course.ratings.exclude(_score0=0)
    ratings1 = course.ratings.exclude(_score1=0)
    ratings2 = course.ratings.exclude(_score2=0)
    #self_Ranking = Ranking.objects.filter(course_id=course.course_id,user_id=??)
    people0 = len(ratings0)
    people1 = len(ratings1)
    people2 = len(ratings2)
    score0 = sum([rating._score0 for rating in ratings0])/people0 if people0 > 0 else 0
    score1 = sum([rating._score1 for rating in ratings1])/people1 if people1 > 0 else 0
    score2 = sum([rating._score2 for rating in ratings2])/people2 if people2 > 0 else 0

    return render(request, 'course_detail.html', {'score0': round(score0,2), 'score1': round(score1,2),
        'score2': round(score2,2),'people0': people0, 'people1': people1, 'people2': people2, 
        'course': course, 'image': image, 'year': year})

def teacher_detail(request, pk):
    teacher = Teacher.objects.get(pk=pk)
    course_list = Course.objects.filter(teacher_ch=teacher.name)
    image = teacher.name + '.jpg'
    return render(request, 'teacher_detail.html', 
                  {'teacher': teacher, 'course_list': course_list, 'image': image})

def add_course(request):
    with open('course.json', 'r', encoding='UTF-8') as file:
        data = json.loads(file.read())
        for i in list(range(len(data))):
          try:
            Course.objects.create(course_id=data[i]['id'],
                                  course_ch=data[i]['course_ch'], 
                                  course_en=data[i]['course_en'], 
                                  category=data[i]['category'],
                                  time=data[i]['time'],
                                  teacher_ch=data[i]['teacher_ch'],
                                  teacher_en=data[i]['teacher_en'],
                                  teacher_id=Teacher.objects.get(name=data[i]['teacher_ch']))
          except:
            pass
    return render(request, 'course_all.html')

def add_teacher_1(request):
    with open('teacher1.json', 'r', encoding='UTF-8') as file:
        data = json.loads(file.read())
        for i in list(range(len(data))):
          Teacher.objects.create(name=data[i]['Name'],
                                 title=data[i]['Title'], 
                                 department=data[i]['Department'], 
                                 experiences='None',
                                 email=data[i]['Email'])
    return render(request, 'course_all.html')

def add_teacher_2(request):
    with open('teacher2.json', 'r', encoding='UTF-8') as file:
        data = json.loads(file.read())
        for i in list(range(len(data))):
          Teacher.objects.create(name=data[i]['Name'],
                                 title=data[i]['Title'], 
                                 department='None', 
                                 experiences=data[i]['Experience'],
                                 email=data[i]['Email'])
    return render(request, 'course_all.html')

def add_comment_to_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.course = course
            comment.save()
            return redirect('course_detail', pk=course.pk)
    else:
        form = CommentForm()
    return render(request, 'add_comment_to_course.html', {'form': form})
@csrf_exempt
def post_rating_to_course(request, pk):
    course = get_object_or_404(Course,pk=pk)
    if request.method == "POST":       
        print('user'+request.POST.get('user_id')+' post '+request.POST.get('score'))
        idx = int(request.POST.get('idx'))
        # print(type(request.POST.get('idx')))
        defaults={'_score'+str(idx):request.POST.get('score')}
        rating = course.ratings.update_or_create(defaults=defaults,user_id=request.POST.get('user_id'))
        score=None
        people=None
        if idx==0:
            ratings = course.ratings.exclude(_score0=0)
            people = len(ratings)
            score = sum([rating._score0 for rating in ratings])/people if people > 0 else 0 
        elif idx==1:
            ratings = course.ratings.exclude(_score1=0)
            people = len(ratings)
            score = sum([rating._score1 for rating in ratings])/people if people > 0 else 0
            print(idx, people, score)
        elif idx==2:
            ratings = course.ratings.exclude(_score2=0)
            people = len(ratings)
            score = sum([rating._score2 for rating in ratings])/people if people > 0 else 0
        
        return HttpResponse(json.dumps({'score':score,'people':people}),content_type='application/json')
    elif request.method == "GET":
        try:
            rating = course.ratings.get(user_id=request.GET.get('user_id'))
            return HttpResponse(json.dumps({'score0':rating._score0,'score1':rating._score1,'score2':rating._score2}),
                content_type='application/json')
        except Rating.DoesNotExist:         
            return HttpResponse(json.dumps({'score0':0,'score1':0,'score2':0}),content_type='application/json')
    
    