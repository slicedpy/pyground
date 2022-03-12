import praw
import sys
import os
import inspect
from datetime import datetime

#https://praw.readthedocs.io/en/stable/

# Custom libraries for local reporting/logging
import sendNotifier
import logmeplz


# Common use to get the script_nm for logging
script_nm = os.path.basename(__file__)
os.makedirs('comment_archive', exist_ok=True) 

# Estabslish the logging to the local temp file
global temp_file
temp_file = logmeplz.getTMPfile()
logmeplz.feedbackMsg(os.environ.get('USERDOMAIN')+'\\'+os.environ.get('USERNAME')+' - [LOG START]: '+script_nm,tfname=temp_file)



def byDate(elem):
    return elem[1]


def collectRedditComments():

    logmeplz.feedbackMsg('[START] - '+os.path.basename(__file__)+' : '+str(inspect.stack()[0][3]),tfname=temp_file)

    # Script time string for filename, reporting
    time_string = datetime.now().strftime("%Y_%m_%d_%H")

    # enable the encoding for emojis--not all will appear. Here's a tip
    # stop using them. Use your words.
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    current_ids,already_archived,comments_sort  = [],[],[]


    # Initiate the reddit object for the project.
    # Will eventually get more secured---eventually
    reddit = praw.Reddit(
    client_id='<client_id>',
    client_secret='<client_secret>',
    password='<client_passowrd>',
    user_agent='<client user agent>',
    username='<username>'
    )

    reddit_usr = str(reddit.user.me())
    logmeplz.feedbackMsg('[CONNECTED] : Reddit instance successful',tfname=temp_file)


    # Create the comment ids file in case it doesn't exist....
    with open('comment_ids.txt','a+') as outputfile:
        outputfile.write('\n')

    # Load the comments that already have been archived--allows the script to skip over it
    # One thing to consider is whether or not the comment has been edited. We're goin' make
    # the 'assumption' that they aren't....
    with open('comment_ids.txt','r') as outputfile:
        for each in outputfile.readlines():
            already_archived.append(each.replace('\n',''))

    # PRAW as this stupid thing with limits--it's annoying. I figured the way around this
    # is to get the thousand from each of the categories.
    comment_chambers = [
        reddit.redditor(reddit_usr).comments.new(limit=None)
        ,reddit.redditor(reddit_usr).comments.top(limit=None)
        ,reddit.redditor(reddit_usr).comments.controversial(limit=None)
        ,reddit.redditor(reddit_usr).comments.hot(limit=None)
        ]

    cursor_num,new_comments = 0,0
    for comment_elements in comment_chambers:
        for idx,comment in enumerate(comment_elements,cursor_num):
            # If the comment, by its id, is already archived, it'll be skipped over
            # else it will be added to the shoot for archiving. Using try/except
            # to save some steps
            try:
                already_archived.index(comment.id)
            except:
                comments_sort.append([comment.id,str(datetime.fromtimestamp(comment.created_utc)),comment.body.translate(non_bmp_map),comment.subreddit,comment.score])
                current_ids.append(comment.id)
                cursor_num = idx
                new_comments += 1


    # Given that the range is 1,000, it might be overkill to load each day--
    # But it would be interesting to see the come along in the logs seperately
    logmeplz.feedbackMsg('Adding '+str(new_comments)+' comments to archive.',tfname=temp_file)


    # Append to the archive new comments. Oldest at the top, Latest at the bottom
    # In the midst of this comment, decided to make seperate files too...
    with open('comment_archive.txt','a+',encoding='utf-8') as outputfile:
        with open('comment_trips.txt','a+',encoding='utf-8') as output_trips:
            comments_sort.sort(key=byDate)
            for cmt in comments_sort:
                outputfile.write('\n\n'+'-'*30+'COMMENT '+cmt[0]+' '+str(idx)+'-'*30)
                outputfile.write('\n'+' '*40+cmt[1]+' '*36+'\n')
                outputfile.write(str(cmt[2]))
                outputfile.write('\n')

                output_trips.write(','.join([cmt[0],cmt[1],str(len(cmt[2])+1 - len(cmt[2].replace(' ',''))),str(cmt[3]),str(cmt[4])]))
                output_trips.write('\n')
                with open(os.path.join('comment_archive',cmt[1].replace(':','').replace(' ','').replace('-','')+'_'+cmt[0]+'.txt'),'w+',encoding='utf-8') as comment_file:
                    comment_file.write(cmt[1]+'\n')
                    comment_file.write(cmt[2]+'\n\n')
                    comment_file.write(str(len(cmt[2])+1 - len(cmt[2].replace(' ','')))+' words\n')
                    comment_file.write('r/'+str(cmt[3])+' ('+str(cmt[4])+')')
        

    with open('comment_ids.txt','a+') as outputfile:
        for each in current_ids:
            outputfile.write(each+'\n')

    logmeplz.feedbackMsg('[END] - '+os.path.basename(__file__)+' : '+str(inspect.stack()[0][3]),tfname=temp_file)
        

if __name__ == '__main__':
    try:
        sendNotifier.sendOut(3,script_nm,'Collect Reddit Comments')
        collectRedditComments()
        sendNotifier.sendOut(1,script_nm,'Collect Reddit Comments')
    except:
        sendNotifier.sendOut(0,script_nm,'Collect Reddit Comments - CHECK LOGS')
        
