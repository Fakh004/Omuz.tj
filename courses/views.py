from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Course, Lesson, Enrollment
from .serializers import CourseSerializer, LessonSerializer
from .permissions import IsTeacher, IsStudent


class CourseListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.role not in ['teacher', 'admin']:
            return Response({'detail': 'Permission denied'}, status=403)

        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(teacher=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class LessonCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def post(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id, teacher=request.user)
        except Course.DoesNotExist:
            return Response({'detail': 'Not found'}, status=404)

        serializer = LessonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(course=course)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class EnrollAPIView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def post(self, request, course_id):
        course = Course.objects.get(id=course_id)

        Enrollment.objects.get_or_create(
            student=request.user,
            course=course
        )

        return Response({'message': 'Enrolled successfully'})
