import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM
from crewai_tools import (
    DirectoryReadTool,
    FileReadTool,
    WebsiteSearchTool
)
from x_api_client import XApiClient
from tools import PerplexityTool

# Load environment variables from .env file
load_dotenv('.env')

llm = LLM(
    model="gpt-4o"
)

# Instantiate tools
docs_tool = DirectoryReadTool(directory='./x-posts')
file_tool = FileReadTool()
perplexity_tool = PerplexityTool()
web_rag_tool = WebsiteSearchTool()

# Create agents
researcher = Agent(
    llm=llm,
    role='AI Research Analyst',
    goal='Find the latest and most popular news from today in the Artificial Intelligence industry.',
    backstory='A Ph.D. in AI that loves to stay up-to-date with the latest AI news, trends, and developments.',
    tools=[perplexity_tool],
    verbose=True,
    function_calling_llm=llm
)

writer = Agent(
    llm=llm,
    role='Content Writer',
    goal='Craft engaging Twitter/X post that is less than 280 characters and is interesting to the general public.',
    backstory='You are passionate creative director with a passion for technology and delivery the news in an engaging way.',
    tools=[docs_tool, file_tool],
    verbose=True
)

# Define tasks
research = Task(
    llm=llm,
    description='Find the latest news from today in the Artificial Intelligence, AI, and Machine Learning industry.',
    expected_output='A summary of the top 5 latest developments from today in the Artificial Intelligence, AI, and Machine Learning industry and why it is important.',
    agent=researcher,
    verbose=True,
    output_file='./x-posts/summary.txt'
)

write = Task(
    llm=llm,
    description="Write an engaging X post about from one the research analyst’s articles. Pick one that would be the most interesting.",
    expected_output='A short X post formatted in with engaging, informative, and accessible content that is less than 280 characters.',
    agent=writer,
    output_file='x_post.txt',
)

# Assemble a crew with planning enabled
crew = Crew(
    agents=[researcher, writer],
    tasks=[research, write],
    function_calling_llm=llm,
    planning=True,
    planning_llm=llm
)

# Execute tasks
_output = crew.kickoff()
print(_output.raw)

if _output.raw:
    client = XApiClient(
        consumer_key=os.environ.get("X_CONSUMER_API_KEY"),
        consumer_secret=os.environ.get("X_CONSUMER_API_KEY_SECRET"),
        access_token=os.environ.get("X_ACCESS_TOKEN"),
        access_token_secret=os.environ.get("X_ACCESS_TOKEN_SECRET")
    )
    if client.post_tweet(_output.raw):
        print('Tweet posted successfully.')
    else:
        print('Failed to post tweet.')
else:
    print('No output to tweet.')

