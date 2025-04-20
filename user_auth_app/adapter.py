from allauth.account.adapter import DefaultAccountAdapter
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
import os

class HTMLOnlyAccountAdapter(DefaultAccountAdapter):
    """
    Custom AccountAdapter, der nur HTML-Mails verschickt
    und ein PNG-Logo als Inline-Attachment (CID) einbettet.
    """

    # Pfad zu deinem Logo-PNG (statt SVG)
    PNG_PATH = os.path.join(
        os.path.dirname(__file__),
        '..', 'static', 'img', 'logo.png'
    )
    PNG_CID = 'videoflix_logo'  # Identifier für die CID

    def send_mail(self, template_prefix, email, context):
        # 1) Betreff als reiner String rendern
        subject = render_to_string(
            f"{template_prefix}_subject.txt",
            context,
            request=context.get("request")
        ).strip()

        # 2) HTML‑Nachricht rendern
        html_message = render_to_string(
            f"{template_prefix}_message.html",
            context,
            request=context.get("request")
        )

        # 3) E‑Mail mit HTML‑Body erzeugen
        msg = EmailMultiAlternatives(
            subject,
            "",  # kein Plain‑Text
            self.get_from_email(),
            [email],
        )
        msg.attach_alternative(html_message, "text/html")

        # 4) Inline‑PNG als CID‑Attachment hinzufügen
        try:
            with open(self.PNG_PATH, 'rb') as png_file:
                png_data = png_file.read()
                # attach_inline (Django ≥4.1) nutzen, falls verfügbar
                if hasattr(msg, 'attach_inline'):
                    msg.attach_inline(
                        filename=os.path.basename(self.PNG_PATH),
                        content=png_data,
                        mimetype='image/png',
                        cid=self.PNG_CID
                    )
                else:
                    # Fallback für ältere Django‑Versionen
                    from email.mime.image import MIMEImage
                    mime_img = MIMEImage(png_data, _subtype='png', name=os.path.basename(self.PNG_PATH))
                    mime_img.add_header('Content-ID', f'<{self.PNG_CID}>')
                    mime_img.add_header('Content-Disposition', 'inline', filename=os.path.basename(self.PNG_PATH))
                    msg.attach(mime_img)
        except FileNotFoundError:
            # Wenn das PNG fehlt, ignorieren wir das Inline-Logo
            pass

        # 5) E‑Mail versenden
        msg.send()