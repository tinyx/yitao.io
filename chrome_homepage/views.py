from datetime import date

from django.views.generic import TemplateView
from django.http import Http404

from crabfactory.models import Profile


class ChromeHomepage(TemplateView):
    template_name = 'chrome_homepage.html'

    def get_context_data(self, **kwargs):
        profile_guid = kwargs.get('profile_guid')
        print profile_guid
        try:
            profile = Profile.objects.get(guid=profile_guid)
            context = super(ChromeHomepage, self).get_context_data(**kwargs)
            if profile.life_partner_name and profile.anniversary_date:
                context['life_partner_name'] = profile.life_partner_name
                context['days_since'] = (date.today() - profile.anniversary_date).days
            context['websites'] = profile.user.website_set.all()
            return context
        except Profile.DoesNotExist:
            raise Http404
