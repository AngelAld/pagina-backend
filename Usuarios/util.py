import random
from django.core.mail import send_mail
from django.conf import settings

from Usuarios.models import CodigoUnUso, Usuario


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
