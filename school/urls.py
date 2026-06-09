from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('dashboard/student/schedule/', views.student_schedule, name='student_schedule'),
    path('dashboard/student/buy-package/', views.create_checkout_session, name='student_buy_package'),
    path('dashboard/student/<int:pk>/', views.student_detail, name='student_detail'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/webhook/', views.stripe_webhook, name='stripe_webhook'),

    path('dashboard/student/lesson-requests/', views.student_lesson_requests, name='student_lesson_requests'),
    path('dashboard/student/lesson-requests/create/', views.student_create_lesson_request, name='student_create_lesson_request'),
    path('dashboard/student/lesson-requests/<int:pk>/respond/', views.student_respond_lesson_request, name='student_respond_lesson_request'),

    path('dashboard/instructor/', views.instructor_dashboard, name='instructor_dashboard'),
    path('dashboard/instructor/schedule/', views.instructor_schedule, name='instructor_schedule'),
    path('dashboard/instructor/lesson-requests/', views.instructor_lesson_requests, name='instructor_lesson_requests'),
    path('dashboard/instructor/lesson-requests/<int:pk>/respond/', views.instructor_respond_lesson_request, name='instructor_respond_lesson_request'),
    path('dashboard/instructor/create-lesson/', views.InstructorLessonCreateView.as_view(), name='instructor_create_lesson'),
    path('dashboard/instructor/edit-lesson/<int:pk>/', views.InstructorLessonUpdateView.as_view(), name='instructor_edit_lesson'),
    path('dashboard/instructor/delete-lesson/<int:pk>/', views.InstructorLessonDeleteView.as_view(), name='instructor_delete_lesson'),

    path('dashboard/secretary/', views.secretary_dashboard, name='secretary_dashboard'),
    path('dashboard/secretary/schedule/', views.secretary_schedule, name='secretary_schedule'),
    path('dashboard/secretary/people/', views.secretary_people, name='secretary_people'),
    path('dashboard/secretary/create-user/', views.UserCreateView.as_view(), name='create_user'),
    path('dashboard/secretary/edit-user/<int:pk>/', views.UserUpdateView.as_view(), name='edit_user'),
    path('dashboard/secretary/delete-user/<int:pk>/', views.UserDeleteView.as_view(), name='delete_user'),
    path('dashboard/secretary/create-lesson/', views.LessonCreateView.as_view(), name='create_lesson'),
    path('dashboard/secretary/edit-lesson/<int:pk>/', views.LessonUpdateView.as_view(), name='edit_lesson'),
    path('dashboard/secretary/delete-lesson/<int:pk>/', views.LessonDeleteView.as_view(), name='delete_lesson'),
    path('dashboard/secretary/create-package/', views.PackageCreateView.as_view(), name='create_package'),
    path('dashboard/secretary/edit-package/<int:pk>/', views.PackageUpdateView.as_view(), name='edit_package'),
    path('dashboard/secretary/delete-package/<int:pk>/', views.PackageDeleteView.as_view(), name='delete_package'),

    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/admin/schedule/', views.admin_schedule, name='admin_schedule'),
    path('dashboard/admin/people/', views.admin_people, name='admin_people'),
]
