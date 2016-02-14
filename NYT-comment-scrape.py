#!/usr/bin/env python
# encoding: utf-8
"""
classify.pynytimes_comments

Created by Neal Caren on 2012-04-17.
neal.caren@unc.edu

Takes a times article and returns a list of dictionaries for each item.

Note: Does not use the Times API, but you should use it:
http://developer.nytimes.com/docs/community_api
Also, if you are having trouble with accessing the web, you will get an error message.
"""

import urllib
import json
from time import sleep
import datetime
import sys
from django.utils.encoding import smart_str, smart_unicode #Added by Varun (ARGO Labs) to clean up text-output

def nytimes_comments(article):
    
    article=article.replace(':','%253A') #convert the : to an HTML entity
    article=article.replace('/','%252F') #convert the / to an HTML entity
    offset=0 #Start off at the very beginning
    total_comments=1 #set a fake minimum number of contents
    comment_list=[] #Set up a place to store the results
    while total_comments>offset:
        url='http://www.nytimes.com/svc/community/V3/requestHandler?callback=NYTD.commentsInstance.drawComments&method=get&cmd=GetCommentsAll&url='+article+'&offset='+str(offset)+'&sort=newest' #store the secret URL
        #print url
        #print offset
        sleep(1) #They don't like you to vist the page too quickly so take a one second break before downloading
        file=urllib.urlopen(url).read() #Get the file and read it into a string

        file=file.replace('NYTD.commentsInstance.drawComments(','') #clean the file by removing some clutter at the front end
        file=file[:-2] #clean the file by remvoings some clutter at the back end

        results=json.loads(file,  'iso-8859-1') #load the file as json
        comment_list=comment_list+results['results']['comments']
        if offset==0: #print out the number of comments, but only the first time through the loop
            total_comments=results['results']['totalCommentsFound'] # store the total number of comments
            print 'Found '+str(total_comments)+' comments'

        offset=offset+25 #increment the counter
        
    return comment_list #return the list back


'''
A sample of what it does.
You probably want to run it over a loop of articles. 
You might also store the fields you want in a CSV file for later use or export.
'''
#Added by Varun (ARGO Labs) to accept commandline args
article_url=str(sys.argv[1])
print article_url
comments=nytimes_comments(article_url)


for comment in comments: #loop through the list
#Added by Varun (ARGO Labs) to capture replies and print out comment fields.
    if comment['replyCount']>0:
        for reply in comment['replies']:
            print smart_str(reply['commentID']),"-R|",smart_str(reply['status']),"|",smart_str(reply['commentSequence']),"|",smart_str(reply['userID']),"|",smart_str(reply['userDisplayName']),"|",smart_str(reply['userLocation']),"|",smart_str(reply['userTitle']),"|",smart_str(reply['userURL']),"|",smart_str(reply['commentTitle']),"|",smart_str(reply['commentBody']),"|",datetime.datetime.fromtimestamp(int(smart_str(comment['createDate']))).strftime('%Y-%m-%d %H:%M:%S'),"|",datetime.datetime.fromtimestamp(int(smart_str(comment['updateDate']))).strftime('%Y-%m-%d %H:%M:%S'),"|",datetime.datetime.fromtimestamp(int(smart_str(comment['approveDate']))).strftime('%Y-%m-%d %H:%M:%S'),"|",smart_str(reply['recommendations']),"|",smart_str(reply['editorsSelection']),"|",smart_str(reply['commentType']),"|",smart_str(reply['trusted']),"|",smart_str(reply['recommendedFlag']),"|",smart_str(reply['reportAbuseFlag']),"|",smart_str(reply['permID']),"|",smart_str(reply['timespeople']),"|",smart_str(reply['sharing'])
    print smart_str(comment['commentID']),"|",smart_str(comment['status']),"|",smart_str(comment['commentSequence']),"|",smart_str(comment['userID']),"|",smart_str(comment['userDisplayName']),"|",smart_str(comment['userLocation']),"|",smart_str(comment['userTitle']),"|",smart_str(comment['userURL']),"|",smart_str(comment['commentTitle']),"|",smart_str(comment['commentBody']),"|",datetime.datetime.fromtimestamp(int(smart_str(comment['createDate']))).strftime('%Y-%m-%d %H:%M:%S'),"|",datetime.datetime.fromtimestamp(int(smart_str(comment['updateDate']))).strftime('%Y-%m-%d %H:%M:%S'),"|",datetime.datetime.fromtimestamp(int(smart_str(comment['approveDate']))).strftime('%Y-%m-%d %H:%M:%S'),"|",smart_str(comment['recommendations']),"|",smart_str(comment['editorsSelection']),"|",smart_str(comment['commentType']),"|",smart_str(comment['trusted']),"|",smart_str(comment['recommendedFlag']),"|",smart_str(comment['reportAbuseFlag']),"|",smart_str(comment['permID']),"|",smart_str(comment['timespeople']),"|",smart_str(comment['sharing'])
