from django.db import models


class Course(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Название курса",
        help_text="Введите название курса",
    )
    preview = models.ImageField(
        upload_to="materials/previews/",
        verbose_name="Превью",
        blank=True,
        null=True,
        help_text="Загрузите превью",
    )
    description = models.TextField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Описание курса",
        help_text="Введите описание курса",
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Название урока",
        help_text="Введите название урока",
    )
    description = models.TextField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Описание урока",
        help_text="Введите описание урока",
    )
    preview = models.ImageField(
        upload_to="materials/previews/",
        verbose_name="Превью",
        blank=True,
        null=True,
        help_text="Загрузите превью",
    )
    video_url = models.URLField(
        verbose_name="URL видео",
        blank=True,
        null=True,
        help_text="Загрузите видео",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Курс",
        help_text="Укажите курс",
        related_name="lessons",
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
