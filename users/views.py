from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from materials.models import Course
from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer
from users.services import create_stripe_checkout_session, create_stripe_price, create_stripe_product


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ["create"]:
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()

    @swagger_auto_schema(operation_description="Получить список пользователей")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Создать нового пользователя (регистрация)"
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Получить пользователя по ID")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Обновить данные пользователя")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Частичное обновление пользователя")
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Удалить пользователя")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["course", "lesson", "payment_method"]
    ordering_fields = ["payment_date"]
    ordering = ["-payment_date"]

    @swagger_auto_schema(
        operation_description="Получить список платежей",
        manual_parameters=[
            openapi.Parameter(
                "course",
                openapi.IN_QUERY,
                description="ID курса",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "lesson",
                openapi.IN_QUERY,
                description="ID урока",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "payment_method",
                openapi.IN_QUERY,
                description="Метод оплаты (напр. 'cash', 'card')",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "ordering",
                openapi.IN_QUERY,
                description="Сортировка по дате (напр. 'payment_date' или '-payment_date')",
                type=openapi.TYPE_STRING,
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Создать запись о платеже")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Получить платеж по ID")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Обновить запись о платеже")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Частично обновить запись о платеже")
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Удалить запись о платеже")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class CreateStripePaymentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        course_id = request.data.get("course_id")
        course = get_object_or_404(Course, id=course_id)

        product_id = create_stripe_product(course.title)
        price_id = create_stripe_price(product_id, course.price)
        success_url = "http://127.0.0.1:8000/success/"
        cancel_url = "http://127.0.0.1:8000/cancel/"
        payment_url = create_stripe_checkout_session(price_id, success_url, cancel_url)

        payment = Payment.objects.create(
            user=request.user,
            course=course,
            amount=course.price,
            payment_method="card",
            payment_url=payment_url,
        )

        return Response(
            {"payment_url": payment_url, "payment_id": payment.id},
            status=status.HTTP_201_CREATED,
        )
