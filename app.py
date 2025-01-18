import streamlit as st

from crewai import Agent, Task,LLM,Crew,Process
from pydantic import BaseModel, Field
from datetime import date, datetime, timedelta
from typing import List
import re

llm = LLM(
    model="groq/llama3-70b-8192",
    temperature=0.2,
)

# Define Pydantic model for structured search data
class UserSearchData(BaseModel):
    query: str = Field(..., description="The user's search query.")
    timestamp: datetime = Field(..., description="The timestamp of the search (YYYY-MM-DD HH:MM:SS).")
    
# Define Pydantic model for the research output
class PersonalizedContent(BaseModel):
    topic_overview: str = Field(..., description="Brief introduction to the topic, including its relevance and importance.")
    key_considerations: dict = Field(...,description="Factors to consider when making decisions or exploring the topic.")
    recent_trends: dict = Field(..., description="Latest updates, trends, or advancements in the given topic.")
    how_to_choose: dict = Field(..., description="Step-by-step guide or criteria to make informed decisions related to the topic.")
    additional_resources: dict = Field(..., description="Links, references, or suggestions for further exploration.")
    conclusion: str = Field(...,description="Summary of the content with actionable takeaways.")
    
# Define the research agent
research_agent = Agent(
    role="Personalized Content Researcher",
    goal="""Research and compile personalized content based on a list of user search queries from the past 10 days, prioritizing recent context and avoiding duplicate queries. Deliver the output in a structured format. the overall out can be between 1000-1500 words""",
    backstory="""You are an experienced researcher specializing in personalized content creation. You are adept at extracting relevant information from various sources and synthesizing it into a structured and engaging format. You prioritize recent information and avoid redundancy.""",
    verbose=True,  # Set to False in production
    llm=llm  # Your LLM instance (e.g., from Groq)
)

# Define the research task
research_task = Task(
    description="""Research and generate personalized content based on comma-separated user search queries from the past 10 days. Prioritize recent searches and avoid duplicates. Format the output according to the provided template. {query}""",
    expected_output="""The output should be a structured dictionary containing personalized content based on the user's search history. The structure should follow the ResearchOutput Pydantic model. each section should have 200 words. Consider the recency of searches, giving more weight to recent queries. Avoid repeating information derived from duplicate queries.""",
    output_pydantic=PersonalizedContent,
    agent=research_agent
)

# Define the research task (Modified)
research_task_2 = Task(
    description="""Research and generate personalized content based on the provided list of user search queries from the past 10 days. Prioritize recent searches and avoid duplicates. Synthesize the information into a single comprehensive output, formatting it according to the PersonalizedContent Pydantic model. Aim for an output between 1000-1500 words.here is the research query {query} """,
    expected_output="""The output should be a single structured dictionary conforming to the PersonalizedContent Pydantic model, containing personalized content synthesized from all provided user search queries. Consider the recency of searches, giving more weight to recent queries. Avoid repeating information derived from duplicate queries. The total output should be between 1000-1500 words.""",
    output_pydantic=PersonalizedContent,
    agent=research_agent
)


research_crew = Crew(
    agents=[research_agent],
    tasks=[research_task],
    process=Process.sequential
)



st.title("Personalized Content Generator")

sample_inputs = {
    "Productivity Focus": "2024-10-26 10:00:00 best productivity apps, 2024-10-25 12:00:00 how to manage time effectively, 2024-10-27 09:00:00 best productivity apps, 2024-10-20 15:00:00 learn python programming, 2024-10-28 11:00:00 how to build good habits",
    "Tech Enthusiast": "2024-10-27 14:00:00 new iphone release date, 2024-10-26 18:00:00 best noise cancelling headphones 2024, 2024-10-25 10:00:00 latest gaming laptops, 2024-10-28 08:00:00 electric cars review",
    "Travel Planner": "2024-10-28 16:00:00 best travel destinations in europe, 2024-10-27 11:00:00 cheap flights to japan, 2024-10-26 09:00:00 all inclusive resorts in mexico, 2024-10-25 13:00:00 travel tips for southeast asia"
}
search_inputs_string = "best noise cancelling headphones 2024, new iphone release date, comparison between RTX 4080 and 4090, latest MacBook Pro specs, best mechanical keyboards for gaming, AI powered photo editing software, virtual reality headset reviews, smart home automation systems, wireless charging pad for multiple devices, best deals on 4k TVs, new android phone releases, portable bluetooth speakers with long battery life, gaming laptop under $1500, best cybersecurity software for home use, cloud storage comparison, how to build a gaming pc, best vpn services for streaming, smartwatches with fitness tracking, drone photography tips, 3d printing for beginners"

search_input_list = search_inputs_string.split(",")

# input_option = st.selectbox("Select a sample input or enter your own:", list(sample_inputs.keys()) + ["Enter Custom Input"])
input_option = st.selectbox("Select a sample input or enter your own:", search_input_list)

if input_option:
    inputs = {"query" : input_option}
else:
    inputs = ""


if st.button("Generate Personalized Content"):
        if inputs:
            with st.spinner("Generating content..."):  # Show a spinner while processing
                try:
                    result = research_crew.kickoff(inputs=inputs)
                    if result:
                      st.subheader("Generated Content:")
                      st.write(f"**Topic Overview:** {result["topic_overview"]}")
                      st.write("---")
                      st.subheader("Key Considerations:")
                      for key, value in result["key_considerations"].items():
                          st.write(f"**{key}:** {value}")
                      st.write("---")
                      st.subheader("Recent Trends:")
                      for key, value in result["recent_trends"].items():
                          st.write(f"**{key}:** {value}")
                      st.write("---")
                      st.subheader("How to Choose:")
                      for key, value in result["how_to_choose"].items():
                          st.write(f"**{key}:** {value}")
                      st.write("---")
                      st.subheader("Additional Resources:")
                      for key, value in result["additional_resources"].items():
                          st.write(f"**{key}:** {value}")
                      st.write("---")
                      st.write(f"**Conclusion:** {result["conclusion"]}")
                    else:
                      st.error("The agent returned no result. Please check your prompt or LLM setup.")
                except Exception as e:
                    st.error(f"An error occurred during content generation: {e}")
        else:
            st.warning("No valid search entries found in the input.")