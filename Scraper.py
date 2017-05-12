import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Chrome()
# Uncomment this line to set the new browser windows out of sight
# browser.set_window_position(-2000, -2000)

base_url = "https://twitter.com/search?q="
# Change this to the appropriate query,
# Remove search?q= if you want to crawl a profile
query = "FinalFour"
url = base_url + query

# You might want to chose , as your separator but
# keep in mind that , appear in text so that might
# mess your columns
column_separator = ","
tags_separator = '|'

# Start browser and wait 1 sec to load
browser.get(url)
time.sleep(1)

# Get the main "body" and set the number of tweets
body = browser.find_element_by_tag_name('body')
num_of_tweets = 100

# While loop to gather the desirable amount of tweets
prev_len = 0
strikes = 0
while True:

    for _ in range(5):
        body.send_keys(Keys.PAGE_DOWN)
        # Feel free to change the waiting time between PAGE_DOWN
        time.sleep(1)

    tweets = browser.find_elements_by_class_name('content')
    if len(tweets) > num_of_tweets:
        break
    # check if enough number of tweets
    if prev_len < len(tweets):
        strikes = 0
    if prev_len == len(tweets):
        strikes += 1
    if strikes == 3:
        break
    prev_len = len(tweets)


# Counter in order to write exactly the desired number of tweets
counter = 0

with open(query+"_twitter_data.csv", 'w', errors='ignore') as f:
    f.write("Username" + column_separator + "Text" + column_separator + "Reply"\
            + column_separator + "Retweet" + column_separator + "Favourite"\
            + column_separator + "RefUsers" + column_separator + "Hashtags\n")

    for tweet in tweets:
        if counter == num_of_tweets:
            break
        user = tweet.find_element_by_class_name('username').text
        # remove , and new line
        text = tweet.find_element_by_class_name('tweet-text').text.replace('\n', ' ').replace(',', ' ')
        stats = tweet.find_elements_by_class_name('ProfileTweet-actionCountForPresentation')

        reply = stats[0].text
        if len(reply) == 0:
            reply = '0'

        retweet = stats[1].text
        if len(retweet) == 0:
            retweet = '0'

        favourite = stats[3].text
        if len(favourite) == 0:
            favourite = '0'

        ref_users = ''
        for user_ref in tweet.find_elements_by_class_name('twitter-atreply'):
            ref_users += user_ref.text + tags_separator
        ref_users = ref_users[:-len(tags_separator)]
        if len(ref_users) == 0:
            ref_users = '-'

        hashtags = ''
        for hashtag in tweet.find_elements_by_class_name('twitter-hashtag'):
            hashtags += hashtag.text + tags_separator
        hashtags = hashtags[:-len(tags_separator)]
        if len(hashtags) == 0:
            hashtags = '-'

        line = user + column_separator + text + column_separator + reply \
               + column_separator + retweet + column_separator + favourite \
               + column_separator + ref_users + column_separator + hashtags + '\n'
        f.write(line)
        counter += 1


browser.close()
