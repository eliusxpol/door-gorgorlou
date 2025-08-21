"""
Message service for handling WhatsApp messages
"""
import logging
import os
import requests
from typing import Optional
from app.schemas import User, Audio, Message

logger = logging.getLogger(__name__)

# WhatsApp API Configuration
WHATSAPP_API_ACCESS_TOKEN = os.getenv("WHATSAPP_API_ACCESS_TOKEN")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "733570336512245")
WHATSAPP_API_URL = f"https://graph.facebook.com/v22.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"

# Mock user database - replace with actual database in production
MOCK_USERS = {
    "221776504003": User(
        id=1,
        first_name="Test",
        last_name="Client",
        phone="221776504003",
        role="client"
    ),
    "15142176828": User(
        id=2,
        first_name="Test",
        last_name="Provider",
        phone="15142176828",
        role="provider"
    )
}

def authenticate_user_by_phone_number(phone_number: str) -> Optional[User]:
    """
    Authenticate user by phone number
    In production, this should query the actual database
    """
    # Remove any formatting from phone number
    clean_phone = phone_number.replace("+", "").replace(" ", "").replace("-", "")
    
    # Check if user exists in mock database
    user = MOCK_USERS.get(clean_phone)
    
    if user:
        logger.info(f"User authenticated: {user.first_name} {user.last_name} ({user.phone})")
        return user
    else:
        logger.warning(f"User not found for phone number: {clean_phone}")
        return None

def transcribe_audio(audio: Audio) -> Optional[str]:
    """
    Transcribe audio message to text
    In production, this would call a speech-to-text service
    """
    logger.info(f"Audio transcription requested for audio ID: {audio.id}")
    # Placeholder - in production, integrate with WhatsApp media download
    # and speech-to-text service (e.g., OpenAI Whisper, Google Speech-to-Text)
    return f"[Audio message {audio.id} - transcription pending]"

def process_message(user: User, message_text: Optional[str], message: Message) -> dict:
    """
    Process incoming message and determine appropriate response
    This is where the AI agent logic will be integrated
    """
    response = {
        "status": "received",
        "user_id": user.id,
        "message_type": message.type
    }
    
    if message_text:
        logger.info(f"Processing text message from {user.phone}: {message_text}")
        response["message"] = "Message received and queued for processing"
        
        # TODO: Integrate with AI agent for:
        # - Intent detection
        # - Service category classification
        # - Slot collection
        # - Provider matching
        
        # Basic keyword detection for early testing
        if "plumber" in message_text.lower() or "plumbing" in message_text.lower():
            response["detected_service"] = "plumbing"
        elif "electrician" in message_text.lower() or "electrical" in message_text.lower():
            response["detected_service"] = "electrical"
        elif "tutor" in message_text.lower() or "tutoring" in message_text.lower():
            response["detected_service"] = "tutoring"
    
    return response

def send_whatsapp_message(to: str, message: str, template: bool = True) -> bool:
    """
    Send a WhatsApp message using the WhatsApp Business API
    
    Args:
        to: Recipient's phone number (with country code)
        message: The message text to send
        template: If True, sends as template message; if False, sends as regular text
    
    Returns:
        bool: True if message was sent successfully, False otherwise
    """
    if not WHATSAPP_API_ACCESS_TOKEN:
        logger.error("WHATSAPP_API_ACCESS_TOKEN not configured")
        return False
    
    # Clean phone number (ensure it has no + or spaces)
    clean_to = to.replace("+", "").replace(" ", "").replace("-", "")
    
    logger.info(f"Sending WhatsApp message to {clean_to}: {message[:50]}...")
    
    headers = {
        "Authorization": f"Bearer {WHATSAPP_API_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    if template:
        # For template messages (we'll need to create templates in WhatsApp Business)
        # For now, using a basic hello_world template as placeholder
        payload = {
            "messaging_product": "whatsapp",
            "to": clean_to,
            "type": "template",
            "template": {
                "name": "hello_world",  # Replace with actual template name
                "language": {
                    "code": "en_US"
                }
            }
        }
    else:
        # For regular text messages (only works within 24-hour session window)
        payload = {
            "messaging_product": "whatsapp",
            "to": clean_to,
            "type": "text",
            "text": {
                "body": message
            }
        }
    
    try:
        response = requests.post(
            WHATSAPP_API_URL,
            headers=headers,
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            logger.info(f"Message sent successfully to {clean_to}")
            return True
        else:
            logger.error(f"Failed to send message. Status: {response.status_code}, Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Error sending WhatsApp message: {e}")
        return False