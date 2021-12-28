#!/usr/bin/env python

import asyncio
import argparse
import feedparser
import os

RHASH = '85facb56a33f34'

async def main():
    print("Starting...")
    parser = argparse.ArgumentParser(description='Watch kafanews feed and post updates to Telegram channel', epilog='Set KAFANEWS_BOT_TOKEN environment variable to use this script')
    parser.add_argument('--channel', help='channel to post updates to', default='@kafanews_com')
    parser.add_argument('--max-backlog', '-m', help='maximum number of items to publish after launch', default=2)
    config = parser.parse_args()
    config.token = os.environ.get('KAFANEWS_BOT_TOKEN')
    if config.token is None or config.token == '':
        print('KAFANEWS_BOT_TOKEN environment variable is not set')
        exit(1)
    
    last_item = None
    # import datetime
    # last_item = (datetime.datetime.now() - datetime.timedelta(days=1)).timetuple()

    while True:
        feed = feedparser.parse('https://kafanews.com/rss/')
        new_entries = feed.entries[:config.max_backlog] \
            if last_item is None \
            else list(filter(lambda entry: entry.published_parsed > last_item, feed.entries))
        if len(new_entries) > 0:
           last_item = new_entries[0].published_parsed
        print(f"Found {len(new_entries)} new entries", flush=True)
        for entry in new_entries[::-1]:
            if should_post(entry.link):
                post(entry)
        await asyncio.sleep(10)   
         

def post(entry):
    print(entry.title, instant_view_link(entry.link), entry.published, flush=True)

def instant_view_link(url: str) -> str:
    return f"https://t.me/iv?rhash={RHASH}&url={url}"

def should_post(url: str) -> bool:
    return True # filter out posts that are not relevant

if __name__ == '__main__':
    asyncio.run(main())
