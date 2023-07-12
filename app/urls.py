from django.urls import path
from . import views
from .views import EditStudentResults
from . import location

app_name = "app"
urlpatterns = [
    path("", views.welcome, name="welcome"),
    path("student_home/", views.home, name="users_home"),
    path("year", views.allocationYears, name="alloc_years"),
    # path('demo',location.MkoaWilayaKata),
    path("userFeedback", views.feedBack, name="user_feedback"),
    path(
        "check_student_allocation", location.SingleStudentSchool, name="check_stu_alloc"
    ),
    path("mikoa", location.GetMikoa, name="all_regions"),
    path("wilaya/<mkoa_id>", location.GetWilaya, name="get_region_discrits"),
    path("schools/<wilaya_id>", location.GetSchools, name="get_district_wards"),
    path(
        "students_allocated/<school_id>",
        location.GetStudents,
        name="get_school_student",
    ),
    path("adminLogin/", views.loginPage, name="login"),
    path("mikoa_ad", location.adminGetMikoa, name="all_regions_ad"),
    path("wilaya_ad/<mkoa_id>", location.adminGetWilaya, name="get_region_discritsad"),
    path(
        "schools_ad/<wilaya_id>", location.adminGetSchools, name="get_district_wards_ad"
    ),
    path(
        "students_allocated_ad/<school_id>",
        location.adminGetStudents,
        name="get_school_student_ad",
    ),
    path("logout_user/", views.logout_user, name="logout_user"),
    path("login", views.doLogin, name="doLogin"),
    path("admin_home/", views.admin_home, name="admin_home"),
    path("manage_student/", views.manage_student, name="manage_student"),
    path("admin_profile/", views.admin_profile, name="admin_profile"),
    path(
        "admin_profile_update/", views.admin_profile_update, name="admin_profile_update"
    ),
    path("allocate_students/", views.insert_students, name="allocate_students"),
    path("chec_alloc/", views.checStudents_alloc, name="checStudents_alloc"),
    path("add_secondary_school/", views.addSchool, name="add_secondary_school"),
    path("manage_session/", views.manage_session, name="manage_session"),
    path("add_session/", views.add_session, name="add_session"),
    path("perform_selection/", views.Selection, name="perform_selection"),
    # path('adminLogin/', views.loginPage, name="login"),
    path("necta_home/", views.necta_home, name="necta_home"),
    path(
        "allocate_students_necta/",
        views.insert_students_necta,
        name="allocate_students_necta",
    ),
    path(
        "edit_student_results/", views.edit_student_results, name="edit_student_results"
    ),
    # class based view
    path(
        "update_results/<int:pk>/", EditStudentResults.as_view(), name="update_results"
    ),
]
