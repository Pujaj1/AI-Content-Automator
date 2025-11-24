from crewai.tools import BaseTool
import feedparser
from typing import Type
from pydantic import BaseModel, Field

# The Google News RSS feed URL, filtered for "AI" topics.
# The query 'ai+breakthroughs+OR+ai+job+market+trends+OR+new+ai+tools' is derived
# from the query your agent was trying to run.
AI_NEWS_RSS_URL = "https://news.google.com/rss/search?q=ai+breakthroughs+OR+ai+job+market+trends+OR+new+ai+tools+when:48h&hl=en-US&gl=US&ceid=US:en"

class NewsFeedInput(BaseModel):
    """Input is a placeholder since the URL is hardcoded to the specific query."""
    dummy_query: str = Field(description="Placeholder. The tool uses a pre-configured Google News RSS feed for AI topics (last 48h). Provide a dummy value like 'fetch news'.")

class GoogleNewsRSS(BaseTool):
    name: str = "Google News RSS Feed"
    description: str = (
        "Reads the latest top 5 news articles on AI breakthroughs, job market trends, "
        "and new tools from a pre-configured Google News RSS feed (last 48 hours). "
        "Returns a structured list of Headline, Source URL, and Summary."
    )
    args_schema: Type[BaseModel] = NewsFeedInput

    def _run(self, dummy_query: str = "fetch news") -> str:
        try:
            feed = feedparser.parse(AI_NEWS_RSS_URL)
            articles = feed.entries[:5] # Takes the top 5 entries

            if not articles:
                return "No recent AI news articles found in the feed."

            formatted_results = []
            for entry in articles:
                # The 'summary' field often contains a snippet or a brief description
                summary = entry.get('summary', 'No summary available.').split(' - ')[0]
                
                formatted_results.append(
                    f"Headline: {entry.title}\n"
                    f"Summary: {summary}\n"
                    f"URL: {entry.link}\n"
                    "---"
                )
            
            return "\n".join(formatted_results)
        
        except Exception as e:
            return f"An error occurred while reading the RSS feed: {e}"