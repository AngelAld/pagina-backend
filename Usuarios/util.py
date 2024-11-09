import random
from django.core.mail import send_mail
from django.conf import settings
from Usuarios.models import CodigoUnUso, Usuario
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView


def generar_otp(usuario: Usuario):
    otp = "".join([str(random.randint(0, 9)) for _ in range(6)])
    CodigoUnUso.objects.create(usuario=usuario, codigo=otp)
    return otp


# TODO: usar redis para enviar correos de forma asíncrona


def enviar_correo(asunto, mensaje, destinatario, remitente=settings.EMAIL_HOST_USER):
    send_mail(
        asunto,
        mensaje,
        remitente,
        [destinatario],
        fail_silently=True,
    )


def enviar_correo_otp(usuario: Usuario):
    asunto = "Código de verificación"
    otp = generar_otp(usuario)
    mensaje = f"Tu código de verificación es: {otp}"
    enviar_correo(asunto, mensaje, usuario.email)
    print("Correo enviado ################################")


class UserRetrieve:
    def get(self, request, *args, **kwargs):
        instance = request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class UserCreate:
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()


class UserUpdate:
    def put(self, request, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = request.user
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        instance.refresh_from_db()
    
        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)


class UserDelete:
    def delete(self, request, *args, **kwargs):
        instance = request.user
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class UserViewSet(UserRetrieve, UserCreate, UserUpdate, GenericAPIView):
    pass
