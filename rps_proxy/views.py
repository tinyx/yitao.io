import json
import requests

from rest_framework.views import APIView
from rest_framework.response import Response


class RpsProxyView(APIView):
    permission_classes = []

    def post(request, *args, **kwargs):
        response = requests.get('https://rps.lucaspickering.me/api/matches/new/')
        return Response({
            'response_type': 'in_channel',
            'text': 'https://rps.lucaspickering.me/matches/live/{}'
                .format(json.loads(response.content)['match_id'])
        })
