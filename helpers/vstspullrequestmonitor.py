#!/usr/bin/env python3

import requests
import time


class PullRequestMonitor:
    def __init__(self, teamaccount, teamproject, repo, key):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print (timestamp + ' - creating repo watcher for :' + repo)
        self.vsts_account = teamaccount
        self.vsts_project = teamproject
        self.gitrepo = repo
        self.apikey = key
        self.lastrequesturi = ''


    def getlastrequesturi(self):
        return self.lastrequesturi


    def getpullrequestcount(self):

        uri = 'https://__account__.visualstudio.com/'
        uri += 'defaultcollection/__project__/_apis/git'
        uri += '/repositories/__repo__/'
        uri += 'pullRequests?api-version=1.0'

        uri = uri.replace('__account__',self.vsts_account)
        uri = uri.replace('__project__',self.vsts_project)
        uri = uri.replace('__repo__',self.gitrepo)

        self.lastrequesturi = uri 
        
        count = -1 # if unchanged, denotes failure

        try:
            r = requests.get(uri, auth=('', self.apikey), timeout=5)
            #print (str(r.status_code))
            if (r.status_code == 200):
                # get count - check for zero and return amber.
                count = r.json()['count']
                

        except:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            print (timestamp + ' - error caught interrogating ' + 
        					self.lastrequesturi)
            pass
            # we swallow all communication errors

        #print ("URI: " + self.lastrequesturi)
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print (timestamp + " - PR: " + self.gitrepo + " has " + str(count) +
        		 " pull requests")

        return count
