import os
from django.conf import settings
from django.contrib.staticfiles import finders
from djoser.email import ActivationEmail, PasswordResetEmail
from email.mime.image import MIMEImage

class CustomActivationEmail(ActivationEmail):
    """
    Send activation email with inline logo using Django staticfiles finder.
    """
    def send(self, to, fail_silently=False, **kwargs):
        self.render()

        # Logo über den Staticfiles‐Finder ermitteln
        logo_path = finders.find('logo.png')
        if not logo_path:
            # Fallback: stilles Scheitern oder eigene Logik
            return super().send(to=to, fail_silently=fail_silently, **kwargs)

        with open(logo_path, 'rb') as f:
            img = MIMEImage(f.read())
            img.add_header('Content-ID', '<videoflix_logo>')
            img.add_header('Content-Disposition', 'inline; filename="logo.png"')
            self.attach(img)

        super().send(to=to, fail_silently=fail_silently, **kwargs)

class CustomPasswordResetEmail(PasswordResetEmail):
    """
    Send password-reset email with inline logo using Django staticfiles finder.
    """
    def send(self, to, fail_silently=False, **kwargs):
        self.render()

        logo_path = finders.find('logo.png')
        if not logo_path:
            return super().send(to=to, fail_silently=fail_silently, **kwargs)

        with open(logo_path, 'rb') as f:
            img = MIMEImage(f.read())
            img.add_header('Content-ID', '<videoflix_logo>')
            img.add_header('Content-Disposition', 'inline; filename="logo.png"')
            self.attach(img)

        super().send(to=to, fail_silently=fail_silently, **kwargs)
