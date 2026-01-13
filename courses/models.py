from django.db import models
from django.conf import settings 

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Course(models.Model):
    LEVEL_CHOICES = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='courses')
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, limit_choices_to={'role': 'mentor'}, on_delete=models.CASCADE, related_name='instructed_courses')
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, limit_choices_to={'role': 'student'}, blank=True, related_name='enrolled_courses')
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='lesson_images/', null=True, blank=True)
    order = models.PositiveIntegerField(default=0) 

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"
