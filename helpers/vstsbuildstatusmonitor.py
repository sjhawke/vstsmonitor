#!/usr/bin/env python3

import time

import requests


class VstsBuildStatusMonitor:
    # limited credentials allow reading build results only/90 days
    buildname = ''
    breaker = ''

    def __init__(self, buildid, colours, teamaccount, teamproject, key):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print (timestamp + ' - creating build watcher for id ' + str(buildid))
        self.buildid = buildid
        self.colours = colours
        self.vsts_account = teamaccount
        self.apikey = key
        self.vsts_project = teamproject
        self.buildnotfoundmessage = '*build not found*'
        self.lastrequesturi = ''


    def getbuildname(self):
        return self.buildname


    def getbreaker(self):
        return self.breaker


    def getlastrequesturi(self):
        return self.lastrequesturi


    def getstatus(self):
        uri = 'https://' + self.vsts_account 
        uri += '.visualstudio.com/DefaultCollection'
        uri += '/' + self.vsts_project + '/'
        uri += '_apis/build/builds?definitions=' + str(self.buildid)
        uri += '&statusFilter=completed'
        #uri += '&reasonFilter=batchedCI'
        uri += '&maxBuildsPerDefinition=30'
        uri += '&$top=30'
        uri += '&api-version=2.0'

        name = ''
        colour = self.colours.AMBER()
        status = '$timestamp$ - Build $id$, \'$name$\' ' \
                 'status is $colour$ (breakers: $breaker$)'

        self.lastrequesturi = uri 
        self.breaker = ''

        try:
            r = requests.get(uri, auth=('', self.apikey), timeout=5)
            if (r.status_code == 200):
                # get count - check for zero and return amber.
                count = r.json()['count']
                if(count == 0):
                    colour = self.colours.AMBER()
                    #print (self.getbuildname() + "  no count")
                else:
                    # loop over all list items checking result and branch
                    for resultslistitem in range(0, count-1):
                        entry = r.json()['value'][resultslistitem]
                        id = entry['id']

                        result = entry['result']
                        branch = entry['sourceBranch']
                        name   = entry['definition']['name']
                        dev    = entry['requestedFor']['displayName']
                        #print (name + " " +  str(id) + " " + branch)

                        if (branch == 'refs/heads/master'):
                            if (result == 'succeeded'):
                                colour = self.colours.GREEN()
                                break
                            elif (result == 'failed'):
                                colour = self.colours.RED()
                                self.breaker = dev
                                break
                            elif (result == 'canceled'):
                                # carry on!
                                continue
                            else:
                                colour = self.colours.AMBER()
                                break
                        else:
                            colour = self.colours.AMBER()

        except:
            pass
            # we swallow all communication errors


        # first time we set to some value / name or missing as appropriate
        if (self.buildname == ''):
            if (name != ''):
                self.buildname = name
            if (self.buildname == ''):
                self.buildname = self.buildnotfoundmessage

        # nth time having never received a valid name, set it if we get one
        if(self.buildname == self.buildnotfoundmessage and name != ''):
            self.buildname = name

        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print(status.replace('$timestamp$', timestamp)
              .replace('$id$', str(self.buildid))
              .replace('$name$', self.buildname)
              .replace('$colour$', colour)
              .replace('$breaker$',self.breaker))

        return colour
