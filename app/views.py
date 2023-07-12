import csv
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from .authencate import EmailBackEnd
from .models import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import math
from django.views.generic import UpdateView

# Create your views here.
data_from_excell = [
    {
        "candidate_name": "james kulwa majuto",
        "candidate_number": "P1278.0108.2007",
        "sex": "male",
        "kiswahili": "B",
        "english": "B",
        "maarifa": "A",
        "hisabati": "A",
        "science": "A",
        "average_grade": "A",
        "average_marks": "250",
        "mkoa": "Tanga",
        "wilaya": "Handeni",
        "kata": "Biazamulo",
    },
    {},
]


def welcome(request):
    return render(request, "welcome.html")


def home(request):
    year = Year.objects.all()
    x = [a.id for a in year]
    current_year = max(x)
    y = Year.objects.get(id=current_year)
    total_student = Student.objects.filter(year=y)
    total_schools = School.objects.all()
    total_allocated = Student.objects.filter(Q(year=y) and Q(is_active=False))
    total_unallocated = Student.objects.filter(Q(year=y) and Q(is_active=True))
    context = {
        "total_student": str(len(total_student)),
        "total_schools": str(len(total_schools)),
        "total_allocated": str(len(total_allocated)),
        "total_unallocated": str(len(total_unallocated)),
    }

    return render(request, "user_templates/check_allocation.html", context)


def loginPage(request):
    return render(request, "login.html")


def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user = EmailBackEnd.authenticate(
            request,
            username=request.POST.get("email"),
            password=request.POST.get("password"),
        )
        if user != None:
            login(request, user)
            if user.type == "admin":
                print("admin")
                return redirect("app:admin_home")
            elif user.type == "necta":
                print("necta")
                return redirect("app:necta_home")

        else:
            messages.error(request, "Invalid Login Credentials!")
            # return HttpResponseRedirect("/")
            return redirect("app:login")


# @login_required
def admin_home(request):
    print(request.user)
    year = Year.objects.all()
    x = [a.id for a in year]
    try:
        current_year = max(x)
        y = Year.objects.get(id=current_year)
        total_student = str(len(Student.objects.all()))
        total_allocated = str(
            len(Student.objects.filter(Q(year=y) and Q(is_active=False)))
        )
        total_unallocated = str(
            len(Student.objects.filter(Q(year=y) and Q(is_active=True)))
        )
    except:
        total_student = "0"
        total_allocated = "0"
        total_unallocated = "0"
    total_schools = School.objects.all()
    special_schools = School.objects.filter(type="special")
    data = []
    for s in special_schools:
        quantity_required = QuantityRequired.objects.get(school_id=s)
        data.append(
            {
                "name": s.name,
                "type": s.type,
                "quantity_required": quantity_required.quantity,
                "Mkoa": s.wilaya_id.mkoa_id.name,
                "Wilaya": s.wilaya_id.name,
            }
        )
    context = {
        "total_student": total_student,
        "total_schools": str(len(total_schools)),
        "total_allocated": total_allocated,
        "total_unallocated": total_unallocated,
        "special_schools": data,
    }
    if request.user:
        return render(request, "admin_template/home_content.html", context)
    else:
        return HttpResponse("Please Login First")


def necta_home(request):
    print(request.user)
    year = Year.objects.all()
    x = [a.id for a in year]
    try:
        current_year = max(x)
        y = Year.objects.get(id=current_year)
        total_student = str(len(Student.objects.all()))
        total_allocated = str(
            len(Student.objects.filter(Q(year=y) and Q(is_active=False)))
        )
        total_unallocated = str(
            len(Student.objects.filter(Q(year=y) and Q(is_active=True)))
        )
    except:
        total_student = "0"
        total_allocated = "0"
        total_unallocated = "0"
    total_schools = School.objects.all()
    special_schools = School.objects.filter(type="special")
    data = []
    for s in special_schools:
        quantity_required = QuantityRequired.objects.get(school_id=s)
        data.append(
            {
                "name": s.name,
                "type": s.type,
                "quantity_required": quantity_required.quantity,
                "Mkoa": s.wilaya_id.mkoa_id.name,
                "Wilaya": s.wilaya_id.name,
            }
        )
    context = {
        "total_student": total_student,
        "total_schools": str(len(total_schools)),
        "total_allocated": total_allocated,
        "total_unallocated": total_unallocated,
        "special_schools": data,
    }

    if request.user:
        return render(request, "necta_template/home_content.html", context)
    else:
        return HttpResponse("Please Login First")


def admin_profile(request):
    user = User.objects.get(id=request.user.id)
    context = {"user": user}
    return render(request, "admin_template/admin_profile.html", context)


def admin_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect("app:admin_profile")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")

        try:
            customuser = User.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect("app:admin_profile")
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect("app:admin_profile")


def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")


def feedBack(request):
    return render(request, "user_templates/student_feedback.html")


def manage_session(request):
    return render(request, "admin_template/manage_session_template.html")


def add_session(request):
    if request.method == "POST":
        year = request.POST["year"]
        yr = Year.objects.create(year=year)
        yr.save()
    return render(request, "admin_template/add_session_template.html")


def checStudents_alloc(request):
    data = Student.objects.all()
    context = {"allocated": True}
    print(context)
    return HttpResponse(context)


def allocationYears(request):
    data = Year.objects.all()
    print(data)
    return HttpResponse(data)


def insert_students(request):
    # pri
    year = Year.objects.all()
    y = []
    for d in year:
        print(year)
        stu = Student.objects.filter(year=d)
        # print(stu)
        allocated = "No"
        if len(stu) >= 1:
            stSc = StudentSchool.objects.filter(student_id=stu[0])
            if len(stSc) >= 1:
                allocated = "Yes"
        data = {"year": d.year, "allocated": allocated}
        y.append(data)

    context = {"data": y}
    print(context)
    if request.method != "POST":
        return render(
            request, "admin_template/add_studntsToallocate_template.html", context
        )

    else:
        # resultSheet = request.POST.get('resultSheet')
        yr = Year.objects.get(year=request.POST["year"])
        csv_file = request.FILES.get("csv_file")
        try:
            # print(resultSheet)
            data = csv.DictReader(csv_file.read().decode("utf-8").splitlines())
            data_list = [dict(row) for row in data]

            s = 0
            for data1 in data_list:
                # This make sure that the id of kata is as we save in kata table
                mkoa = Mkoa.objects.get(name=data1["mkoa"])

                w = Wilaya.objects.values("id", "name").filter(mkoa_id=mkoa)

                wl = [x for x in w if x["name"].replace("\n", " ") == data1["wilaya"]]

                wilaya = Wilaya.objects.get(id=wl[0]["id"])

                s = s + 1
                print(s)
                print("here")
                student = Student.objects.create(
                    candidate_name=data1["candidate_name"],
                    candidate_number=data1["candidate_number"],
                    sex=data1["sex"],
                    kiswahili=data1["kiswahili"],
                    english=data1["english"],
                    maarifa=data1["maarifa"],
                    hisabati=data1["hisabati"],
                    science=data1["science"],
                    average_grade=data1["average_grade"],
                    average_marks=data1["average_marks"],
                    wilaya_id=wilaya,
                    year=yr,
                )
                student.save()
            print("done")
            messages.success(request, "resultSheet Successfully")
            return redirect("app:allocate_students")
        except:
            messages.error(request, "Failed to Upload")
            return redirect("app:allocate_students")


def insert_students_necta(request):
    # pri
    year = Year.objects.values("year").all()
    context = {"years": year}
    if request.method != "POST":
        return render(
            request, "necta_template/add_studntsToallocate_template.html", context
        )

    else:
        year = Year.objects.all()
        x = [a.id for a in year]
        try:
            new_year_id = max(x) + 1
            yr = Year.objects.get(id=new_year_id)
        except:
            new_year = "2023"
            yr = Year.objects.create(year=new_year)

        csv_file = request.FILES.get("csv_file")
        try:
            # print(resultSheet)
            data = csv.DictReader(csv_file.read().decode("utf-8").splitlines())
            data_list = [dict(row) for row in data]
            # print(data_list[0])
            # print(dict(data))
            s = 0
            for data1 in data_list:
                # print('here1')
                # This make sure that the id of kata is as we save in kata table
                mkoa = Mkoa.objects.get(name=data1["mkoa"])
                # print(mkoa.name)
                w = Wilaya.objects.values("id", "name").filter(mkoa_id=mkoa)
                # print(w[0]['name'])
                wl = [x for x in w if x["name"].replace("\n", " ") == data1["wilaya"]]
                # print(wl)
                wilaya = Wilaya.objects.get(id=wl[0]["id"])

                s = s + 1
                print(s)
                print("here")
                student = Student.objects.create(
                    candidate_name=data1["candidate_name"],
                    candidate_number=data1["candidate_number"],
                    sex=data1["sex"],
                    kiswahili=data1["kiswahili"],
                    english=data1["english"],
                    maarifa=data1["maarifa"],
                    hisabati=data1["hisabati"],
                    science=data1["science"],
                    average_grade=data1["average_grade"],
                    average_marks=data1["average_marks"],
                    wilaya_id=wilaya,
                    # year=request.data['year']
                    year=yr,
                )
                student.save()
            print("done")
            messages.success(request, "resultSheet Successfully")
            return redirect("app:allocate_students_necta")
        except:
            messages.error(request, "Failed to Upload")
            return redirect("app:allocate_students_necta")


def edit_student_results(request):
    students = Student.objects.all()
    context = {
        "students": students,
    }
    return render(request, "necta_template/edit_student_results.html", context)


def addSchool(request):
    if request.method != "POST":
        return render(request, "admin_template/add_secSchool_template.html")

    else:
        resultSheet = request.POST.get("resultSheet")
        try:
            print(resultSheet.path)
            messages.success(request, "resultSheet Successfully")
            return redirect("app:allocate_students")
        except:
            messages.error(request, "Failed to Upload")
            return redirect("app:allocate_students")


def manage_student(request):
    yr = Year.objects.all()
    y = [a.id for a in yr]
    year = Year.objects.get(id=max(y))
    stu = StudentSchool.objects.all()
    students = []
    for d in stu:
        if d.student_id.year == year:
            students.append(d)
        continue

    context = {"students": students}
    return render(request, "admin_template/manage_student_template.html", context)


def group_list(lst, group_lengths):
    result = []
    idx = 0
    for length in group_lengths:
        group = lst[idx : idx + length]
        result.append(group)
        idx += length
    return result


def specialSchool(year):
    # This give us required student in special schools
    # for girls
    special_school_f = School.objects.values("id", "name", "sex", "type").filter(
        type="special", sex="female"
    )
    ssf = [x for x in special_school_f]
    ssf_list = []
    total_required_special_f = 0
    for d in ssf:
        sps = School.objects.get(id=d["id"])
        ss_q = QuantityRequired.objects.values("quantity").get(Q(school_id=sps))
        total_required_special_f = total_required_special_f + ss_q["quantity"]
        data = {
            "id": d["id"],
            "name": d["name"],
            "sex": d["sex"],
            "type": d["type"],
            "quantity_required": ss_q["quantity"],
        }
        ssf_list.append(data)
    students_f = (
        Student.objects.values("id", "candidate_name", "sex")
        .filter(Q(year=year) and Q(is_active=True) and Q(sex="female"))
        .order_by("-average_marks")[:total_required_special_f]
    )
    students_fx = [x for x in students_f]
    special_quantity_f = [x["quantity_required"] for x in ssf_list]
    student_groups_f = group_list(students_fx, special_quantity_f)
    output_list_f = [
        {
            "id": d["id"],
            "name": d["name"],
            "sex": d["sex"],
            "type": d["type"],
            "quantity_required": d["quantity_required"],
            "students": sub_list,
        }
        for d, sub_list in zip(ssf_list, student_groups_f)
    ]
    # This is to save the students to the special school

    for sch in output_list_f:
        school = School.objects.get(id=sch["id"])
        for stu in sch["students"]:
            student = Student.objects.get(id=stu["id"])
            data = StudentSchool.objects.create(school_id=school, student_id=student)
            data.save()
            student.is_active = False
            student.save()
    print("boys student saved at special school")

    # for boys
    special_school_m = School.objects.values("id", "name", "sex", "type").filter(
        type="special", sex="male"
    )
    ssm = [x for x in special_school_m]
    ssm_list = []
    total_required_special_m = 0
    for d in ssm:
        sps = School.objects.get(id=d["id"])
        ss_q = QuantityRequired.objects.values("quantity").get(Q(school_id=sps))
        total_required_special_m = total_required_special_m + ss_q["quantity"]
        data = {
            "id": d["id"],
            "name": d["name"],
            "sex": d["sex"],
            "type": d["type"],
            "quantity_required": ss_q["quantity"],
        }
        ssm_list.append(data)
    students_m = (
        Student.objects.values("id", "candidate_name", "sex")
        .filter(Q(year=year) and Q(is_active=True) and Q(sex="male"))
        .order_by("-average_marks")[:total_required_special_m]
    )
    students_mx = [x for x in students_m]
    special_quantity_m = [x["quantity_required"] for x in ssm_list]
    student_groups_m = group_list(students_mx, special_quantity_m)
    output_list_m = [
        {
            "id": d["id"],
            "name": d["name"],
            "sex": d["sex"],
            "type": d["type"],
            "quantity_required": d["quantity_required"],
            "students": sub_list,
        }
        for d, sub_list in zip(ssm_list, student_groups_m)
    ]
    # This is to save the students to the special school

    for sch in output_list_m:
        school = School.objects.get(id=sch["id"])
        for stu in sch["students"]:
            student = Student.objects.get(id=stu["id"])
            data = StudentSchool.objects.create(school_id=school, student_id=student)
            data.save()
            student.is_active = False
            student.save()
        print("student saved at " + sch["name"])


def technicalSchool(year):
    # This give us required student in special schools
    # for girls
    special_school_f = School.objects.values("id", "name", "sex", "type").filter(
        type="technical", sex="female"
    )
    ssf = [x for x in special_school_f]
    ssf_list = []
    total_required_special_f = 0
    for d in ssf:
        sps = School.objects.get(id=d["id"])
        ss_q = QuantityRequired.objects.values("quantity").get(Q(school_id=sps))
        total_required_special_f = total_required_special_f + ss_q["quantity"]
        data = {
            "id": d["id"],
            "name": d["name"],
            "sex": d["sex"],
            "type": d["type"],
            "quantity_required": ss_q["quantity"],
        }
        ssf_list.append(data)
    students_f = (
        Student.objects.values("id", "candidate_name", "sex")
        .filter(Q(year=year) and Q(is_active=True) and Q(sex="female"))
        .order_by("-average_marks")[:total_required_special_f]
    )
    students_fx = [x for x in students_f]
    special_quantity_f = [x["quantity_required"] for x in ssf_list]
    student_groups_f = group_list(students_fx, special_quantity_f)
    output_list_f = [
        {
            "id": d["id"],
            "name": d["name"],
            "sex": d["sex"],
            "type": d["type"],
            "quantity_required": d["quantity_required"],
            "students": sub_list,
        }
        for d, sub_list in zip(ssf_list, student_groups_f)
    ]
    # This is to save the students to the special school

    for sch in output_list_f:
        school = School.objects.get(id=sch["id"])
        for stu in sch["students"]:
            student = Student.objects.get(id=stu["id"])
            data = StudentSchool.objects.create(school_id=school, student_id=student)
            data.save()
            student.is_active = False
            student.save()
    print("boys student saved at special school")

    # for boys
    special_school_m = School.objects.values("id", "name", "sex", "type").filter(
        type="technical", sex="male"
    )
    ssm = [x for x in special_school_m]
    ssm_list = []
    total_required_special_m = 0
    for d in ssm:
        sps = School.objects.get(id=d["id"])
        ss_q = QuantityRequired.objects.values("quantity").get(Q(school_id=sps))
        total_required_special_m = total_required_special_m + ss_q["quantity"]
        data = {
            "id": d["id"],
            "name": d["name"],
            "sex": d["sex"],
            "type": d["type"],
            "quantity_required": ss_q["quantity"],
        }
        ssm_list.append(data)
    students_m = (
        Student.objects.values("id", "candidate_name", "sex")
        .filter(Q(year=year) and Q(is_active=True) and Q(sex="male"))
        .order_by("-average_marks")[:total_required_special_m]
    )
    students_mx = [x for x in students_m]
    special_quantity_m = [x["quantity_required"] for x in ssm_list]
    student_groups_m = group_list(students_mx, special_quantity_m)
    output_list_m = [
        {
            "id": d["id"],
            "name": d["name"],
            "sex": d["sex"],
            "type": d["type"],
            "quantity_required": d["quantity_required"],
            "students": sub_list,
        }
        for d, sub_list in zip(ssm_list, student_groups_m)
    ]
    # This is to save the students to the special school

    for sch in output_list_m:
        school = School.objects.get(id=sch["id"])
        for stu in sch["students"]:
            student = Student.objects.get(id=stu["id"])
            data = StudentSchool.objects.create(school_id=school, student_id=student)
            data.save()
            student.is_active = False
            student.save()
        print("student saved at " + sch["name"])


def wardSchool(year):
    wilaya = Wilaya.objects.values("id", "name").all()
    w = [x for x in wilaya]
    c = 0
    for i in w:
        wly = Wilaya.objects.get(id=i["id"])
        print(wly.id)
        # stu = Student.objects.values('id', 'average_grade').filter(wilaya_id=wly)
        sch = School.objects.values("id", "name").filter(wilaya_id=wly)
        x = Student.objects.filter(wilaya_id=wly)
        stu = []
        for q in x:
            if q.is_active == True:
                if q.year == year:
                    stu.append(q)
                else:
                    continue
            else:
                continue
        sch_length = len(sch)
        stu_length = len(stu)
        print(type(stu_length))
        c = c + stu_length
        print(c)
        div = stu_length / sch_length
        grouping_length = []
        for i in range(sch_length):
            grouping_length.append(math.floor(div))
        e = 0
        for v in grouping_length:
            e = e + v
        grouping_length[sch_length - 1] = (
            grouping_length[sch_length - 1] + stu_length - e
        )
        student_groups = group_list(stu, grouping_length)
        output_list = [
            {"id": d["id"], "name": d["name"], "students": sub_list}
            for d, sub_list in zip(sch, student_groups)
        ]

        for i in output_list:
            # print('here')

            school = School.objects.get(id=i["id"])
            for j in i["students"]:
                student = Student.objects.get(id=j.id)
                data = StudentSchool.objects.create(
                    school_id=school, student_id=student
                )
                student.is_active = False
                student.save()
        # print(wly.mkoa_id.name+"----"+wly.name)
    # print('student length'+c)


def Selection(request):
    year = Year.objects.all()
    x = [a.id for a in year]
    current_year = max(x)
    y = Year.objects.get(id=current_year)
    try:
        specialSchool(y)
    except:
        print("special school error")
    print("special school done")
    try:
        technicalSchool(y)
    except:
        print("technical school error")
    print("technical school done")
    try:
        wardSchool(y)
    except:
        print("ward school error")
    print("ward school done")
    return redirect("app:allocate_students")


def InsertStudentView(request):
    for data in data_from_excell:
        # This make sure that the id of kata is as we save in kata table
        mkoa = Mkoa.objects.get(name=data["mkoa"])
        w = Wilaya.objects.values("id", "name").filter(mkoa_id=mkoa)
        wl = [x for x in w if x["name"] == data["wilaya"]]
        wilaya = Wilaya.objects.get(id=wl[0]["id"])
        # k = Kata.objects.values('id', 'name').filter(wilaya_id=wilaya)
        # kt = [x for x in k if x['name'] == data['kata']]
        # kata = Kata.objects.get(id=kt[0]['id'])
        ##

        student = Student.objects.create(
            candidate_name=data["candidate_name"],
            candidate_number=data["candidate_number"],
            sex=data["sex"],
            kiswahili=data["kiswahili"],
            english=data["english"],
            maarifa=data["maarifa"],
            hisabati=data["hisabati"],
            science=data["science"],
            average_grade=data["average_grade"],
            average_marks=data["average_marks"],
            wilaya_id=wilaya,
            year=request.data["year"],
        )
        student.save()
    return 0


def QuantifyStudent(request):
    schools = School.objects.filter(Q(type="special") or Q(type="technical"))
    x = [e for e in schools]
    for sc in x:
        quantity = QuantityRequired.objects.create(
            quantity=20, school_id=sc, year="2023"
        )
        quantity.save()
    return HttpResponse("done")


def joke(request):
    stu = StudentSchool.objects.values("id").all()
    return HttpResponse(str(len(stu)))


# class based view

class EditStudentResults(UpdateView):
    model = Student
    fields = "__all__"
    template_name = "necta_template/update_student_view.html"
    success_url = reverse_lazy("app:edit_student_results")
