import requests
import time
import datetime


class Sitereport:


    def __init__(self, site, checkinterval):
        self.site = site  # url of the site
        self.checkinterval = checkinterval  # in seconds
        self.time = []  # the time of each check (self.time[i] time at check i)
        self.availability = []  # self.availability[i] = int(0,1) at time self.time[i]
        self.responsetime = []  # self.responsetime[i] = responsetime at time self.time[i]
        self.lasttimeupdated = datetime.datetime.now()
        self.alert = None

    def report_stats(self, mins):
        """uses the funtions below to report
        the accumulated stats"""

        now = datetime.datetime.now()
        before = now - datetime.timedelta(minutes=mins)
        indextostart = self.find_index(before)  # the first index of self.time whose time is in the 10mins window
        self.__compute_availability(indextostart, mins)
        self.__compute_average_max_time(indextostart, mins)

    def __compute_availability(self, indextostart, mins):
        """updates the self.availablity to only the relevant
        values (i.e recieved in the last 60 minutes) and
        computes the percentage of the availability starting
        from the correct index of time"""
        availability = self.availability[indextostart:]
        if (mins == 60):
            self.availability = availability
        print("Availability for the last {} mins for site {} is: {}%"
              .format(mins, self.site, sum(availability) * 100 / len(availability)))

    def __compute_average_max_time(self, indextostart, mins):
        """updates the self.responsetime to only the relevant
        values (i.e recieved in the last 60 mins) and
        computes the average response time and maximum
        response time starting from the correct index
        of time"""
        response = self.responsetime[indextostart:]
        if (mins == 60):
            self.responsetime = response
        print("Average Response time for the last {} mins for site {} is: {} s"
              .format(mins, self.site, sum(response) / len(response)))
        print("Maximum Response time for the last {} mins for site {} is: {} s"
              .format(mins, self.site, max(response)))

    def add_stats(self):
        """Logs the time of the update and
        appends the results from the request made"""

        response = requests.get(self.site, timeout=5)
        now = datetime.datetime.now()
        self.lasttimeupdated = now
        self.time.append(now)
        if response.status_code == 200:  # site available
            self.availability.append(1)
        else:
            self.availability.append(0)
        self.responsetime.append(response.elapsed.total_seconds())

    def alerting(self):
        """Computes the average availability of the
        last two minutes and if there is not an existing
        alert it creates it otherwise if the alert is recovered
        it notifies the user"""
        now = datetime.datetime.now()
        before = now - datetime.timedelta(minutes=2)
        indextostart = self.find_index(before)
        availability = self.availability[indextostart:]
        average = sum(availability) / len(availability)
        if average < 0.8 and self.alert == None:
            self.alert_up(average, now)
        elif average >= 0.8 and self.alert is not None:
            self.alert_gone(self.alert)

    def alert_up(self, average, now):
        """Alerts if the website availability has
        dropped below 80% in the last to minutes"""
        self.alert = Alert(self.site, average, now)
        print(self.alert)

    def alert_gone(self, alert):
        """Alerts that the alert for the website
        is gone"""
        print("Alert given at time {} for website {} being down is not valid anymore."
              "The website is up again at time {}".format(alert.time, alert.site, datetime.datetime.now()))
        self.alert = None

    def find_index(self, before):
        """the first index of self.time whose
        time is in the 10mins window """

        for i, time in enumerate(self.time):
            if time > before:
                return i
        return 0


class Alert():
    def __init__(self, site, availability, time):
        self.site = site  # url of the site
        self.availability = availability  # availability in [0,1]
        self.time = time  # the time of the alert

    def __str__(self):
        return str("Website {} is down. availability={}%, time={}"
                   .format(self.site, self.availability * 100, self.time))

if __name__ == '__main__':
    nrsites = int(input("Please enter the number of sites you want to monitor:\n"))
    Sites=[]
    for i in range(nrsites):
        url = input("Please enter the url of your website (example: https://google.com) \n")
        interval = int(input("Please enter the check interval (in seconds) for the website above \n"))
        Sites.append(Sitereport(url,interval))

    globaltime = datetime.datetime.now()

    print("Initial report: \n")
    for site in Sites:
        site.add_stats()
        site.report_stats(10)
        print()
    time.sleep(10)

    while True:
        # do the report for 10 minutes
        print("Report for the last 10 minutes: \n")
        for site in Sites:
            now = datetime.datetime.now()
            dif = (now - site.lasttimeupdated).total_seconds()  # time since the last update
            if dif > site.checkinterval:
                site.add_stats()
            site.report_stats(10)
            print()
            site.alerting()
            print()

        # now check if 1 minute has passed to do the report for 1h
        currentime = datetime.datetime.now()
        if (currentime - globaltime).total_seconds() > 60:
            print("Report for the last 1 hour: \n")
            for site in Sites:
                site.report_stats(60)
                print()
            globaltime = currentime
            print()
        time.sleep(10)
