
import os
from django.conf import settings
from templated_email import send_templated_mail, InlineImage
from djoser import email as djoser_email

class CustomActivationEmail(djoser_email.ActivationEmail):
    """
    Djoser ActivationEmail mit Inline-PNG-Logo über templated_email.
    """
    def send(self, to, context):
        # 1) Logo laden (falls vorhanden)
        logo_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'logo.png')
        try:
            with open(logo_path, 'rb') as png_file:
                logo = InlineImage(
                    name='logo.png',
                    content=png_file.read(),
                    cid='videoflix_logo'
                )
        except FileNotFoundError:
            logo = None

        # 2) E-Mail versenden
        send_templated_mail(
            template_name='email/activation',    # lädt activation.txt & activation.html
            from_email=self.from_email,
            recipient_list=[to],
            context=context,
            attachments=[logo] if logo else None
        )


class CustomPasswordResetEmail(djoser_email.PasswordResetEmail):
    """
    Djoser PasswordResetEmail mit Inline-PNG-Logo über templated_email.
    """
    def send(self, to, context):
        # 1) Logo laden
        logo_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'logo.png')
        try:
            with open(logo_path, 'rb') as png_file:
                logo = InlineImage(
                    name='logo.png',
                    content=png_file.read(),
                    cid='videoflix_logo'
                )
        except FileNotFoundError:
            logo = None

        # 2) E-Mail versenden
        send_templated_mail(
            template_name='email/password_reset',  # lädt password_reset.txt & password_reset.html
            from_email=self.from_email,
            recipient_list=[to],
            context=context,
            attachments=[logo] if logo else None
        )