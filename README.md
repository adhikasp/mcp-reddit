[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/adhikasp-mcp-reddit-badge.png)](https://mseep.ai/app/adhikasp-mcp-reddit)

# MCP Reddit Server
[![smithery badge](https://smithery.ai/badge/@adhikasp/mcp-reddit)](https://smithery.ai/server/@adhikasp/mcp-reddit)

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) server that provides tools for fetching and analyzing Reddit content.

<a href="https://glama.ai/mcp/servers/3cg9gdyors"><img width="380" height="200" src="https://glama.ai/mcp/servers/3cg9gdyors/badge" alt="mcp-reddit MCP server" /></a>

## Features

- Fetch hot threads from any subreddit
- Get detailed post content including comments
- Support for different post types (text, link, gallery)

## Installation

### Installing via Smithery

To install Reddit Content for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@adhikasp/mcp-reddit):

```bash
npx -y @smithery/cli install @adhikasp/mcp-reddit --client claude
```

### Manual Installation
```json
{
  "reddit": {
    "command": "uvx",
    "args": ["--from", "git+https://github.com/adhikasp/mcp-reddit.git", "mcp-reddit"],
    "env": {}
  }
}
```

## Usage

Using [mcp-client-cli](https://github.com/adhikasp/mcp-client-cli):

```
$ llm what are latest hot thread in r/victoria3

I'll fetch the latest hot threads from the Victoria 3 subreddit for you.

Tool Calls:
  fetch_hot_threads
  Args:
    subreddit: victoria3


Based on the hot threads, here are the key highlights from the Victoria 3 subreddit:

1. Dev Diary #126 - Update 1.8 Overview
   - Major updates planned for the game, including:
     - Political Movement Rework (Ideological Forces)
     - Discrimination Rework
     - Food Availability, Famines, and Harvest Incidents
     - Additional features like Companies owning buildings and Bulk Nationalization

2. Dev Diary #138 - Pivot of Empire Update
   - Update 1.8 "Masala Chai" has been released
   - Focuses on India with new Journal Entries, Events, and Immersion Pack
   - 10 new achievements added
   - Save games from 1.7.7 are not compatible with 1.8

3. Interesting Community Discussions:
   - A player shared a detailed experience of retaking Constantinople as Greece, highlighting the complex population dynamics
   - Humorous posts about game mechanics, such as investment rights and political movements
   - Various memes and gameplay screenshots showcasing unique game situations

The most upvoted thread is the Dev Diary #126, which provides an in-depth look at the upcoming game mechanics improvements, particularly the reworks to political movements and discrimination systems.

Would you like me to elaborate on any of these points or provide more details about the Victoria 3 update?
``` 
