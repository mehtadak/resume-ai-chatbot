# Author: Prof. MM Ghassemi <ghassem3@msu.edu>
################################################################################
# RFERENCES:
# https://www.geeksforgeeks.org/python/beautifulsoup-scraping-paragraphs-from-html/
# https://stackoverflow.com/questions/1936466/how-to-scrape-only-visible-webpage-text-with-beautifulsoup
################################################################################

import requests
from bs4 import BeautifulSoup
from bs4.element import Comment 
from .a2a_protocol import A2AProtocol, A2AMessage
from .llm import handle_ai_chat_request
from .database import database

db = database()

class WebCrawlerAgent:
    def __init__(self, a2a_protocol: A2AProtocol = None):
        # TODO: Initialize the A2A protocol and set agent ID
        self.a2a = a2a_protocol
        
    def tag_visible(self, element):
        if element.parent.name in ['style', 'script', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True

    def handle_a2a_request(self, message: A2AMessage) -> A2AMessage:
        # TODO: Check if action is "crawl_url"
        # TODO: Extract URL from message.params.get("url")
        # TODO: Call _crawl_url() method
        # TODO: Return response using a2a_protocol.send_response()
        url = None
        if message.action == "crawl_url":
            url = message.params.get('url')
        
        if url:
            response = self._crawl_url(url, message.message_id)
        
        if response:
            reply = self.a2a.send_response(message_id=message.message_id,sender='web_crawler_agent',recipient=message.sender,result=response)
            return reply
    
    def _crawl_url(self, url: str, message_id):
        # TODO: Use requests.get() to fetch the web page
        # TODO: Parse HTML content using BeautifulSoup
        # TODO: Extract page title
        # TODO: Extract raw text content
        # TODO: Call LLM to clean up text (remove menus, ads, navigation, etc.)
        # TODO: Segment cleaned text into chunks (500-1000 characters each)
        # TODO: Generate embeddings for each chunk using the embedding service you developed in Homework 2.
        # TODO: Store text chunks and corresponding embeddings in `documents` table you created in Step 2
        # TODO: Return a dictionary with the url, title, chunks_created, status
        try:
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            title = soup.find("title")
            title = title.get_text(strip=True) if title else "No Title"
            text = soup.find_all(string=True)
            filtered_text = filter(self.tag_visible, text)
            raw_text = " ".join(t.strip() for t in filtered_text)
            cleaned_text = handle_ai_chat_request(message=str(raw_text), llm_role='HTML Cleaner')
            chunks_created = 0
            for i in range(0, len(cleaned_text), 750):
                s = cleaned_text[i:i+750]
                db.insertRows(table='documents', columns=['url', 'title', 'chunk_text', 'chunk_index'], parameters=[[url, title, s, chunks_created]])
                chunks_created += 1
            
            # A2AProtocol.send_response(message_id=message_id)
            return {'url': url, 'title': title, 'chunks_created': chunks_created, 'status': 'success'}
        except Exception as e:
            return {'url': url, 'error': str(e), 'status': 'error'}

        