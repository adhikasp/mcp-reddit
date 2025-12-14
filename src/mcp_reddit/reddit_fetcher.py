import os
from typing import Optional
from redditwarp.ASYNC import Client
from redditwarp.models.submission_ASYNC import LinkPost, TextPost, GalleryPost
from fastmcp import FastMCP
import logging

mcp = FastMCP("Reddit MCP")

REDDIT_CLIENT_ID=os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET=os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_REFRESH_TOKEN=os.getenv("REDDIT_REFRESH_TOKEN")

CREDS = [x for x in [REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_REFRESH_TOKEN] if x]

client = Client(*CREDS)
logging.getLogger().setLevel(logging.WARNING)

@mcp.tool()
async def search_reddit(
    query: str,
    time: str = "week",
    subreddit: str = "",
    limit: int = 10,
    max_content_length: int = 2000,
    post_type_filter: str = "text",
) -> str:
    """
    Search for Reddit submissions using a query

    Args:
        query: Search query string
        time: Time filter - either: 'all', 'hour', 'day', 'week', 'month', 'year' (default: 'all')
        subreddit: Subreddit name to search in. Use empty string to search all of Reddit (default: '')
        limit: Number of posts to fetch (default: 10)
        max_content_length: Maximum characters for post content (default: 2000)
        post_type_filter: Post type to include (default: 'text')

    Returns:
        Human readable string containing list of matching submission information
    """
    try:
        posts = []
        result = client.p.submission.search(sr=subreddit, query=query, time=time)
        count = 0
        async for submission in result:
            if count >= 10:
                break
            post_type = _get_post_type(submission)
            post_content = _get_content(submission)
            if post_content is not None:
                post_content = post_content.strip()
                # Truncate content if it exceeds max_content_length
                if len(post_content) > max_content_length:
                    post_content = post_content[:max_content_length] + "..."
            if (
                post_type == post_type_filter
                and post_content is not None
                and post_content != ''
            ):
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

        return "\n\n".join(posts) if posts else "No results found."

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return f"An error occurred: {str(e)}"

@mcp.tool()
async def fetch_reddit_hot_threads(subreddit: str, limit: int = 10) -> str:
    """
    Fetch hot threads from a subreddit

    Args:
        subreddit: Name of the subreddit
        limit: Number of posts to fetch (default: 10)

    Returns:
        Human readable string containing list of post information
    """
    try:
        posts = []
        async for submission in client.p.subreddit.pull.hot(subreddit, limit):
            post_info = (
                f"Title: {submission.title}\n"
                f"Score: {submission.score}\n"
                f"Comments: {submission.comment_count}\n"
                f"Author: {submission.author_display_name or '[deleted]'}\n"
                f"Type: {_get_post_type(submission)}\n"
                f"Content: {_get_content(submission)}\n"
                f"Link: https://reddit.com{submission.permalink}\n"
                f"---"
            )
            posts.append(post_info)

        return "\n\n".join(posts)

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return f"An error occurred: {str(e)}"

def _format_comment_tree(comment_node, depth: int = 0) -> str:
    """Helper method to recursively format comment tree with proper indentation"""
    comment = comment_node.value
    indent = "-- " * depth
    content = (
        f"{indent}* Author: {comment.author_display_name or '[deleted]'}\n"
        f"{indent}  Score: {comment.score}\n"
        f"{indent}  {comment.body}\n"
    )

    for child in comment_node.children:
        content += "\n" + _format_comment_tree(child, depth + 1)

    return content

@mcp.tool()
async def fetch_reddit_post_content(post_id: str, comment_limit: int = 20, comment_depth: int = 3) -> str:
    """
    Fetch detailed content of a specific post

    Args:
        post_id: Reddit post ID
        comment_limit: Number of top level comments to fetch
        comment_depth: Maximum depth of comment tree to traverse

    Returns:
        Human readable string containing post content and comments tree
    """
    try:
        submission = await client.p.submission.fetch(post_id)

        content = (
            f"Title: {submission.title}\n"
            f"Score: {submission.score}\n"
            f"Author: {submission.author_display_name or '[deleted]'}\n"
            f"Type: {_get_post_type(submission)}\n"
            f"Content: {_get_content(submission)}\n"
        )

        comments = await client.p.comment_tree.fetch(post_id, sort='top', limit=comment_limit, depth=comment_depth)
        if comments.children:
            content += "\nComments:\n"
            for comment in comments.children:
                content += "\n" + _format_comment_tree(comment)
        else:
            content += "\nNo comments found."

        return content

    except Exception as e:
        return f"An error occurred: {str(e)}"

def _get_post_type(submission) -> str:
    """Helper method to determine post type"""
    if isinstance(submission, LinkPost):
        return 'link'
    elif isinstance(submission, TextPost):
        return 'text'
    elif isinstance(submission, GalleryPost):
        return 'gallery'
    return 'unknown'

def _get_content(submission) -> Optional[str]:
    """Helper method to extract post content based on type"""
    if isinstance(submission, LinkPost):
        return submission.permalink
    elif isinstance(submission, TextPost):
        return submission.body
    elif isinstance(submission, GalleryPost):
        return str(submission.gallery_link)
    return None

if __name__ == "__main__":
    mcp.run()
