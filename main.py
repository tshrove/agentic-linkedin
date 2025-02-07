import os
import langchain_openai
from typing import Literal
from openai import OpenAI
from x_api_client import XApiClient
from langgraph.graph import Graph, START, END
from langchain_core.prompts import PromptTemplate
from linkedin_api.clients.restli.client import RestliClient

# Load API keys from environment variables
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
ME_RESOURCE = "/me"
UGC_POSTS_RESOURCE = "/ugcPosts"
POSTS_RESOURCE = "/posts"
API_VERSION = "202302"


def get_latest_ai_news(_input: str) -> str:
    try:
        messages = [
            {
                "role": "user",
                "content": ("Get the top 5 lastest AI news from today."),
            },
        ]
        _client = OpenAI(
            api_key=PERPLEXITY_API_KEY, base_url="https://api.perplexity.ai"
        )

        _response = _client.chat.completions.create(
            model="sonar-pro",
            messages=messages,
        )
        return _response.choices[0].message.content
    except Exception as e:
        print("Error fetching news:", e)
        raise e


def select_top_stories(news: str) -> str:
    """
    Select the best 5 stories from the news list.

    For simplicity, we choose the first five items.
    """
    top_stories = news
    return top_stories


def create_x_post(top_stories: str) -> str:
    # Build a prompt that includes the top stories
    prompt = (
        """{question}:\n\n
    The post should be professional, informative, and engaging for a tech-savvy audience.
    \n\n --- Stories Start Here --- \n\n"""
        + top_stories
        + """ \n\n --- Stories Stop Here --- \n\n"""
    )
    template_prompt = PromptTemplate.from_template(prompt)

    llm = langchain_openai.OpenAI(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_organization=os.getenv("OPENAI_ORGANIZATION_ID"),
    )
    llm_chain = template_prompt | llm
    output = llm_chain.invoke(
        "Given the stories below, write a professional LinkedIn post that is concise and engaging for a tech-savvy audience."
    )
    return output


def clean_up_the_post(post: str) -> str:
    # Remove any unwanted characters
    post = post.replace("\n", " ")
    post = post.replace("\t", " ")
    post = post.replace("\r", " ")
    post = post.replace("  ", " ")
    post = post.strip()

    # Remove non-ASCII characters
    post = post.encode("ascii", "ignore").decode("ascii")

    return post
def switch_between_linkedin_and_twitter(post: str) -> Literal["LinkedIn", "X"]:
    return "X"

def post_to_x(post: str) -> str:
    try:
        print("X post:")
        # client = XApiClient(
        #     consumer_key=os.environ.get("X_CONSUMER_API_KEY"),
        #     consumer_secret=os.environ.get("X_CONSUMER_API_KEY_SECRET"),
        #     access_token=os.environ.get("X_ACCESS_TOKEN"),
        #     access_token_secret=os.environ.get("X_ACCESS_TOKEN_SECRET"),
        # )
        # if client.post_tweet(post):
        #     print("Tweet posted successfully.")
        # else:
        #     print("Failed to post tweet.")
    except Exception as e:
        print("Error posting to LinkedIn:", e)
        raise e


def post_to_linkedin(post: str) -> str:
    try:
        print("LinkedIn post:")
        # client = RestliClient()
        # ugc_posts_create_response = client.create(
        #     resource_path=UGC_POSTS_RESOURCE,
        #     entity={
        #         "author": "urn:li:person:78j8u43rgt79h9",
        #         "lifecycleState": "PUBLISHED",
        #         "specificContent": {
        #             "com.linkedin.ugc.ShareContent": {
        #                 "shareCommentary": {
        #                     "text": "Sample text post created with /ugcPosts API"
        #                 },
        #                 "shareMediaCategory": "NONE",
        #             }
        #         },
        #         "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
        #     },
        #     access_token=LINKEDIN_ACCESS_TOKEN,
        # )
        # print(
        #     f"Successfully created post using /ugcPosts: {ugc_posts_create_response.entity_id}"
        # )
    except Exception as e:
        print("Error posting to LinkedIn:", e)
        raise e


def main():
    # Initialize a new LangGraph
    graph = Graph()

    # Add nodes to the graph.
    graph.add_node("NewsFetcher", get_latest_ai_news)
    graph.add_node("TopStoriesSelector", select_top_stories)
    graph.add_node("LinkedInPostCreator", create_x_post)
    graph.add_node("CleanUpThePost", clean_up_the_post)
    graph.add_node("LinkedIn", post_to_linkedin)
    graph.add_node("X", post_to_x)

    # Connect nodes so that:
    # NewsFetcher -> TopStoriesSelector -> LinkedInPostCreator -> LinkedInPoster
    graph.add_edge(start_key=START, end_key="NewsFetcher")
    graph.add_edge(start_key="NewsFetcher", end_key="TopStoriesSelector")
    graph.add_edge(start_key="TopStoriesSelector", end_key="LinkedInPostCreator")
    graph.add_edge(start_key="LinkedInPostCreator", end_key="CleanUpThePost")
    graph.add_conditional_edges("CleanUpThePost", switch_between_linkedin_and_twitter)
    graph.add_edge(start_key="LinkedIn", end_key=END)
    graph.add_edge(start_key="X", end_key=END)

    # Run the graph to execute the pipeline.
    _app = graph.compile()

    # Start the process by providing an initial input (the prompt is not used by the API call).
    final_output = _app.invoke("Fetch latest AI news")
    # graph.set_input(node_name="NewsFetcher", input_data="Fetch latest AI news")

    # Retrieve and print the final output from the LinkedInPoster node.
    # final_output = graph.get_output("LinkedInPoster")
    print("Final Output:", final_output)


if __name__ == "__main__":
    main()
