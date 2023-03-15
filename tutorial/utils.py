import logging

from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

logger = logging.getLogger(__name__)

@receiver(user_logged_in)
def login_logger(request, user, **kwargs):
    print("{} logged in with {}".format(user.email, request))