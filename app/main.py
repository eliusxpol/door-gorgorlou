from fastapi import FastAPI, Request, Response, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, Annotated
import logging
import os

# Import schemas, services and dependencies
from app.schemas import Payload, User, Image
from app.services import message_service
from app.dependencies import (
    parse_message, get_current_user, parse_audio_file, 
    parse_image_file, message_extractor
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="WhatsApp AI Agent API",
    description="API for handling WhatsApp Business API webhooks and messages",
    version="0.1.0"
)

# Configuration - Use environment variable in production
WEBHOOK_VERIFY_TOKEN = os.getenv("WEBHOOK_VERIFY_TOKEN", "your-verify-token-here")

@app.get("/")
async def root():
    """Root endpoint to verify the API is running"""
    return {
        "status": "active",
        "message": "WhatsApp AI Agent API is running",
        "version": "0.1.0"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "whatsapp-ai-agent"
    }

@app.get("/webhook")
async def verify_whatsapp_webhook(
    hub_mode: str = Query("subscribe", description="The mode of the webhook", alias="hub.mode"),
    hub_verify_token: str = Query(..., description="The verification token", alias="hub.verify_token"),
    hub_challenge: str = Query(..., description="The challenge to verify the webhook", alias="hub.challenge")
):
    """
    Webhook verification endpoint for WhatsApp Business API
    This endpoint is called by WhatsApp to verify the webhook URL
    Uses Query aliases to handle WhatsApp's dot notation (hub.mode, hub.verify_token, hub.challenge)
    """
    logger.info(f"Webhook verification request received: mode={hub_mode}, token={hub_verify_token}")
    
    if hub_mode == "subscribe" and hub_verify_token == WEBHOOK_VERIFY_TOKEN:
        logger.info("Webhook verified successfully")
        return Response(content=hub_challenge, media_type="text/plain")
    else:
        logger.warning("Webhook verification failed")
        raise HTTPException(status_code=403, detail="Verification failed")


@app.post("/webhook", status_code=200)
async def receive_whatsapp_webhook(
    payload: Payload,
    user: Annotated[Optional[User], Depends(get_current_user)],
    user_message: Annotated[Optional[str], Depends(message_extractor)],
    image: Annotated[Optional[Image], Depends(parse_image_file)],
):
    """
    Webhook endpoint to receive WhatsApp messages and notifications
    This endpoint will handle incoming messages from WhatsApp
    """
    
    # WhatsApp sends status updates and other notifications too
    # We only process actual messages
    if not user:
        logger.info("Received webhook without valid user/message - likely a status update")
        return JSONResponse(content={"status": "ok"})
    
    # Process the message based on type
    if image:
        logger.info(f"Image message received from {user.phone}")
        # TODO: Implement image handling
        # For now, acknowledge but inform it's not supported
        message_service.send_whatsapp_message(
            to=user.phone,
            message="We received your image. Image processing will be available soon!",
            template=False  # Use regular text within 24-hour session
        )
        return JSONResponse(content={"status": "ok", "message": "Image received"})
    
    if user_message:
        logger.info(f"Text message received from {user.first_name} {user.last_name}: {user_message}")
        
        # Get the full message object for processing
        message = parse_message(payload)
        if message:
            # Process the message through the service
            result = message_service.process_message(user, user_message, message)
            
            # Send automated response for testing
            # TODO: Replace with actual AI agent response
            if "detected_service" in result:
                response_text = f"I understand you're looking for {result['detected_service']} services. We'll connect you with the right provider soon!"
            else:
                response_text = "Thank you for your message. We're processing your request and will respond shortly."
            
            message_service.send_whatsapp_message(
                to=user.phone,
                message=response_text,
                template=False  # Use regular text within 24-hour session
            )
            
            return JSONResponse(content={"status": "ok", "result": result})
    
    return JSONResponse(content={"status": "ok"})


@app.post("/test-webhook")
async def test_webhook(data: Dict[str, Any]):
    """
    Test endpoint to simulate webhook calls for development
    """
    logger.info(f"Test webhook received: {data}")
    
    # Try to parse as WhatsApp payload
    try:
        payload = Payload(**data)
        message = parse_message(payload)
        if message:
            user = message_service.authenticate_user_by_phone_number(message.from_)
            text = message.text.body if message.text else None
            result = message_service.process_message(user, text, message) if user and text else None
            
            return {
                "status": "success",
                "message": "Test webhook processed as WhatsApp payload",
                "parsed_message": text,
                "user": user.model_dump() if user else None,
                "processing_result": result
            }
    except Exception as e:
        logger.debug(f"Not a WhatsApp payload: {e}")
    
    return {
        "status": "success",
        "message": "Test webhook received",
        "data_received": data
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)