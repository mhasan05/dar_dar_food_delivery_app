import random
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import render
from django.utils.html import strip_tags
from email.utils import formataddr
from django.utils import timezone
from datetime import timedelta
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import transaction
import logging
from dotenv import load_dotenv
import os
import googlemaps
load_dotenv()
logger = logging.getLogger(__name__)

api_key = os.getenv('GOOGLE_MAPS_API_KEY')

gmaps = googlemaps.Client(key=api_key)

def get_location(lat, lon):
    result = gmaps.reverse_geocode((lat, lon))
    return result[0]['formatted_address'] if result else None

def send_otp(user):
    otp = str(random.randint(100000, 999999))
    user.otp = otp
    user.otp_expired = timezone.now() + timedelta(minutes=10)

    try:
        with transaction.atomic():
            user.save()

            # Send OTP email
            subject = 'Verify Your Identity'
            from_email = formataddr(("Dar Dar", settings.EMAIL_HOST_USER))
            to = user.email
            html_content = render_to_string('email/otp_verification.html', {'otp': otp})
            text_content = strip_tags(html_content)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

        return True, otp
    except Exception as e:
        logger.error(f"Error while sending OTP: {str(e)}")
        return False, otp

    

def user_token(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)



def custom_error(request, exception=None):
    status_code = getattr(exception, 'status_code', 500)
    template_name = f"error/{status_code}.html"

    logger.error(f"Error {status_code} occurred at {request.path} from {request.META.get('REMOTE_ADDR')}")

    try:
        return render(request, template_name, {'status_code': status_code}, status=status_code)
    except Exception:
        return render(request, "error/generic_error.html", {'status_code': status_code}, status=status_code)

