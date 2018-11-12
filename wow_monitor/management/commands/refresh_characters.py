import json

from django.core.management.base import BaseCommand
from django.conf import settings

from wow_monitor.models import Character, SimcRank
from subprocess import call

class Command(BaseCommand):
    help = """This is a cron job for refreshing all wow characters."""
    def handle(self, *args, **options):
        for c in Character.objects.all():
            updated = False
            print 'Checking {}'.format(c.name)
            old_c_dict = c.to_dict()
            new_c_dict = c.fetch_from_battlenet().to_dict()
            for key in old_c_dict:
                if new_c_dict[key] != old_c_dict[key]:
                    updated = True
                    # Run simc here
                    call([settings.SIMC,
                          'armory={server},{name}'.format(
                              server=c.server_name, name=c.name
                          ),
                          'report_details=0',
                          'json=simcTmp'])
                    with open('simcTmp', 'r') as report:
                        report_json = json.load(report)
                        dps_rank = report_json['sim']['raid_dps']['mean']
                        SimcRank.objects.create(character=c, dps_rank=dps_rank)
                    break
            if not updated:
                print 'Nothing changed for character {}'.format(c.name)
            else:
                print 'Difference found for character {}'.format(c.name)
        return
