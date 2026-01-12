from django.urls import path
from .views import (
    CourseListCreateAPIView,
    LessonCreateAPIView,
    EnrollAPIView
)

urlpatterns = [
    path('courses/', CourseListCreateAPIView.as_view()),
    path('courses/<int:course_id>/lessons/', LessonCreateAPIView.as_view()),
    path('courses/<int:course_id>/enroll/', EnrollAPIView.as_view()),
]
