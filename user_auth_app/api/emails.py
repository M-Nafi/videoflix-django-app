import os
from django.conf import settings
from djoser.email import ActivationEmail as DjoserActivationEmail, PasswordResetEmail as DjoserPasswordResetEmail
from email.mime.image import MIMEImage

class CustomActivationEmail(DjoserActivationEmail):
    """
    Send activation email with inline logo and correct backend URL.
    """
    def send(self, to, fail_silently=False, **kwargs):
        # 1) Template rendern (füllt subject, body und html_body)
        self.render()

        # 2) Logo einlesen und als Inline-MIMEImage anhängen
        logo_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'logo.png')
        try:
            with open(logo_path, 'rb') as f:
                img_data = f.read()
            img = MIMEImage(img_data)
            img.add_header('Content-ID', '<videoflix_logo>')
            img.add_header('Content-Disposition', 'inline; filename="logo.png"')
            self.attach(img)
        except FileNotFoundError:
            pass

        # 3) Absenden
        super().send(to=to, fail_silently=fail_silently, **kwargs)

class CustomPasswordResetEmail(DjoserPasswordResetEmail):
    """
    Send password-reset email with inline logo and correct backend URL.
    """
    def send(self, to, fail_silently=False, **kwargs):
        self.render()

        logo_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'logo.png')
        try:
            with open(logo_path, 'rb') as f:
                img_data = f.read()
            img = MIMEImage(img_data)
            img.add_header('Content-ID', '<videoflix_logo>')
            img.add_header('Content-Disposition', 'inline; filename="logo.png"')
            self.attach(img)
        except FileNotFoundError:
            pass

        super().send(to=to, fail_silently=fail_silently, **kwargs)
