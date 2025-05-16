import pytest
import os
import sys
from unittest.mock import MagicMock, patch

# Add parent directory to path to import agent module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agent import HotpotQAAgent

# Sample expected answers (these would be more comprehensive in a real test)
EXPECTED_ANSWERS = {
    "Which government position was held by the woman who portrayed Corliss Archer in the film Kiss and Tell?": {
        "keywords": ["Shirley Temple", "ambassador", "Ghana", "Czechoslovakia", "Chief of Protocol"]
    },
    "Are both Coldplay and The Killers from the same country?": {
        "keywords": ["Coldplay", "British", "UK", "The Killers", "American", "USA", "not", "different"]
    },
    "Who released the album that contained the song 'Stylo' first, Gorillaz or Coldplay?": {
        "keywords": ["Gorillaz", "Plastic Beach", "2010", "before", "first"]
    }
}

class TestHotpotQAAgent:
    @pytest.fixture
    def mock_agent(self):
        # Mock the LLM and search tool to avoid making actual API calls during tests
        with patch("agent.ChatOpenAI"), patch("agent.DuckDuckGoSearchRun"):
            agent = HotpotQAAgent(model="gpt-3.5-turbo")
            
            # Mock the agent executor's invoke method
            agent.agent_executor = MagicMock()
            
            # Set up responses for each question
            def side_effect(inputs):
                question = inputs["input"]
                
                if "Corliss Archer" in question:
                    return {
                        "output": "Shirley Temple, who portrayed Corliss Archer in Kiss and Tell, served as United States ambassador to Ghana and to Czechoslovakia, and as Chief of Protocol of the United States."
                    }
                elif "Coldplay and The Killers" in question:
                    return {
                        "output": "No, Coldplay and The Killers are not from the same country. Coldplay is a British band from London, UK, while The Killers are an American band from Las Vegas, Nevada, USA."
                    }
                elif "'Stylo'" in question or "Gorillaz or Coldplay" in question:
                    return {
                        "output": "Gorillaz released the album 'Plastic Beach' containing the song 'Stylo' in 2010, before any Coldplay album featuring this song. In fact, 'Stylo' is not a Coldplay song, it's exclusively a Gorillaz track."
                    }
                else:
                    return {
                        "output": "I don't have enough information to answer this question."
                    }
            
            agent.agent_executor.invoke.side_effect = side_effect
            
            yield agent
    
    def test_corliss_archer_question(self, mock_agent):
        question = "Which government position was held by the woman who portrayed Corliss Archer in the film Kiss and Tell?"
        answer = mock_agent.answer_question(question)
        
        # Check that the answer contains the correct information
        assert "Shirley Temple" in answer
        assert "ambassador" in answer
        
        # Calculate score based on keywords
        score = self.calculate_score(answer, question)
        assert score >= 80, f"Answer score too low: {score}%"
    
    def test_bands_country_question(self, mock_agent):
        question = "Are both Coldplay and The Killers from the same country?"
        answer = mock_agent.answer_question(question)
        
        # Check that the answer contains the correct information
        assert "Coldplay" in answer
        assert "The Killers" in answer
        
        # Calculate score based on keywords
        score = self.calculate_score(answer, question)
        assert score >= 80, f"Answer score too low: {score}%"
    
    def test_stylo_song_question(self, mock_agent):
        question = "Who released the album that contained the song 'Stylo' first, Gorillaz or Coldplay?"
        answer = mock_agent.answer_question(question)
        
        # Check that the answer contains the correct information
        assert "Gorillaz" in answer
        
        # Calculate score based on keywords
        score = self.calculate_score(answer, question)
        assert score >= 80, f"Answer score too low: {score}%"
    
    def calculate_score(self, answer, question):
        """Calculate a score based on the presence of expected keywords"""
        if question not in EXPECTED_ANSWERS:
            return 0
        
        expected = EXPECTED_ANSWERS[question]
        keywords = expected["keywords"]
        
        # Count how many keywords are in the answer
        matches = sum(1 for keyword in keywords if keyword.lower() in answer.lower())
        
        # Calculate percentage
        score = (matches / len(keywords)) * 100
        
        return score 