from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson, Subscription
from materials.validators import validate_video_url


class CourseSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_is_subscribed(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, course=obj).exists()
        return False


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(validators=[validate_video_url])

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


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ["user", "course"]
