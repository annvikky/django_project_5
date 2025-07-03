from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import User


class LessonAndSubscriptonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@mail.ru", password="admin")
        self.course = Course.objects.create(title="Test Course")
        self.lesson = Lesson.objects.create(
            title="Test Lesson", course=self.course, owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_create_lesson(self):
        url = reverse("materials:lessons_create")
        data = {
            "title": "New Lesson",
            "course": self.course.pk,
            "video_url": "https://youtube.com/some_video",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_lesson(self):
        url = reverse("materials:lessons_retrieve", args=[self.lesson.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.lesson.title)

    def test_update_lesson(self):
        url = reverse("materials:lessons_update", args=[self.lesson.pk])
        response = self.client.patch(url, {"title": "Updated"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_lesson(self):
        url = reverse("materials:lessons_delete", args=[self.lesson.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_subscription(self):
        url = reverse("materials:subscribe")
        data = {"course_id": self.course.pk}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Подписка добавлена")
        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

        response = self.client.post(url, data)
        self.assertEqual(response.data["message"], "Подписка удалена")
        self.assertFalse(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )
