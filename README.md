# Website-Monitoring
Running:
1) Create a new environment: 
        - $ pip install virtualenv
        - $ virtualenv mypython
2) Activate the new environment:
        - for MacOS/Linux: $ source mypython/bin/activate
        - for Windows: $ mypthon\Scripts\activate
3) Install the packages:
        -$ pip install nose2
        -$ pip install requests
4) To run the website monitor: python ./{path_to_file}/websitemonitor.py
5) To run the testing alerting: python3 -m nose2

Packages used:
1) unittest
2) statistics
3) datetime
4) time
5) requests

# General Structure

The main class is the Sitereport which contains the whole information for a site starting with the site address (given by the user), its checkinterval (given by the user), its availability at every respective time, its response time at every measurement, an Alert object which represents whether the site has triggered an alert / has recovered from it as well as a list of all the alerts triggered by the website. This class contains the method for statistics computation (availability, max response time, average response time of the site) , statistics log (to update the statistics depending on the latest observations) as well as a method to verify if any threshold is crossed in order to raise/recover an alert. There is also another class called Alert which keeps the essential information of an alert (i.e the site of the alert, the time of the alert and the availability when the treshhold was crossed. The rest is done by the __main__ of the program which after the input is taken from the user, creates Sitereport instances for each website entered, and with the help of a loop for each 10s each website report is given, for each timeinterval the websites stats are updated (more clarifications on this on the Improvments section), for each update of the website stats alerts are verified if they are triggered or not and for each 1 minute the 1 hour report is given. Note: there are quite a few clarifications on comments in the code.

# Improvements
There is always room for improvement, unless proven otherwise. In this case i think the architecture of the program is quite well designed however, there are a few points which i think can be improved/adapted depending on a more specific usage of the program.
1) For the moment, the information/alerts/report is just printed in the stdout. An improvement can be adopting the program to save the information printed in a file, database or a data structure in the program depending on the scale of the usage. 
2) A more graceful exit of the program when the user decides to do so.
3) Another way of handling the checkintervals of the websites. In the current implementation, the websites' statistics will be updated approximately in each closest number bigger than the checkinterval that is divisibile by 10 (i.e checkinterval=15 it will be updated each approximately 20 seconds). This is due to the fact that the program is set to sleep for 10 seconds in each big iteration. As a matter of fact this was a personal choice which I did (rather than a flow of the program) as I believed it was a fair trade off between a slight loss in the accuracy of the interval check and a good save in resources considering that the program sleeps and doesn't run at all moments. Nonetheless, as I said before, thanks to the architechture design, updating each website's stats at the exact proper interval is possible. I went ahead and offered an implementation of this case which is found commented at the end of websitemonitor.py.
4) As alerts are quite important and can be missed by an unattentive user, sending an email / creating a pop up window (part of gui) every time there is an alert might be a good solution. The design of my code allows such adaption as well.
5) Improvements can be done on the visual side as well, in order to have better visual on the output of the program. 
