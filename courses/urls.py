from django.urls import path
from .views import *

urlpatterns = [
    # Category
    path('categories/', CategoryListCreateAPIView.as_view()),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroyAPIView.as_view()),

    # Courses
    path('courses/', CourseListAPIView.as_view()),
    path('courses/create/', CourseListCreateAPIView.as_view()),
    path('courses/<int:pk>/', CourseRetrieveUpdateDestroyAPIView.as_view()),

    # Enroll student
    path('courses/<int:pk>/enroll/', EnrollStudentAPIView.as_view()),

    # Lessons
    path('courses/<int:course_pk>/lessons/', LessonListCreateAPIView.as_view()),
    path('lessons/<int:pk>/', LessonRetrieveUpdateDestroyAPIView.as_view()),
]
