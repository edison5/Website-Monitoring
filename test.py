import websitemonitor
import unittest
import statistics
import datetime


class TestAlert(unittest.TestCase):

    def test1(self):
        """test alert up"""
        site = websitemonitor.Sitereport('https://coreyms.com', 5)
        site.add_stats()  # add the first stats
        site.availability = [0]
        site.alert()  # create a first alert
        self.assertFalse(site.currentalert == None)

    def test2(self):
        """test that alert object contains good information"""
        site = websitemonitor.Sitereport('https://coreyms.com', 5)
        site.add_stats()  # add the first stats
        site.availability = [0]
        site.alert()  # create a first alert
        self.assertEqual(site.currentalert.site,site.site)
        self.assertEqual(site.currentalert.availability,0)
        self.assertTrue(site.currentalert.time<datetime.datetime.now())


    def test3(self):
        """test alert down"""
        site = websitemonitor.Sitereport('https://coreyms.com', 5)
        site.add_stats()  # add the first stats
        site.availability = [0.7]
        site.alert()  # create a first alert
        site.add_stats()
        site.availability = [0.7, 1]  # make sure that average avail>0.8
        site.alert()  # the second alert should shut the first alert down turning it to none
        self.assertEqual(site.currentalert, None)

    def test4(self):
        """test alert up after being down and checking time of the alerts is different"""
        site = websitemonitor.Sitereport('https://coreyms.com', 5)
        site.add_stats()  # add the first stats
        site.availability = [0.7]
        site.alert()  # create a first alert
        firstalertup=site.currentalert
        site.add_stats()
        site.availability = [0.7, 1]  # make sure that average avail>=0.8
        site.alert()
        site.add_stats()
        site.availability = [0.7, 1, 0.5]  # make sure that average avail<0.8
        site.alert()  # the third alert should create a new alert down turning it to none
        secondalertup=site.currentalert
        self.assertFalse(secondalertup==None)
        self.assertFalse(firstalertup.time==secondalertup.time)



if __name__ == '__main__':
    unittest.main()
