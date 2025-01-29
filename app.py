from dotenv import load_dotenv
from crewai import Agent, Task, Crew
# Importing crewAI tools
from crewai_tools import (
    DirectoryReadTool,
    FileReadTool,
    WebsiteSearchTool
)
from crewai import LLM
from tweepytwitterclient import TweepyTwitterClient
# from grok_tool import GrokTool
from perplexity_tool import PerplexityTool

# Load environment variables from .env file
load_dotenv('.env')

llm = LLM(
    model="gpt-4o"
)

# Instantiate tools
docs_tool = DirectoryReadTool(directory='./linkedin-posts')
file_tool = FileReadTool()
perplexity_tool = PerplexityTool()
web_rag_tool = WebsiteSearchTool()

# Create agents
researcher = Agent(
    llm=llm,
    role='AI Research Analyst',
    goal='Find the latest news from today in the Artificial Intelligence, AI, and Machine Learning industry.',
    backstory='A Ph.D. in AI that loves to stay up-to-date with the latest AI news, trends, and developments.',
    tools=[perplexity_tool],
    verbose=True,
    function_calling_llm=llm
)

writer = Agent(
    llm=llm,
    role='Content Writer',
    goal='Craft engaging LinkedIn post about the latest AI news from today.',
    backstory='A skilled social media writer with a passion for technology.',
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
    output_file='./linkedin-posts/research_summary.txt'
)

write = Task(
    llm=llm,
    description="Write an engaging LinkedIn post about the latest AI news from today, based on the research analyst’s summary. Draw inspiration from the latest news in the directory.",
    expected_output='A short LinkedIn post formatted in with engaging, informative, and accessible content.',
    agent=writer,
    output_file='linkedin_post.txt',
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
    _client:TweepyTwitterClient = TweepyTwitterClient()
    _client.send_tweet(_output.raw)
else:
    print('No output to tweet.')

