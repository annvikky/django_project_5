from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.http import HttpResponse

schema_view = get_schema_view(
    openapi.Info(
        title="Courses API",
        default_version="v1",
        description="Приложение для управления курсами, уроками, пользователями и платежами",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="admin@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


def index(request):
    return HttpResponse("Приложение успешно работает!")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("materials/", include("materials.urls", namespace="materials")),
    path("users/", include("users.urls", namespace="users")),
    path('', index),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
