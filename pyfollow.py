#!/usr/bin/env python3

driver = '/usr/bin/chromedriver' #Path to chromedriver binary
chrome = '/usr/bin/google-chrome-beta' #Path to Chrome binary
user = 'realdonaldtrump' #Track @realdonaldtrump by default

import sys
import os
import configparser
from selenium import webdriver  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options  
from textwrap import fill


config = configparser.ConfigParser()
try:
    config.read(os.getenv('HOME') + '/.pyfollow.conf')
    driver = config['DEFAULT']['driver']
    chrome = config['DEFAULT']['chrome']
    user = config['DEFAULT']['user']
except:
    print('No config file found.')
    chrome = input('Path to Chrome binary: ')
    driver = input('Path to chromedriver binary: ')
    user = input('Twitter user to follow (without @): ')
    config['DEFAULT'] = { 'chrome':chrome, 'driver':driver, 'user':user }
    with open(os.getenv('HOME') + '/.pyfollow.conf', 'w+') as f:
        config.write(f)

try:
    if len(sys.argv) > 1:
        user = sys.argv[1]

    try:
        with open('{}/.pyfollow.last.{}.txt'.format(os.getenv('HOME'), user), 'r') as f:
            last_time = f.read()
    except Exception:
        last_time = '0'

    chrome_options = Options()  
    chrome_options.add_argument("--headless")  
    chrome_options.binary_location = chrome
    driver = webdriver.Chrome(executable_path=driver,   chrome_options=chrome_options)
    driver.get('https://twitter.com/search?f=tweets&vertical=default&q=from%3A%40{}'.format(user))
    tweets = driver.find_elements_by_css_selector('#stream-items-id li')
    tweets.reverse()
    def aprint(text):
        print(fill(' '.join(''.join(char for char in text if ord(char) < 128).split()), 79) + '\n')

    most_recent = '0' 
    no_tweets = True
    for tweet in tweets:
        try:
            time = tweet.find_element_by_css_selector('._timestamp').get_attribute('data-time')
            if int(time) > int(most_recent):
                most_recent = time
            if not int(time) > int(last_time):
                continue
            no_tweets = False
            aprint('{} {} ({})'.format(
                tweet.find_element_by_css_selector('.fullname').text,
                tweet.find_element_by_css_selector('.username').text,
                tweet.find_element_by_css_selector('._timestamp').text
            ))
            aprint(tweet.find_element_by_css_selector('.tweet-text').text)
            try:
                retweet = tweet.find_element_by_css_selector('.QuoteTweet-authorAndText')
                aprint('---Retweeted {} {}---'.format(
                    retweet.find_element_by_css_selector('.QuoteTweet-fullname').text,
                    retweet.find_element_by_css_selector('.username').text
                ).replace('\n', ''))
                aprint(retweet.find_element_by_css_selector('.QuoteTweet-text').text)
            except:
                pass
            print('-' * 79)
        except:
            pass
    driver.close()

    if no_tweets:
        print('No tweets.')
    else:
        try:
            with open('{}/.pyfollow.last.{}.txt'.format(os.getenv('HOME'), user), 'w+') as f:
                f.write(most_recent)
        except Exception:
            print('WARNING: could not save timestamp of last tweet')
except Exception:
    print('ERROR: an unknown error occurred; is the configuration correct, and are you connected to the internet?')
