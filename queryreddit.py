import json
import praw
from praw.models import MoreComments
from datetime import datetime
import redditdata as rd

reddit = praw.Reddit('redditaiscraper', user_agent='redditaiscraper script by thecomputerscientist')

print("Reddit AI scraper\n\n")
print("Scraping commencing...")

total_comment_num = 0

for subreddit_name in rd.subreddit_list:
    print("Gettings posts from: {}".format(subreddit_name))
    numposts = 0
    numcomments = 0
    comments = []
    subreddit = reddit.subreddit(subreddit_name)

    posts = subreddit.hot(limit=1000)

    for submission in posts:
        numposts += 1
        for top_level_comment in submission.comments:
            if isinstance(top_level_comment, MoreComments) or top_level_comment.body == "[removed]" or top_level_comment.score_hidden:
                continue
            numcomments += 1
            comments += [rd.extractInfoFromComment(top_level_comment, submission, subreddit_name)]
        if not isinstance(top_level_comment, MoreComments) and top_level_comment.body != "[removed]"  and not top_level_comment.score_hidden:
            for second_level_comment in top_level_comment.replies:
                if isinstance(second_level_comment, MoreComments) or second_level_comment.body == "[removed]"  or second_level_comment.score_hidden:
                    continue
                numcomments += 1
                comments += [rd.extractInfoFromComment(second_level_comment, submission, subreddit_name)]

    with open('data/comments_' + subreddit_name + '.json', 'w') as f:
        json.dump(comments, f)

    total_comment_num += numcomments
    print("There are {} posts".format(numposts))
    print("There are {} comments".format(numcomments))

print("There are {} comments in total".format(total_comment_num))
