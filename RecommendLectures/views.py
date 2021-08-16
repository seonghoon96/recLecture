from django.shortcuts import render,redirect,HttpResponse
import json
from django.http import JsonResponse
from django.views import View
from django.views import generic
from .models import *
from . import compare
# Create your views here.

schoolyear = ''
sid = 0


def logincheck(request):
    if request.method == 'POST':
        global schoolyear,sid
        ID = request.POST['user_id']
        sid = ID[1]
        PW = request.POST['user_pw']
        com = compare.Compares(ID,PW)
        result = com.crawling()
        if result == -1:
            return render(request, 'RecommendLectures/index.html', {'data': 'ID 또는 비밀번호가 잘못되었습니다.'})
        else:
            return render(request, 'RecommendLectures/Graduate_Check.html', {'result': result, 'dic': result.items(), 'check': 'btn'})


def table_selector(section):
    T_name = ''
    if section[0:2] == '일교':

        T_name = 'GeneralCulture'
    elif section[0:2] == '핵교':
        T_name = 'CoreCulture'
    else:
        T_name = section
    return T_name



def RecommendLecture(request):
    table = {
        '일교1': 'Specialistculture',
        '일교2': 'Specialistculture',
        '일교3': 'Specialistculture',
        '일교4': 'Specialistculture',
        '일교5': 'Specialistculture',
        '핵교6': 'Specialistculture',
        '핵교7': 'Specialistculture',
        '핵교8': 'Specialistculture',
        '전공기초': 'Specialistenglist',
        '전공': 'Major',
        '과학': 'Mscscience',
        '수학': 'Mscmath',
        '전산': 'Mscdataprocess',
    }
    section = {
        '일교1': '언어와철학',
        '일교2': '사회와경제',
        '일교3': '역사와문화',
        '일교4': '예술과디자인',
        '일교5': '제2외국어와한문',
        '핵교6': '법과생활',
        '핵교7': '공학의이해',
        '핵교8': '핵교8',
        '기초교양': '기초교양',
        '전공': '전공',
        'MSC과학': 'MSC과학',
        'MSC수학': 'MSC수학',
        'MSC전산': 'MSC전산',
    }
    template_name = 'RecommendLectures/Graduate_Check.html'
    c = request.GET["input"]
    print(c,"c출력1")
    Type = table[c]
    cls = section[c]
    if Type == 'major':
        Type += schoolyear
    elif Type == 'Specialistculture':
        data = Specialistculture.objects.all()
    elif Type == 'Mscscience':
        data = Mscscience.objects.all()
    elif Type == 'Mscmath':
        data = Mscmath.objects.all()
    elif Type == 'Mscdataprocess':
        data = Mscdataprocess.objects.all()
    else:
        data = Specialistenglist.objects.all()
    datas = []
    for value in data:
        dic = {
            'subjects' : value.subjects,
            "gpa" : value.gpa,
            "opensemester" : value.opensemester,
            "professor" : value.professor,
            "homework" : value.homework,
            "groupmeeting" : value.groupmeeting,
            "perofcredits" : value.perofcredits
        }
        if Type == "Specialistenglist":
            datas.append(dic)
        elif Type[:5] == "Major":
            datas.append(dic)
        else:
            if value.class_field == cls:
                datas.append(dic)
    print(datas)
    return HttpResponse(json.dumps(datas))

def index(request):
    return render(request, 'RecommendLectures/index.html')