from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ["id", "title", "preview", "description", "lessons_count", "lessons"]

    def get_lessons_count(self, course):
        # return Lesson.objects.filter(course=course).count()
        return course.lessons.count()
