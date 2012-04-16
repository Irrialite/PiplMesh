from django import dispatch
from django.conf import settings
from django.views import debug, generic as generic_views

from pushserver import signals

from piplmesh.account import models

@dispatch.receiver(signals.channel_subscribe)
def process_channel_subscribe(sender, request, channel_id, **kwargs):
    request.user.update(
        push__opened_connections = {
            'http_if_none_match': request.META['HTTP_IF_NONE_MATCH'],
            'http_if_modified_since': request.META['HTTP_IF_MODIFIED_SINCE']
        },
        set__last_access = datetime.datetime.now()
    )
    
    if channel_id not in request.user.channel:
        updates.send_update(
            channel_id,
            {
                'type': 'answer',
                'value': {
                    'action': 'JOIN',
                    'message': request.user.username
                }
            }
        )
    # TODO: Code this into upper request
    request.user.channel[channel_id] = True
    reques.user.save()

@dispatch.receiver(signals.channel_unsubscribe)
def process_channel_unsubscribe(sender, request, channel_id, **kwargs):
    models.User.objects(
        id = request.user.id,
        opened_connections = {
            'http_if_none_match': request.META['HTTP_IF_NONE_MATCH'],
            'http_if_modified_since': request.META['HTTP_IF_MODIFIED_SINCE']
        }
    ).update_one(unset__opened_connections__S = 1)

    # TODO: Race condition??
    request.user.update(pull__opened_connections=None)
    request.user.update(set__last_access = datetime.datetime.now())


class HomeView(generic_views.TemplateView):
    template_name = 'home.html'
        
class SearchView(generic_views.TemplateView):
    template_name = 'search.html'