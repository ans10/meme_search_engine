#This code is uses Reddit API and crawls the reddit subreddit
#Path change the path variable of the directory to store image
import praw
import urllib
import time
import logging
import os
r = praw.Reddit(user_agent='Enter your user agent here')

""" Choose number of posts and what subreddit here """
number_of_images = 5000
subreddit = 'AdviceAnimals'
submissions = r.get_subreddit(subreddit).get_new(limit=int(number_of_images))
path = "C:\\Users\\Abhishek\\Downloads\\allnewanimals\\"


""" Open files where to put images """
logging.basicConfig(filename="redditcrawler.log",level = logging.DEBUG)
start = time.time()
logging.debug('Started')
count = 1
imgcount = 0
for i, sub in enumerate(submissions):
    #if not sub.is_self and sub.url.endswith(".jpg") or sub.url.endswith(".png") or sub.url.endswith(".jpeg"):
    try:
        f = urllib.urlopen(sub.url)
        file_name = sub.url.rsplit("/",1)[-1]
        tempstring = "img_"+file_name
        filepath = os.path.join(path,tempstring)
        with open(filepath, "wb") as imgFile:

            imgFile.write(f.read())
        logging.debug("%s crawled successfully" % sub.url)

        imgcount += 1
        if(imgcount % 10 == 0):
            print imgcount
            percent_complete = (float(imgcount) / float(number_of_images)) * 100.00
            logging.debug("%2d %% done" % int(percent_complete))
        f.close()
    except:
        time.sleep(10)
        logging.debug("Sleeping")
    count = count + 1
finish = time.time()
logging.debug("Finished")



