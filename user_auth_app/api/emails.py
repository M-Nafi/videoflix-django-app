
import os
from django.conf import settings
from templated_email import send_templated_mail, InlineImage
from djoser import email as djoser_email

class CustomActivationEmail(djoser_email.ActivationEmail):
    """
    Send activation email with inline logo.
    """
    def send(self, to):
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

        send_templated_mail(
            template_name='email/activation',
            from_email=self.from_email,
            recipient_list=to,
            context=self.context,
            attachments=[logo] if logo else None
        )

class CustomPasswordResetEmail(djoser_email.PasswordResetEmail):
    """
    Send password-reset email with inline logo.
    """
    def send(self, to):
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

        send_templated_mail(
            template_name='email/password_reset',
            from_email=self.from_email,
            recipient_list=to,
            context=self.context,
            attachments=[logo] if logo else None
        )