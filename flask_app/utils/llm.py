# Author: Prof. MM Ghassemi <ghassem3@msu.edu>

from email import message
import os
import requests
import time
from typing import Dict, List, Optional
from flask import current_app, session, jsonify
from flask_app import socketio
from .socket_events import process_and_emit_message
# importing database
from .database import database
from langchain.llms.base import LLM
from langchain.schema.runnable import RunnableLambda
from langchain.prompts import PromptTemplate
import ast
import json
from flask_app.utils.a2a_protocol import A2AProtocol, A2AMessage

#--------------------------------------------------
# GLOBAL INSTANCES
#--------------------------------------------------
db = database()

class ChatGPTClient:
    """Client for interacting with OpenAI's ChatGPT API"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = None, max_tokens: int = None, temperature: float = None):
        """Initialize the ChatGPT client
        
        Args:
            api_key: OpenAI API key. If not provided, will try to get from environment variable OPENAI_API_KEY
            model: OpenAI model to use. If not provided, will use config default
            max_tokens: Maximum tokens in response. If not provided, will use config default
            temperature: Response randomness (0.0-1.0). If not provided, will use config default
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
        
        self.base_url = "https://api.openai.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Get configuration values
        self.model       = model       or current_app.config.get('OPENAI_MODEL')
        self.max_tokens  = max_tokens  or current_app.config.get('OPENAI_MAX_TOKENS')
        self.temperature = temperature or current_app.config.get('OPENAI_TEMPERATURE')
    
    def send_message(self, message: str, conversation_history: Optional[List[Dict]] = None, system_prompt: Optional[str] = None) -> Dict:
        """Send a message to ChatGPT and get a response
        
        Args:
            message: The user's message
            conversation_history: List of previous messages in the conversation
            system_prompt: Custom system prompt to define AI behavior (optional)
            
        Returns:
            Dictionary containing the response and metadata
        """
        if conversation_history is None:
            conversation_history = []
        
        # Prepare the messages for the API
        messages = []
        
        # Add system prompt if provided
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        # Add conversation history
        messages.extend(conversation_history)
        
        # Add current user message
        messages.append({"role": "user", "content": message})
        
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature
        }
        
        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            
            # Extract the assistant's response
            assistant_message = result['choices'][0]['message']['content']
            
            return {
                "success": True,
                "response": assistant_message,
                "usage": result.get('usage', {}),
                "model": self.model
            }
            
        except (requests.exceptions.RequestException, KeyError, IndexError) as e:
            return {
                "success": False,
                "error": f"Request or response error: {str(e)}",
                "response": "I'm sorry, I'm having trouble right now. Please try again later."
            }

chat = ChatGPTClient()

# added llm_role parameter
def handle_ai_chat_request(message: str, llm_client: ChatGPTClient = chat, system_prompt: str = None, room: str = 'main', page_content: dict = None, llm_role: str = None, orchestrator_flag: bool = False, web_content: bool = False):
    """
    Handle AI chat requests with LLM and broadcast responses via SocketIO.
    
    Args:
        llm_client: Pre-configured LLM client instance
        message: The user's message to send to the LLM
        system_prompt: Custom system prompt to define AI behavior (optional)
        room: Chat room to emit the AI response to (default: 'main')
        page_content: Dictionary containing page content information (optional)
        llm_role: The role of the LLM to use
        recursion_flag: True if the call is by the Orchestrator
    Returns:
        Response: JSON response with LLM reply or error message
    """
    try:
        # if session.get('pending_validation'):
        #     if message.lower() == 'no':
        #         m = 'Not running this query'
        #         process_and_emit_message(socketio, m, 'ai', 'main')
        #         session['pending_validation'] = None
        #         return jsonify({
        #             'success': True,
        #             'response': m
        #         }), 200
        #     elif message.lower() == 'yes':
        #         message = session['pending_validation']
        #         session['pending_validation'] = None
        #     else:
        #         m = 'Enter yes or no'
        #         process_and_emit_message(socketio, m, 'ai', 'main')
        #         return jsonify({
        #             'success': 'Waiting on human input',
        #             'response': m
        #         }), 200
        # else:
        #     if assess_message_risk(user_string=message):
        #         request_human_validation(user_string=message)
        #         return jsonify({
        #             'success': 'Waiting on human input',
        #             'response': 'Should I go ahead with this database query? Reply with one word YES or NO'
        #         }), 200

        # session['pending_validation'] = None
        LLM_ROLES = db.getLLMRoles()
        # Get conversation history from session if available
        conversation_history = session.get('chat_history', [])
        # add the page content to background context if the role is context expert
        if llm_role and llm_role not in ['HTML Cleaner', 'Content Curator']:
            if llm_role == 'Content Expert' and page_content:
                LLM_ROLES[llm_role]['background_context'] = page_content
            # else:
            #     LLM_ROLES[llm_role]['background_context'] += str(page_content)
            system_prompt = f"You are a senior {llm_role} with experience in {LLM_ROLES[llm_role]['domain']}. {LLM_ROLES[llm_role]['background_context']}. {LLM_ROLES[llm_role]['specific_instructions']}. {LLM_ROLES[llm_role]['few_shot_examples']}"
        else:
            system_prompt = system_prompt or current_app.config.get('OPENAI_SYSTEM_PROMPT')
        
        if llm_role == 'HTML Cleaner':
            system_prompt = """
                            You are a senior HTML cleaning expert specializing in processing and sanitizing text extracted from web pages.
                            Your task is to clean raw HTML or scraped website content and return only the meaningful, human-readable text.
                            I explicitly order you to remove the newline symbol and other unicode from the text. 

                            Follow these rules carefully:
                            1. Remove all navigation menus, headers, footers and sidebars
                            2. Strip out all HTML tags, scripts, styles and newline symbol "\n" from the text.
                            3. Preserve only the main article or body text, including relevant headings, paragraphs, and list items.
                            4. Do NOT alter or rewrite the actual wording or structure of the original content—just clean and extract it.
                            5. Return a single plain-text string as the final output.

                            Let’s think step-by-step to ensure only the essential textual content remains.
                            """
        if llm_role == 'Content Curator':
            system_prompt = """
                            You are an expert in text extraction and summarization. You will be given a Python string 
                            containing a list of dictionaries, where each dictionary includes text from a different source 
                            such as 'experience' or 'document' describing the same person or their projects. 

                            Your task is to:
                            1. Extract and analyze all relevant text about the project or experience described.
                            2. Identify what the person has done — focusing on actions, methodologies, technologies used, and outcomes.
                            3. Combine the information from all sources into a single, coherent paragraph summarizing the work.
                            4. You have to ignore other things that are not related to the content. Be smart about this.
                            5. Ignore metadata fields such as similarity scores, IDs, or hyperlinks unless they provide useful context.
                            6. DO NOT EXCLUDE ANYTHING THAT MAY BE RELEVANT

                            Output requirements:
                            - Write one clear, concise paragraph in plain text (no markdown, bullet points, or headings).
                            - Remove unnecessary punctuation, special characters, and irrelevant details.
                            - The paragraph should professionally describe the person’s contributions and technical impact in the project.
                            """
        result = llm_client.send_message(message, conversation_history, system_prompt=system_prompt)
        
        # this is where it is handling js output
        if result["success"]:

            # update conversation history
            conversation_history.append({"role": "user", "content": message})
            conversation_history.append({"role": "assistant", "content": result["response"]})
            max_history = current_app.config.get('OPENAI_MAX_CONVERSATION_HISTORY')
            if len(conversation_history) > max_history:
                conversation_history = conversation_history[-max_history:]
            session['chat_history'] = conversation_history

            ai_response = result["response"]

            if llm_role == 'Database Read Expert':
                print(ai_response)
                reply = handle_database_read_expert(ai_response, orchestrator_flag)
                if orchestrator_flag and reply:
                    return reply
            elif llm_role == 'Database Write Expert':
                handle_database_write_expert(ai_response)
            elif llm_role == 'Orchestrator Reasoning Agent':
                print(ai_response)
                handle_orchestrator_reasoning(ai_response)
            elif llm_role == 'Orchestrator':
                print(ai_response)
                handle_orchestrator_expert(ai_response)
            elif llm_role == 'Content Expert':
                handle_content_expert(ai_response)
            elif llm_role == 'HTML Cleaner':
                return ai_response
            elif llm_role == 'Content Curator':
                print_message(ai_response)

        return jsonify(result)
        
    except Exception as e:
        print(f"Error in handle_ai_chat_request: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "response": f"An error occurred: {str(e)}"
        }), 500

def print_message(message):
    process_and_emit_message(socketio, message, 'ai', 'main')


def handle_database_read_expert(ai_response, orchestrator_flag=False):
    try:
        query_result = db.query(query=ai_response)
        if orchestrator_flag:
            return query_result
        else:
            if isinstance(query_result, list) and isinstance(query_result[0], dict):
                temp_read_reply = list(query_result[0].values())
                query_result = str(temp_read_reply[0])
        
        # query_result += 'SQL QUERY = ' + ai_response
        print_message(message=query_result)

    except Exception as e:
        query_result = str(e)
        print_message(message=query_result + " Read")

def handle_database_write_expert(ai_response):
    db.query("SELECT setval('skills_skill_id_seq', COALESCE((SELECT MAX(skill_id) FROM skills), 0) + 1, false)")
    db.query("SELECT setval('experiences_experience_id_seq', COALESCE((SELECT MAX(experience_id) FROM experiences), 0) + 1, false)")

    try:
        query_result = eval(ai_response)
        if query_result:
            print_message(message='Operation was successful ' + str(query_result))
        else:
            if 'skills' in ai_response:
                query_result = "Skill inserted into skills table\n"
            elif 'experiences' in ai_response:
                query_result = "Experience inserted into experiences table\n"
            elif 'positions' in ai_response:
                query_result = "Position inserted into positions table\n"
            elif 'users' in ai_response:
                query_result = "User inserted into users table\n"
            elif 'institutions' in ai_response:
                query_result = "Institution inserted into institutions table\n"
            else:
                query_result = "Operation was unsuccessful"
            
            query_result = "Database Modified"
            # query_result += ai_response
            print_message(message=query_result)
    
    except Exception as e:
        query_result = f"Operation was unsuccessful. Error: {e}"
        print_message(message=query_result + " WRITE " + ai_response)

def handle_content_expert(ai_response):
    try:
        print_message(message=ai_response)
    except Exception as e:
        print_message(message='CONTENT EXPERT ' + str(e))

def handle_orchestrator_expert(ai_response):
    try:
        query_result = ""
        function_calls = ast.literal_eval(ai_response)
        web_content_flag = False
        for index, function_call in enumerate(function_calls):
            if web_content_flag:
                reply = handle_ai_chat_request(
                    message=function_call['message'],
                    llm_role=function_call['role'],
                    orchestrator_flag = True,
                    web_content=True
                )
                web_content_flag = False
            else:
                reply = handle_ai_chat_request(
                    message=function_call['message'],
                    llm_role=function_call['role'],
                    orchestrator_flag = True
                )

            if function_call['role'] == 'Database Read Expert':
                from flask_app.utils.web_crawler import WebCrawlerAgent
                query_result += 'Database Read Expert invoked by Orchestrator.\n'
                if reply and len(function_calls) > 1 and index != len(function_call) - 1:
                    print(reply)
                    url = next((d['hyperlink'] for d in reply if 'hyperlink' in d), None)
                    if url:
                        a2a = A2AProtocol()
                        crawler = WebCrawlerAgent(a2a)
                        message_id = a2a.send_request(sender="Orchestrator", recipient='web_crawler_agent', action='crawl_url', params={'url': url})
                        scraping_message = a2a.pending_requests[message_id]
                        response = crawler.handle_a2a_request(scraping_message)
                        if response.params['result']['status'] != 'success':
                            break
                        else:
                            web_content_flag = True
                            continue
                    else:
                        val = list(reply[0].values())[0]
                        if isinstance(val, int) and val > 0:
                            query_result += 'Element already exists.\n'
                            break
                        elif isinstance(val, bool) and val:
                            query_result += 'Element already exists.\n'
                            break
                        elif isinstance(val, str):
                            if val.isnumeric() and int(val) > 0:
                                query_result += 'Element already exists.\n'
                                break
                            elif val.lower() == 'true':
                                query_result += 'Element already exists.\n'
                                break
                elif reply and len(function_calls) == 1:
                    if len(reply) > 3:
                        val = ', '.join(list(reply[i].values())[0] for i in range(len(reply) - 3))
                    else:
                        val = str(list(reply[0].values())[0])
                    query_result += val
                
                elif reply:
                    handle_ai_chat_request(
                        message=str(reply),
                        llm_role='Content Curator'
                    )
                
            elif function_call['role'] == 'Database Write Expert':
                query_result += 'Database Write Expert invoked by Orchestrator.\n'
            
            elif function_call['role'] == 'Content Expert':
                query_result += 'Content Expert invoked by Orchestrator.\n'
        
        print_message(message=str(query_result))
    
    except Exception as e:
        query_result = 'ORCHESTRATOR ' + str(e)
        print_message(message=query_result)

def handle_orchestrator_reasoning(ai_response):
    try:
        reply = handle_ai_chat_request(
                message=ai_response,
                llm_role="Orchestrator",
            )
        
    except Exception as e:
        query_result = 'ORCHESTRATOR REASONING' + str(e)
        print_message(message=query_result)        

def assess_message_risk(user_string: str):
    if any(word in user_string.lower() for word in ['delete', 'remove', 'clear', 'drop', 'destroy']):
        return True
    return False

def request_human_validation(user_string: str):
    session['pending_validation'] = user_string
    msg = 'Should I go ahead with this database query? Reply with one word YES or NO'
    process_and_emit_message(socketio, msg, 'ai', 'main')
    return