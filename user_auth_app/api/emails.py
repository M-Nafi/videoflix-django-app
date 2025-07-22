import os
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.staticfiles import finders
from email.mime.image import MIMEImage


def send_verification_email(email: str, uidb64: str, token: str) -> None:
    """
    Sends an email to the given address with a link to verify it.
    The email contains a link with a uid and token that can be used to
    verify the email address. The link is valid for 24 hours.
    """
    subject = 'Confirm your email'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    # Create the correct frontend link
    link = f'{settings.FRONTEND_ACTIVATION_URL}?uid={uidb64}&token={token}'

    plain_message = (
        'Hello!\n\n'
        'Please confirm your email address by copying the following link into your browser:\n\n'
        f'{link}\n\n'
        'This link is valid for 24 hours.\n\n'
        'Thanks,\nYour Videoflix Team'
    )

    # Use EmailMultiAlternatives to support logo attachment
    msg = EmailMultiAlternatives(
        subject=subject,
        body=plain_message,
        from_email=from_email,
        to=recipient_list
    )

    # Render HTML template
    try:
        html_message = render_to_string('email/activation.html', {
            'link': link,
            'user_email': email
        })
        msg.attach_alternative(html_message, "text/html")
    except Exception as e:
        print(f"Warning: Could not render HTML template: {e}")

    # Attach logo for inline display
    try:
        logo_path = finders.find('logo.png')
        print(logo_path)
        if logo_path and os.path.exists(logo_path):
            with open(logo_path, 'rb') as f:
                img = MIMEImage(f.read())
                img.add_header('Content-ID', '<videoflix_logo>')
                img.add_header('Content-Disposition', 'inline; filename="logo.png"')
                msg.attach(img)
    except Exception as e:
        print(f"Warning: Could not attach logo: {e}")

    msg.send(fail_silently=False)


def send_password_reset_email(email: str, uidb64: str, token: str) -> None:
    """
    Sends an email to the given address with a link to reset the password.
    The email contains a link with a uid and token that can be used to
    reset the password. The link is valid for 24 hours.
    """
    subject = 'Reset your password - Videoflix'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    # Create the correct frontend link
    link = f'{settings.FRONTEND_CONFIRM_PASSWORD_URL}?uid={uidb64}&token={token}'

    plain_message = (
        'Hello!\n\n'
        'You have requested a password reset.\n\n'
        'To reset your password, copy the following link into your browser:\n\n'
        f'{link}\n\n'
        'This link is valid for 24 hours.\n\n'
        'Thanks,\nYour Videoflix Team'
    )

    # Use EmailMultiAlternatives to support logo attachment
    msg = EmailMultiAlternatives(
        subject=subject,
        body=plain_message,
        from_email=from_email,
        to=recipient_list
    )

    # Render HTML template
    try:
        html_message = render_to_string('email/reset_password.html', {
            'link': link,
            'user_email': email
        })
        msg.attach_alternative(html_message, "text/html")
    except Exception as e:
        print(f"Warning: Could not render HTML template: {e}")

    # Attach logo for inline display
    try:
        logo_path = finders.find('logo.png')
        if logo_path and os.path.exists(logo_path):
            with open(logo_path, 'rb') as f:
                img = MIMEImage(f.read())
                img.add_header('Content-ID', '<videoflix_logo>')
                img.add_header('Content-Disposition', 'inline; filename="logo.png"')
                msg.attach(img)
    except Exception as e:
        print(f"Warning: Could not attach logo: {e}")

    msg.send(fail_silently=False)
