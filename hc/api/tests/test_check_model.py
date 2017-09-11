from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from hc.api.models import Check


class CheckModelTestCase(TestCase):
    """Contains tests that check models"""
    def test_it_strips_tags(self):
        """Tests it strips tags"""
        check = Check()

        check.tags = " foo  bar "
        self.assertEquals(check.tags_list(), ["foo", "bar"])

    def test_it_strips_tags_empty_string(self):
        """Tests it strips tags for empty"""
        check = Check()
        check.tags = ""
        self.assertEquals(check.tags_list(), [])

    def test_status_works_with_grace_period(self):
        """Test status works with grace period"""
        check = Check()

        check.status = "up"
        check.last_ping = timezone.now() - timedelta(days=1, minutes=30)

        self.assertTrue(check.in_grace_period())
        self.assertEqual(check.get_status(), "up")

    def test_paused_check_is_not_in_grace_period(self):
        """Test paused check is not in grace period"""
        check = Check()

        check.status = "up"
        check.last_ping = timezone.now() - timedelta(days=1, minutes=30)
        self.assertTrue(check.in_grace_period())

        check.status = "paused"
        self.assertFalse(check.in_grace_period())

    def test_created_check_is_not_in_grace_period(self):
        """Test created check is not in grace period"""
        check = Check()
        check.status = "up"
        check.last_ping = timezone.now() - timedelta(days=1, minutes=30)
        self.assertTrue(check.in_grace_period())

        check.status = "new"
        self.assertFalse(check.in_grace_period())
