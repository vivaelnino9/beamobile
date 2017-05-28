from django import template
from django.core.exceptions import ObjectDoesNotExist

from bea_app.models import *
from bea_app.choices import *

register = template.Library()

@register.simple_tag(name='get_challenge_status',takes_context=True)
# gets status of challenge for current user
def get_challenge_status(context,challenge):
    request = context['request']
    user = request.user
    try:
        status = Challenge_Status.objects.get(user=user,challenge=challenge).status
        return dict(STATUS_CHOICES).get(int(status))
    except ObjectDoesNotExist:
        return 'Pending'
