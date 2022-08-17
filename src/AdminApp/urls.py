from django.urls import path

from . import views

urlpatterns = [
    path('admins', views.AdminsTableTemplateView.as_view(), name='admins_table'),
    path('students', views.StudentsTableTemplateView.as_view(), name='students_table'),
    path('teachers', views.TeachersTableTemplateView.as_view(), name='teachers_table'),
    path('subjects', views.SubjectsTableTemplateView.as_view(), name='subjects_table'),
    path('courses', views.CoursesTableTemplateView.as_view(), name='courses_table'),

    path('user/delete', views.UserDeleteView.as_view(), name='user_delete'),
    path('user/create', views.GenerateUserCreateLink.as_view(), name='user_create'),
    path('user/import', views.ExcelImportDataView.as_view(), name='excel_import'),

    path('course/delete', views.CourseDeleteView.as_view(), name='course_delete'),
    path('course/create', views.CourseCreateView.as_view(), name='course_create'),
    path('course/view/<int:course_identifier>', views.CourseDetailView.as_view(), name='course_detail'),
    path('course/update/<int:course_identifier>', views.CourseUpdateView.as_view(), name='course_update'),
    
    path('subjects/delete', views.SubjectsDeleteView.as_view(), name='subjects_delete'),
    path('subjects/create', views.SubjectsCreateView.as_view(), name='subjects_create'),
    path('subject/view/<int:subject_identifier>', views.SubjectDetailView.as_view(), name='subject_detail'),
    path('subject/update/<int:subject_identifier>', views.SubjectUpdateView.as_view(), name='subject_update'),

    path('course/lessons/delete', views.CourseLessonsDeleteView.as_view(), name='lessons_delete'),
    path('course/<int:course_identifier>/lessons', views.CourseLessonGenerateView.as_view(), name='lessons_create'),
]
