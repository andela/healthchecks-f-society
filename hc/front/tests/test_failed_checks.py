from hc.api.models import Check
from hc.test import BaseTestCase
from datetime import timedelta as td
from django.utils import timezone
from django.urls import reverse

class MyChecksTestCase(BaseTestCase):

    def setUp(self):
        super(MyChecksTestCase, self).setUp()
        self.check = Check(user=self.alice)
        self.check.save()

    def test_it_shows_red_check(self):
        self.check.last_ping = timezone.now() - td(days=3)
        self.check.status = "up"
        self.check.save()

        self.client.login(username="alice@example.org", password="password")
        url = reverse('hc-failed-checks')
        response = self.client.get(url)

        # Desktop
        self.assertContains(response, "icon-down")

        # Mobile
        self.assertContains(response, "label-danger")
        