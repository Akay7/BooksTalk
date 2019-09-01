from django.views import View
from django.http import HttpResponse, HttpResponseForbidden
from django.conf import settings


class FacebookWebHookView(View):
    def get(self, request):
        hub_mode = request.GET.get('hub.mode')
        hub_challenge = request.GET.get('hub.challenge')
        hub_verify_token = request.GET.get('hub.verify_token')

        if hub_mode and hub_verify_token:
            if hub_mode == 'subscribe' and hub_verify_token == getattr(settings, 'FB_VERIFY_TOKEN'):
                return HttpResponse(hub_challenge)

            return HttpResponseForbidden()
