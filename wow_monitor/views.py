import json

from django.views.generic import TemplateView
from django.http import HttpResponse, Http404
from rest_framework import generics

from wow_monitor.models import Character, SimcRank


def simc_ranks(request, server_name, name):
    character = Character.objects.filter(server_name=server_name, name=name)
    if character:
        result = []
        for simc in SimcRank.objects.filter(character=character).order_by('rating_time'):
            result.append({
                'dps_rank': simc.dps_rank,
                'rating_time': simc.rating_time.isoformat()
            })
        return HttpResponse(json.dumps(result),\
                            content_type='application/json')
    return HttpResponse(json.dumps([]), content_type='application/json')


class WowMonitorView(TemplateView):
    template_name = 'wow-monitor.html'

    def get_context_data(self, **kwargs):
        server_name = kwargs.get('server_name')
        name = kwargs.get('name')
        character = Character.objects.filter(server_name=server_name, name=name)
        if character:
            result = []
            for simc in SimcRank.objects.filter(character=character).order_by('rating_time'):
                result.append({
                    'dps_rank': simc.dps_rank,
                    'rating_time': simc.rating_time.isoformat()
                })
            context = super(WowMonitorView, self).get_context_data(**kwargs)
            context['simc_ranks'] = json.dumps(result)
            context['char_name'] = name
            return context
        else:
          raise Http404