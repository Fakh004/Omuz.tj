from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated ,AllowAny
from rest_framework.response import Response
from .models import Category, Course, Lesson
from .serializers import *
from .permissions import IsAdminOrReadOnly, IsInstructorOrAdmin



class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class CategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class CourseListAPIView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]


class CourseListCreateAPIView(generics.ListCreateAPIView):
    queryset = Course.objects.all() 
    serializer_class = CourseCreateUpdateSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):

        serializer.save(instructor=self.request.user)

class CourseRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    permission_classes = [AllowAny]  
    serializer_class = CourseCreateUpdateSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CourseSerializer
        return self.serializer_class


from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import EnrollStudentSerializer
from .models import Course
from .permissions import IsInstructorOrAdmin  

class EnrollStudentAPIView(generics.GenericAPIView):
    serializer_class = EnrollStudentSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Response({"error": "Курс не найден"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(course=course)

        return Response({"success": f"Студент добавлен в курс {course.title}"}, status=status.HTTP_200_OK)

    

class LessonListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsInstructorOrAdmin]

    def get_queryset(self):
        course_id = self.kwargs['course_pk']
        return Lesson.objects.filter(course_id=course_id)

    def perform_create(self, serializer):
        course_id = self.kwargs['course_pk']
        serializer.save(course_id=course_id)


class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [AllowAny]
