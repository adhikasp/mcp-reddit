
import os
import unittest
from typing import Optional
import asyncio
from redditwarp.ASYNC import Client
from redditwarp.models.submission_ASYNC import LinkPost, TextPost, GalleryPost


class TestRedditAPI(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        REDDIT_CLIENT_ID=os.getenv("REDDIT_CLIENT_ID")
        REDDIT_CLIENT_SECRET=os.getenv("REDDIT_CLIENT_SECRET")
        REDDIT_REFRESH_TOKEN=os.getenv("REDDIT_REFRESH_TOKEN")
        CREDS = [x for x in [REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_REFRESH_TOKEN] if x]
        self.client = Client(*CREDS)

    async def testClientSearch(self):
        result = self.client.p.submission.search(sr = "", query = "no king protest", time="day")
        async for submission in result:
            print(f"Title: {submission.title}")
            print(f"URL: {submission.permalink}")
            ## pull detail post given url above
            print(f"Score: {submission.score}")
            # print(f"Content: {_get_content(submission)}")
            print("-" * 80)

    async def testClientSearch(self):
        posts = []
        result = self.client.p.submission.search(sr="", query="no king protest", time="week")
        count = 0
        async for submission in result:
            if count >= 10:
                break
            post_type = _get_post_type(submission)
            post_content = _get_content(submission)
            if post_content is not None:
                post_content = post_content.strip()
            if post_type == 'text' and post_content is not None and post_content != '':
                post_info = (
                    f"Title: {submission.title}\n"
                    f"Score: {submission.score}\n"
                    f"Comments: {submission.comment_count}\n"
                    f"Author: {submission.author_display_name or '[deleted]'}\n"
                    f"Type: {post_type}\n"
                    f"Content: {post_content}\n"
                    f"Url: {submission.permalink}\n"
                    f"---"
                )
                posts.append(post_info)
                count += 1
        print("\n\n".join(posts) if posts else "No results found.")

def _get_content(submission) -> Optional[str]:
    """Helper method to extract post content based on type"""
    if isinstance(submission, LinkPost):
        return submission.permalink
    elif isinstance(submission, TextPost):
        return submission.body
    elif isinstance(submission, GalleryPost):
        return str(submission.gallery_link)
    return None

def _get_post_type(submission) -> str:
    """Helper method to determine post type"""
    if isinstance(submission, LinkPost):
        return 'link'
    elif isinstance(submission, TextPost):
        return 'text'
    elif isinstance(submission, GalleryPost):
        return 'gallery'
    return 'unknown'

