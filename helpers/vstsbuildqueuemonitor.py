#!/usr/bin/env python3

import requests


class QueueStatusMonitor:
    def __init__(self, teamaccount, key):
        self.vsts_account = teamaccount
        self.apikey = key
        self.lastrequesturi = ''


    def getlastrequesturi(self):
        return self.lastrequesturi

    # TODO: iterate the list of builds and only show red if the first i.e. last run
    # TODO: of the master branch build failed.
    def getqueuelength(self):
        uri = 'https://' + self.vsts_account 
        uri += '.visualstudio.com/DefaultCollection/'
        uri += '_apis/build/queues?'
        uri += 'api-version=1.0'

        self.lastrequesturi = uri 
        
        count = -1 # if unchanged, denotes failure

        try:
            r = requests.get(uri, auth=('', self.apikey), timeout=5)
            if (r.status_code == 200):
                # get count - check for zero and return amber.
                count = r.json()['count']
                

        except:
            pass
            # we swallow all communication errors

        return count
