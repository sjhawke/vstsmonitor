#!/usr/bin/env python3

import time

#from helpers import displayotron
from helpers import displayotronstub as displayotron
from helpers import trafficlights
from helpers import vstsprojectdetails
from helpers import vstspullrequestmonitor
from helpers import vstsbuildstatusmonitor


class StatusApp:
    def __init__(self):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print (timestamp + " - starting monitoring")
        
        self.colourvalues = trafficlights.Colours()

        self.display = displayotron.Display(self.colourvalues)

        h2 = vstsprojectdetails.Hub2ProjectDetails()
        
        self.monitorinterval = h2.getrefreshintervalseconds()
        
        # quick test on start to check that all LEDs are working
        for colour in self.colourvalues.ALL():
            self.display.setcolour(colour)
            time.sleep(0.5)

        
        # build the pull request api watchers
        self.pullrequestmonitors = []
        for repo in h2.getgitrepostowatch():
            prmonitor = vstspullrequestmonitor.PullRequestMonitor(
                                    teamaccount=h2.getvstsaccount(),
                                    teamproject=h2.getteamprojectname(),
                                    repo=repo,
                                    key=h2.getapikey())
            self.pullrequestmonitors.append(prmonitor)

        # construct the build results api watchers
        self.buildmonitors = []       
        for buildid in h2.getbuildstowatch():
            monitor = vstsbuildstatusmonitor.VstsBuildStatusMonitor(
                buildid=buildid,
                colours=self.colourvalues,
                teamaccount=h2.getvstsaccount(),
                teamproject=h2.getteamprojectname(),
                key=h2.getapikey())
            self.buildmonitors.append(monitor)


    def getStatusOfPullRequests(self):
        """
        Get pull request count for all repositories that we are given
        in the project details in the constructor.
        Aggregate the results. return of -1 means failure and 
        when that happens we indicate that error.
        """
        pullrequestsopen = 0
        
        for prqmonitor in self.pullrequestmonitors:
            prcount = prqmonitor.getpullrequestcount()
            # -1 denotes a problem getting the data for this repo
            if(prcount >= 0):
                pullrequestsopen += prcount
            else:
                pullrequestsopen = -1
                break

        if (pullrequestsopen >= 0):
            paddedvalue = str(pullrequestsopen) + \
                            (' ' * (6 - len(str(pullrequestsopen))))
            message = "Open PRs: " + paddedvalue
        else:
            message = "Open PRs: n/a   "

        return message


    def getStatusofBuilds(self):
        """
        logic here queries builds using adapter objects in an array
        then sets the status message and the overall result colour
        to use to backlight the LCD display.
        Any build failure => RED
        Any errors getting data => AMBER
        No errors => GREEN
        Message shows build name and details of person who broke it if
        there was a build failure for all builds where this is the case.
        Message is otherwise self explanatory.
        """
        failingbuilds = ""
        failingcount = 0
        colours = self.colourvalues
        summarystatus = colours.GREEN()

        for monitor in self.buildmonitors:
            status = monitor.getstatus()

            if (status == colours.RED()):
                summarystatus = colours.RED()
                failingbuilds += monitor.getbuildname() + ":"
                failingbuilds += monitor.getbreaker() + " "
                failingcount += 1

            elif (status == colours.GREEN() and
                    summarystatus == colours.GREEN()):
                summarystatus = colours.GREEN()

            elif (status == colours.AMBER() and
                    summarystatus == colours.GREEN()):
                summarystatus = colours.AMBER()
        
        if (len(failingbuilds) > 0):
            message = failingbuilds
        elif (summarystatus == colours.AMBER()):
            message = ' ' * 16 + " Network Error"
        else:
            message = ' ' * 16 + " ALL BUILDS OK"

        return summarystatus, message


    def run(self):
        colours = self.colourvalues
        # try / except allows us to loop forever until ^C is pressed
        try:
            while (True):
                message = self.getStatusOfPullRequests()
                
                summarystatus, buildmessage = self.getStatusofBuilds()

                # if the build succeeded we are happy with the PR count
                # and build success message
                displaymessage = message + buildmessage

                # if a build has failed we need all 3 lines to show
                # the failure message - perhaps we should truncate
                # at 3x16 ?
                if (summarystatus != colours.GREEN()):
                    displaymessage = buildmessage[:48]

                #self.display.setbarlevel(failingcount / 
                #                           len(h2.getbuildstowatch()))
                self.display.setcolour(summarystatus)
                self.display.settext(displaymessage)
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                print (timestamp + " - " +
                    "message: #" + displaymessage + "# " + summarystatus)
                print (timestamp + ' - ' + 
                       "message: #" +
                       '1' * 16 + '2' * 16 + '3' * 16)
                
                time.sleep(self.monitorinterval)

        except Exception as e:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            print (timestamp + " - " + e)
            pass

        finally:
            self.display.clear()


def main():
    app = StatusApp()
    app.run()


if (__name__ == "__main__"):
    main()

