import json
import hmac
from hashlib import sha1
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound
from django.conf import settings
from .bot import process_message


@method_decorator(csrf_exempt, 'dispatch')
class FacebookWebHookView(View):
    def get(self, request):
        hub_mode = request.GET.get('hub.mode')
        hub_challenge = request.GET.get('hub.challenge')
        hub_verify_token = request.GET.get('hub.verify_token')

        if hub_mode and hub_verify_token:
            if hub_mode == 'subscribe' and hub_verify_token == getattr(settings, 'FB_VERIFY_TOKEN'):
                return HttpResponse(hub_challenge)

            return HttpResponseForbidden()

    def post(self, request):
        fb_app_secret = getattr(settings, 'FB_APP_SECRET').encode()
        x_hub_signature = request.headers.get('X-Hub-Signature')
        expected_signature = 'sha1=' + hmac.new(fb_app_secret, request.body,  sha1).hexdigest()
        if x_hub_signature != expected_signature:
            return HttpResponseForbidden()

        body = json.loads(request.body.decode())
        if body.get('object') == 'page':
            for entry in body['entry']:
                # Get the webhook event. entry.messaging is an array, but
                # will only ever contain one event, so we get index 0
                message = entry['messaging'][0]
                process_message(message)

            return HttpResponse()
        return HttpResponseNotFound()
