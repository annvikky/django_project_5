from rest_framework.serializers import ValidationError


def validate_video_url(value):
    allowed_domain = "youtube.com"
    if allowed_domain not in value.lower():
        raise ValidationError(
            "Допустимы только ссылки с YouTube. Проверьте вводимую ссылку"
        )
    return value
