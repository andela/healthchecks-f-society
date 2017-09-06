from hc.api.models import Check
from hc.test import BaseTestCase




class AddCheckTestCase(BaseTestCase):

    def test_it_works(self):
        url = "/checks/add/"
        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url)
        self.assertRedirects(r, "/checks/")
        assert Check.objects.count() == 1

    ### Test that team access works
    def test_team_access_works(self):
        url = "/checks/add/"
        
        self.client.login(username="charlie@example.org", password="password")
        r = self.client.post(url)
     
        check = Check.objects.get()
        self.assertNotEqual(check.user, self.alice)



  
