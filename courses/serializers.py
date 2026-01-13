from rest_framework import serializers
from .models import Category, Course, Lesson
from accounts.models import CustomUser



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']



class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content', 'image', 'order']



class CourseSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)  
    lessons = LessonSerializer(many=True, read_only=True) 
    instructor = serializers.StringRelatedField()  
    students = serializers.StringRelatedField(many=True) 

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'category',
            'instructor', 'students', 'level', 'created_at', 'lessons'
        ]



class CourseCreateUpdateSerializer(serializers.ModelSerializer):
    instructor = serializers.StringRelatedField(read_only=True)  # не нужно передавать в POST

    class Meta:
        model = Course
        fields = ['title', 'description', 'category', 'level', 'instructor']


class EnrollStudentSerializer(serializers.ModelSerializer):
    student_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Course
        fields = ['student_id']

    def validate_student_id(self, value):
        try:
            user = CustomUser.objects.get(id=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Студент не найден")
        if user.role != 'student':
            raise serializers.ValidationError("Можно записать только студентов")
        return value

    def save(self, **kwargs):
        course = self.instance
        student_id = self.validated_data['student_id']
        student = CustomUser.objects.get(id=student_id)
        course.students.add(student)
        return course
