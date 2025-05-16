from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_community.tools import DuckDuckGoSearchRun
import os
import json

class HotpotQAAgent:
    def __init__(self, model="gpt-3.5-turbo"):
        # Initialize with either OpenAI or a local model
        if os.environ.get("OPENAI_API_KEY"):
            self.llm = ChatOpenAI(
                model=model,
                temperature=0.2,
                api_key=os.environ.get("OPENAI_API_KEY")
            )
        else:
            # Fallback to local Llama model if no OpenAI key
            from langchain_community.llms import LlamaCpp
            self.llm = LlamaCpp(
                model_path="./models/llama-2-7b-chat.Q5_K_M.gguf",
                temperature=0.2,
                max_tokens=2000,
                n_ctx=4096
            )
        
        # Initialize tools
        self.search_tool = DuckDuckGoSearchRun()
        
        # Define tools
        @tool
        def search(query: str) -> str:
            """Search the web for information to help answer the question."""
            return self.search_tool.run(query)
        
        # Create ReAct agent
        react_prompt = PromptTemplate.from_template(
            """You are an AI assistant that answers complex multi-hop questions from the HotpotQA dataset.
            You need to break down the question into steps, search for relevant information, and combine the information to give a final answer.
            
            Examples:
            Question: Which government position was held by the woman who portrayed Corliss Archer in the film Kiss and Tell?
            Thought: I need to find who portrayed Corliss Archer in Kiss and Tell, then find what government position she held.
            Action: search("Who portrayed Corliss Archer in Kiss and Tell film")
            Observation: Shirley Temple played Corliss Archer in the 1945 film Kiss and Tell.
            Thought: Now I need to find what government position Shirley Temple held.
            Action: search("What government position did Shirley Temple hold")
            Observation: Shirley Temple Black (born Shirley Temple; April 23, 1928 – February 10, 2014) was an American actress, singer, dancer, and diplomat who was Hollywood's number one box-office draw as a child actress from 1934 to 1938. She later served as United States ambassador to Ghana and to Czechoslovakia, and as Chief of Protocol of the United States.
            Thought: I have the answer now. Shirley Temple, who portrayed Corliss Archer in Kiss and Tell, held several government positions including US ambassador to Ghana and Czechoslovakia, and Chief of Protocol of the United States.
            Action: Finish[Shirley Temple, who portrayed Corliss Archer in Kiss and Tell, served as United States ambassador to Ghana and to Czechoslovakia, and as Chief of Protocol of the United States.]
            
            {chat_history}
            Question: {input}
            {agent_scratchpad}
            """
        )
        
        tools = [search]
        self.agent = create_react_agent(self.llm, tools, react_prompt)
        self.agent_executor = AgentExecutor(agent=self.agent, tools=tools, verbose=True)
        
        # Sample HotpotQA data for testing
        self.sample_questions = self._load_sample_questions()
    
    def _load_sample_questions(self):
        """Load sample questions from HotpotQA or use defaults if file not available"""
        try:
            with open("data/hotpotqa_sample.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            # Fallback to some default questions
            return [
                "Which government position was held by the woman who portrayed Corliss Archer in the film Kiss and Tell?",
                "Are both Coldplay and The Killers from the same country?",
                "Who released the album that contained the song 'Stylo' first, Gorillaz or Coldplay?"
            ]
    
    def answer_question(self, question):
        """Process a HotpotQA question using ReAct and return an answer"""
        response = self.agent_executor.invoke({"input": question})
        return response["output"]

if __name__ == "__main__":
    agent = HotpotQAAgent()
    
    # Test with sample questions
    for q in agent.sample_questions[:2]:  # Only run first 2 questions to save time
        print(f"\nQuestion: {q}")
        answer = agent.answer_question(q)
        print(f"Answer: {answer}") 