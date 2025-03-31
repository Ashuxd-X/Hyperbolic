"""
  ('-.      .-')    ('-. .-.             
  ( OO ).-. ( OO ). ( OO )  /             
  / . --. /(_)---\_),--. ,--. ,--. ,--.   
  | \-.  \ /    _ | |  | |  | |  | |  |   
.-'-'  |  |\  :` `. |   .|  | |  | | .-') 
 \| |_.'  | '..`''.)|       | |  |_|( OO )
  |  .-.  |.-._)   \|  .-.  | |  | | `-' /
  |  | |  |\       /|  | |  |('  '-'(_.-' 
  `--' `--' `-----' `--' `--'  `-----'    
                                         

Simple Hyperbolic Bot that generates and answers questions.
"""

import time
import requests
import logging
from datetime import datetime
import sys
from typing import Optional, List
import random
import json
import os
import base64
import hashlib
from colorama import init, Fore, Style

# Initialize colorama for Windows support
init()

# Hyperbolic API Configuration
HYPERBOLIC_API_URL = "https://api.hyperbolic.xyz/v1/chat/completions"
MODEL = "deepseek-ai/DeepSeek-V3-0324"      # Or specify the required model
MAX_TOKENS = 2048
TEMPERATURE = 0.7
TOP_P = 0.9
DELAY_BETWEEN_QUESTIONS = 30  # delay between questions in seconds
API_TIMEOUT = 60  # Increased timeout to 60 seconds
MAX_RETRIES = 3  # Maximum number of retries for failed requests
RETRY_DELAY = 5  # Delay between retries in seconds

# Question Generation Topics
TOPICS = [
    "Technology", "Science", "History", "Art", "Literature",
    "Philosophy", "Economics", "Politics", "Environment", "Health",
    "Sports", "Entertainment", "Education", "Social Issues", "Innovation"
]

# Question Types and Templates
QUESTION_TYPES = {
    "analysis": [
        "Analyze the impact of {topic} on society.",
        "What are the key factors influencing {topic}?",
        "How has {topic} evolved over time?",
        "What are the main challenges in {topic}?",
        "Analyze the relationship between {topic} and modern life."
    ],
    "prediction": [
        "What will be the future of {topic}?",
        "How might {topic} change in the next decade?",
        "What emerging trends are shaping {topic}?",
        "What innovations are expected in {topic}?",
        "How will {topic} transform in the future?"
    ],
    "comparison": [
        "Compare different approaches to {topic}.",
        "What are the advantages and disadvantages of {topic}?",
        "How does {topic} differ across cultures?",
        "Compare traditional and modern methods in {topic}.",
        "What are the similarities and differences in {topic}?"
    ],
    "evaluation": [
        "Evaluate the effectiveness of {topic}.",
        "What are the pros and cons of {topic}?",
        "How successful has {topic} been?",
        "What are the strengths and weaknesses of {topic}?",
        "Assess the impact of {topic} on society."
    ],
    "explanation": [
        "Explain the concept of {topic}.",
        "How does {topic} work?",
        "What are the fundamental principles of {topic}?",
        "Can you explain the basics of {topic}?",
        "What is the significance of {topic}?"
    ],
    "opinion": [
        "What are your thoughts on {topic}?",
        "Do you think {topic} is beneficial?",
        "What's your perspective on {topic}?",
        "How do you feel about {topic}?",
        "What's your take on {topic}?"
    ],
    "solution": [
        "How can we improve {topic}?",
        "What solutions exist for {topic}?",
        "How can we address challenges in {topic}?",
        "What strategies can enhance {topic}?",
        "How can we optimize {topic}?"
    ],
    "exploration": [
        "Explore the possibilities of {topic}.",
        "What are the potential applications of {topic}?",
        "How can we expand {topic}?",
        "What new directions could {topic} take?",
        "What are the unexplored aspects of {topic}?"
    ]
}

# ANSI color codes
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors"""
    
    def format(self, record):
        # Add timestamp
        record.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Add colors based on log level
        if record.levelno == logging.INFO:
            color = Colors.GREEN
        elif record.levelno == logging.ERROR:
            color = Colors.RED
        elif record.levelno == logging.WARNING:
            color = Colors.YELLOW
        else:
            color = Colors.WHITE
            
        # Format the message
        record.msg = f"{color}{record.msg}{Colors.END}"
        return super().format(record)

def setup_logger() -> logging.Logger:
    """Setup a logger with custom formatting"""
    logger = logging.getLogger('HyperBot')
    logger.setLevel(logging.INFO)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    # Create formatter
    formatter = ColoredFormatter(
        '%(timestamp)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(console_handler)
    
    return logger

# Security layer for visual elements
def _s():
    _x = lambda x: base64.b64decode(x).decode('utf-8')
    _y = lambda x: hashlib.sha256(x.encode()).hexdigest()
    
    _a = "ICBfKCctLSAgICAgIC4tJykgICAgKCctLSAuLS4gICAgICAgICAgICAgIAogIChPTyApLi0uIChPTyApLiAo"
    _b = "T08pICAvICAgICAgICAgICAgIAogLyAuIC0tLiAvKF8pLS0tXF8pLC0tLiAsLS0uICwtLS4gICwtLS4gICwtLS4gICAKIHwgXC0uICBcIC8gICAgIF8gfCB8ICB8IHwgIHwgfCAgfCB8ICAgCi4tJy0nICB8IHxcICA6YC4gIHwgICB8IHwgIHwgfCAgfCB8IC4tJykgCiBcfCB8Li4nIHwgfCAnLi4uYGBgLikgfCAgICAgIHwgfCAgfHwoT08pIAogIHwgIC4tLiAgfC4tLl8pICAgXHwgIHwgLS0uICB8IHwgIHwgfCBgLScvCiAgfCAgfCB8IHxcfCAgICAgIC98ICB8IHwgIHwgfCgnICAtJygvLScgCiAgfCAgfCB8IHxcfCAgICAgIC98ICB8IHwgIHx8KCcgIC0nKC8uLS0nIAogIGAtLScgYC0tJyBgLS0tLScgYC0tJyBgLS0tJSAgYC0tLS0tJSAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAo="
    
    try:
        _c = _x(_a + _b)
        _d = _y(_c)
        # Clean up the ASCII art
        _c = _c.replace('\r', '').replace('\t', '    ')
        # Ensure consistent line breaks and spacing
        _c = '\n'.join(line.rstrip() for line in _c.split('\n'))
        # Add proper spacing at the end
        _c = _c + '\n' + ' ' * 41
        return _c
    except:
        return "Hyperbolic Bot - AI Question Answering System"

def print_banner():
    """Print system information"""
    # ASCII Art Banner
    banner = """
  ('-.      .-')    ('-. .-.             
  ( OO ).-. ( OO ). ( OO )  /             
  / . --. /(_)---\_),--. ,--. ,--. ,--.   
  | \-.  \ /    _ | |  | |  | |  | |  |   
.-'-'  |  |\  :` `. |   .|  | |  | | .-') 
 \| |_.'  | '..`''.)|       | |  |_|( OO )
  |  .-.  |.-._)   \|  .-.  | |  | | `-' /
  |  | |  |\       /|  | |  |('  '-'(_.-' 
  `--' `--' `-----' `--' `--'  `-----'    
                                         
"""
    # Calculate padding to center the banner
    lines = banner.split('\n')
    max_width = max(len(line) for line in lines)
    padding = (80 - max_width) // 2
    
    # Print the banner with padding
    for line in lines:
        print(f"{Colors.CYAN}{' ' * padding}{line}{Colors.END}")
    
    # Calculate the width based on the longest line
    width = 80
    topics_str = ', '.join(TOPICS)
    types_str = ', '.join(QUESTION_TYPES.keys())
    
    # Create information lines
    lines = [
        f"{Colors.CYAN}{'='*width}",
        f"{Colors.BOLD}Hyperbolic Bot - AI Question Answering System{Colors.END}{Colors.CYAN}",
        f"{Colors.WHITE}Model: {MODEL}{Colors.CYAN}",
        f"{Colors.WHITE}Max Tokens: {MAX_TOKENS} | Temperature: {TEMPERATURE} | Top P: {TOP_P}{Colors.CYAN}",
        f"{Colors.WHITE}Delay between questions: {DELAY_BETWEEN_QUESTIONS} seconds{Colors.CYAN}",
        f"{Colors.WHITE}Topics: {topics_str}{Colors.CYAN}",
        f"{Colors.WHITE}Question Types: {types_str}{Colors.CYAN}",
        f"{'='*width}{Colors.END}"
    ]
    
    # Print each line with proper padding
    for line in lines:
        # Calculate padding to center the text
        padding = (width - len(line.replace(Colors.CYAN, '').replace(Colors.WHITE, '').replace(Colors.BOLD, '').replace(Colors.END, ''))) // 2
        print(f"{' ' * padding}{line}")
    print("\n")  # Add some space after banner

def load_api_key() -> str:
    try:
        with open("key.txt", "r", encoding="utf-8") as f:
            # Read all lines and filter out comments and empty lines
            lines = [line.strip() for line in f.readlines() if line.strip() and not line.strip().startswith('#')]
            if not lines:
                raise ValueError("No API key found in key.txt")
            # Get the first non-comment line as the API key
            api_key = lines[0].strip()
            if not api_key:
                raise ValueError("API key is empty")
            return api_key
    except Exception as e:
        logger.error(f"Error reading API key from key.txt: {e}")
        raise

def generate_question(topic: str, question_type: str) -> str:
    """Generate a question using templates and API"""
    try:
        # First try to use a template
        template = random.choice(QUESTION_TYPES[question_type])
        question = template.format(topic=topic)
        
        # Then enhance it using the API
        api_key = load_api_key()
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        prompt = f"""Enhance this question to make it more specific and thought-provoking, but keep it concise:
"{question}"

Make it more engaging but keep it short. Format: Just the enhanced question, nothing else."""

        data = {
            "messages": [{"role": "user", "content": prompt}],
            "model": MODEL,
            "max_tokens": 100,
            "temperature": 0.8,
            "top_p": 0.9
        }
        
        for attempt in range(MAX_RETRIES):
            try:
                response = requests.post(HYPERBOLIC_API_URL, headers=headers, json=data, timeout=API_TIMEOUT)
                response.raise_for_status()
                json_response = response.json()
                enhanced_question = json_response.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
                
                # Clean up the question
                enhanced_question = enhanced_question.replace('"', '').replace("'", "")
                if enhanced_question.endswith('?'):
                    enhanced_question = enhanced_question[:-1]
                enhanced_question = enhanced_question.strip() + "?"
                
                return enhanced_question
            except requests.Timeout:
                if attempt < MAX_RETRIES - 1:
                    logger.warning(f"Question generation timed out. Retrying in {RETRY_DELAY} seconds... (Attempt {attempt + 1}/{MAX_RETRIES})")
                    time.sleep(RETRY_DELAY)
                else:
                    logger.error("Question generation timed out after all retries")
                    return question
            except requests.RequestException as e:
                if attempt < MAX_RETRIES - 1:
                    logger.warning(f"Question generation failed: {e}. Retrying in {RETRY_DELAY} seconds... (Attempt {attempt + 1}/{MAX_RETRIES})")
                    time.sleep(RETRY_DELAY)
                else:
                    logger.error(f"Question generation failed after all retries: {e}")
                    return question
            except Exception as e:
                logger.error(f"Unexpected error in question generation: {e}")
                return question
                
    except Exception as e:
        logger.error(f"Error in question generation: {e}")
        return question  # Return the template question if API fails

def get_response(question: str) -> str:
    for attempt in range(MAX_RETRIES):
        try:
            api_key = load_api_key()
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            data = {
                "messages": [
                    {"role": "system", "content": "You are a concise AI assistant. Always provide very short, 1-2 line answers. Be direct and to the point."},
                    {"role": "user", "content": f"{question}\n\nProvide a very short, 1-2 line answer."}
                ],
                "model": MODEL,
                "max_tokens": 100,  # Reduced from 2048 to encourage brevity
                "temperature": TEMPERATURE,
                "top_p": TOP_P
            }
            logger.info(f"Sending request to {Colors.CYAN}Hyperbolic API{Colors.END}")
            response = requests.post(HYPERBOLIC_API_URL, headers=headers, json=data, timeout=API_TIMEOUT)
            response.raise_for_status()
            json_response = response.json()
            answer = json_response.get("choices", [{}])[0].get("message", {}).get("content", "No answer").strip()
            
            # Clean up the answer to ensure it's short
            if len(answer.split('\n')) > 2:
                answer = answer.split('\n')[0] + " " + answer.split('\n')[1]
            
            return answer
        except requests.Timeout:
            if attempt < MAX_RETRIES - 1:
                logger.warning(f"Request timed out. Retrying in {RETRY_DELAY} seconds... (Attempt {attempt + 1}/{MAX_RETRIES})")
                time.sleep(RETRY_DELAY)
            else:
                logger.error("Request timed out after all retries")
                raise
        except requests.RequestException as e:
            if attempt < MAX_RETRIES - 1:
                logger.warning(f"Request failed: {e}. Retrying in {RETRY_DELAY} seconds... (Attempt {attempt + 1}/{MAX_RETRIES})")
                time.sleep(RETRY_DELAY)
            else:
                logger.error(f"Request failed after all retries: {e}")
                raise
        except Exception as e:
            logger.error(f"Unexpected error in API request: {e}")
            raise

def save_question_history(question: str, answer: str, topic: str, question_type: str):
    """Save question and answer to history file"""
    try:
        history = []
        if os.path.exists('question_history.json'):
            with open('question_history.json', 'r', encoding='utf-8') as f:
                history = json.load(f)
        
        history.append({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'topic': topic,
            'question_type': question_type,
            'question': question,
            'answer': answer
        })
        
        with open('question_history.json', 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
            
        logger.info(f"Saved question to {Colors.CYAN}question_history.json{Colors.END}")
    except Exception as e:
        logger.error(f"Error saving question history: {e}")

def main():
    # Print banner
    print_banner()
    
    question_count = 0
    used_combinations = set()  # Track used topic-type combinations
    
    while True:
        # Generate a new question
        topic = random.choice(TOPICS)
        question_type = random.choice(list(QUESTION_TYPES.keys()))
        
        # Check if this combination has been used recently
        combination = (topic, question_type)
        if combination in used_combinations:
            # Try to find an unused combination
            available_combinations = [(t, qt) for t in TOPICS for qt in QUESTION_TYPES.keys()]
            available_combinations = [c for c in available_combinations if c not in used_combinations]
            
            if available_combinations:
                combination = random.choice(available_combinations)
                topic, question_type = combination
            else:
                # Reset used combinations if all have been used
                used_combinations.clear()
        
        used_combinations.add(combination)
        
        logger.info(f"{Colors.BOLD}Generating {Colors.CYAN}{question_type}{Colors.END} question about {Colors.CYAN}{topic}{Colors.END}")
        
        question = generate_question(topic, question_type)
        question_count += 1
        
        logger.info(f"{Colors.BOLD}Question #{question_count}:{Colors.END} {question}")
        try:
            answer = get_response(question)
            logger.info(f"{Colors.GREEN}Answer:{Colors.END} {answer}")
            
            # Save to history
            save_question_history(question, answer, topic, question_type)
        except Exception as e:
            logger.error(f"Error getting response for question: {question}\n{e}")
        
        logger.info(f"Waiting {Colors.YELLOW}{DELAY_BETWEEN_QUESTIONS}{Colors.END} seconds before next question...")
        time.sleep(DELAY_BETWEEN_QUESTIONS)

if __name__ == "__main__":
    logger = setup_logger()
    main()