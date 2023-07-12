from mtaa import tanzania
from .models import *
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse


def MkoaWilayaKata(request):
    print(tanzania)
    mikoa = [entry for entry in tanzania]
    for i in range(0, len(mikoa) - 1):
        tosave = Mkoa.objects.create(name=mikoa[i])
        tosave.save()
    print("mikoa saved")
    mikoa_again = Mkoa.objects.values('id', 'name').all()
    mikoa_list = [entry for entry in mikoa_again]
    data = []
    for ml in mikoa_list:
        dist = tanzania.get(ml['name']).districts
        mk = Mkoa.objects.get(id=ml['id'])
        districtss = [entry for entry in dist]
        dataD = []
        for z in range(0, len(districtss)):
            d = districtss[z]
            w_tosave = Wilaya.objects.create(mkoa_id=mk, name=d)
            w_tosave.save()
            x = Wilaya.objects.values('id', 'name', 'mkoa_id').get(name=districtss[z])
            dataD.append(x)
        data.append({'id': ml['id'], 'name': ml['name'], 'districts': dataD})
        print("saved district of " + ml['name'])

        district_again = Wilaya.objects.values('id', 'name').filter(mkoa_id=mk)
        district_list = [entry for entry in district_again]

        for dl in district_list:
            wad = tanzania.get(ml['name']).districts.get(dl['name']).wards
            kata = [entry for entry in wad if entry != "ward_post_code"]
            wl = Wilaya.objects.get(id=dl['id'])
            for k in kata:
                to_save = Kata.objects.create(name=k, wilaya_id=wl)
                to_save.save()

    return 0


def GetMikoa(request):
    data = Mkoa.objects.values('id', 'name').all()
    context = {
        "mikoa": data
    }

    return render(request, "user_templates/student_view_attendance.html", context)


def GetWilaya(request, mkoa_id):
    mkoa = Mkoa.objects.get(id=mkoa_id)
    mkoadata = Mkoa.objects.values('id', 'name').get(id=mkoa_id)
    data = Wilaya.objects.values('id', 'name').filter(mkoa_id=mkoa)
    context = {"wilayadata": data, "mkoadata":mkoadata}
    return render(request, "user_templates/user_view_wilaya.html", context)
  


def GetSchools(request, wilaya_id):
    year = Year.objects.values('year').all()
    wilaya = Wilaya.objects.get(id=wilaya_id)
    wilayadata = Wilaya.objects.values('id', 'name').get(id=wilaya_id)
    data = School.objects.values('id', 'name', 'type', 'sex').filter(wilaya_id=wilaya)
    print("------------------")
    print(data)
    context = {"wilayadata": wilayadata['name'], "schools":data, 'years': year}
    return render(request, "user_templates/user_view_wards.html", context)

def adminGetMikoa(request):
    data = Mkoa.objects.values('id', 'name').all()
    context = {
        "mikoa": data
    }

    return render(request, "admin_template/student_view_attendance.html", context)


def adminGetWilaya(request, mkoa_id):
    mkoa = Mkoa.objects.get(id=mkoa_id)
    mkoadata = Mkoa.objects.values('id', 'name').get(id=mkoa_id)
    data = Wilaya.objects.values('id', 'name').filter(mkoa_id=mkoa)
    context = {"wilayadata": data, "mkoadata":mkoadata}
    return render(request, "admin_template/user_view_wilaya.html", context)
  


def adminGetSchools(request, wilaya_id):
    year = Year.objects.values('year').all()

    print(request.POST)
    wilaya = Wilaya.objects.get(id=wilaya_id)
    wilayadata = Wilaya.objects.values('id', 'name').get(id=wilaya_id)
    data = School.objects.values('id', 'name', 'type', 'sex').filter(wilaya_id=wilaya)
    print("------------------")
    context = {"wilayadata": wilayadata['name'], "schools":data, 'years': year}
    return render(request, "admin_template/user_view_wards.html", context)


def adminGetStudents(request, school_id):
    print(request.POST['year'])
    print('------------------')
    yr = Year.objects.get(year=request.POST['year'])
    school = School.objects.get(id=school_id)
    print('here')
    data = StudentSchool.objects.values('id', 'student_id').filter(school_id=school)
    d = [x for x in data]
    schooldata = School.objects.values('id', 'name', 'type', 'sex').get(id=school_id)
    print(schooldata)
    students = []
    for g in d:
        stu = Student.objects.get(id=g['student_id'])
        if stu.year == yr:
            some = {
                    'id': stu.id,
                    'candidate_name': stu.candidate_name,
                    'candidate_number': stu.candidate_number,
                    'sex': stu.sex,
                    'average_marks': stu.average_marks,
                    'average_grade': stu.average_grade,
                    'mkoa': stu.wilaya_id.mkoa_id.name,
                    'wilaya': stu.wilaya_id.name,
                    }
            students.append(some)
        continue
    context = {"school": schooldata, "student":students}
    return render(request, "admin_template/students_allocated.html", context)



def GetStudents(request, school_id):
    print(request.POST['year'])
    yr = Year.objects.get(year=request.POST['year'])
    school = School.objects.get(id=school_id)
    print(school.name)
    data = StudentSchool.objects.values('id', 'student_id').filter(school_id=school)
    print(data)
    d = [x for x in data]
    schooldata = School.objects.values('id', 'name', 'type', 'sex').get(id=school_id)

    students = []
    for g in d:
        stu = Student.objects.get(id=g['student_id'])
        if stu.year == yr:
            some = {'id': stu.id, 'candidate_name': stu.candidate_name, 'candidate_number': stu.candidate_number, 'sex':stu.sex}
            students.append(some)
        continue
    context = {"school": schooldata, "student":students}
    return render(request, "user_templates/students_allocated.html", context)


def SingleStudentSchool(request):
    if request.method == "POST":
        cand_number = request.POST["candidate_number"]
        print(cand_number)
        try:
            stud = Student.objects.get(candidate_number=cand_number)
            data = StudentSchool.objects.get(student_id=stud)
            context = {'data': data}
   
            return render(request, "user_templates/check_allocation.html", context)
        except:
            messages.error(request, "Invalid Credentials!")
            redirect('app:check_stu_alloc')
    else:
        return render(request, "user_templates/check_allocation.html")



