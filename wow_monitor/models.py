from django.conf import settings
from django.db import models
from django.forms.models import model_to_dict

import json
import requests


class Character(models.Model):
    name = models.CharField(max_length=250)
    server_name = models.CharField(max_length=250)
    head = models.TextField(blank=True, null=True)
    neck = models.TextField(blank=True, null=True)
    back = models.TextField(blank=True, null=True)
    chest = models.TextField(blank=True, null=True)
    wrist = models.TextField(blank=True, null=True)
    hands = models.TextField(blank=True, null=True)
    waist = models.TextField(blank=True, null=True)
    legs = models.TextField(blank=True, null=True)
    feet = models.TextField(blank=True, null=True)
    finger1 = models.TextField(blank=True, null=True)
    finger2 = models.TextField(blank=True, null=True)
    trinket1 = models.TextField(blank=True, null=True)
    trinket2 = models.TextField(blank=True, null=True)
    mainHand = models.TextField(blank=True, null=True)
    artifactTraits = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return '{server_name} - {name}'.format(
            server_name=self.server_name,
            name=self.name
        )

    def fetch_from_battlenet(self):
        api_key = settings.BN_APIKEY
        url = 'https://us.api.battle.net/wow/character/{server_name}/{char_name}?'\
              'fields=items+talents&locale=en_US&apikey={api_key}'.format(
                  server_name=self.server_name,
                  char_name=self.name,
                  api_key=api_key
              )
        response = requests.get(url)
        data = json.loads(response.content)
        positions = [
            'head', 'neck', 'back', 'chest', 'wrist', 'hands', 'waist', 'legs',
            'feet', 'finger1', 'finger2', 'trinket1', 'trinket2', 'mainHand'
        ]
        for position in positions:
            setattr(
                self,
                position,
                str(data['items'][position]['id']) + str(data['items'][position]['itemLevel'])
            )
        self.save()
        return self

    def to_dict(self):
        return model_to_dict(self)


class SimcRank(models.Model):
    character = models.ForeignKey(Character)
    dps_rank = models.IntegerField()
    rating_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '{name} - {dps_rank}'.format(
            name=self.character.name,
            dps_rank=self.dps_rank
        )
