import uuid
from typing import Dict, Any

class A2AMessage:
    def __init__(self, sender: str, recipient: str, action: str, params: Dict[str, Any]):
        self.message_id = str(uuid.uuid4())		# Generate unique ID for this message
        self.sender = sender									# Who sent this message
        self.recipient = recipient 						# Who should receive this message
        self.action = action									# What action to perform (e.g., "crawl_url")
        self.params = params 									# Parameters for the action (e.g., {"url": "https://example.com"})

class A2AProtocol:
    def __init__(self):
        self.pending_requests = {}            # Track requests that haven't been responded to yet
    
    def send_request(self, sender: str, recipient: str, action: str, params: Dict[str, Any]) -> str:
        message = A2AMessage(sender, recipient, action, params) # Create a new message
        self.pending_requests[message.message_id] = message     # Store it as pending until we get a response
        return message.message_id                               # Return the message ID so we can match responses
    
    def send_response(self, message_id: str, sender: str, recipient: str, result: Any) -> A2AMessage:
        response = A2AMessage(sender, recipient, "response", {"result": result})   # Create response message with the result
        if message_id in self.pending_requests: # Remove the original request from pending (it's been answered)
            del self.pending_requests[message_id]
        return response