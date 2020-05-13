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
        site.alerting()  # create a first alert
        self.assertFalse(site.alert == None)

    def test2(self):
        """test that alert object contains good information"""
        site = websitemonitor.Sitereport('https://coreyms.com', 5)
        site.add_stats()  # add the first stats
        site.availability = [0]
        site.alerting()  # create a first alert
        self.assertEqual(site.alert.site,site.site)
        self.assertEqual(site.alert.availability,0)
        self.assertTrue(site.alert.time<datetime.datetime.now())


    def test3(self):
        """test alert down"""
        site = websitemonitor.Sitereport('https://coreyms.com', 5)
        site.add_stats()  # add the first stats
        site.availability = [0.7]
        site.alerting()  # create a first alert
        site.add_stats()
        site.availability = [0.7, 1]  # make sure that average avail>0.8
        site.alerting()  # the second alert should shut the first alert down turning it to none
        self.assertEqual(site.alert, None)

    def test4(self):
        """test alert up after being down and checking time of the alerts is different"""
        site = websitemonitor.Sitereport('https://coreyms.com', 5)
        site.add_stats()  # add the first stats
        site.availability = [0.7]
        site.alerting()  # create a first alert
        firstalertup=site.alert
        site.add_stats()
        site.availability = [0.7, 1]  # make sure that average avail>=0.8
        site.alerting()
        site.add_stats()
        site.availability = [0.7, 1, 0.5]  # make sure that average avail<0.8
        site.alerting()  # the third alert should create a new alert down turning it to none
        secondalertup=site.alert
        self.assertFalse(secondalertup==None)
        self.assertFalse(firstalertup.time==secondalertup.time)



if __name__ == '__main__':
    unittest.main()
