from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="WhatsApp AI Agent API",
    description="API for handling WhatsApp Business API webhooks and messages",
    version="0.1.0"
)

# Pydantic models for webhook data
class WebhookVerification(BaseModel):
    hub_mode: str = "subscribe"
    hub_verify_token: str
    hub_challenge: str

class WhatsAppMessage(BaseModel):
    object: str
    entry: list[Dict[str, Any]]

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
async def verify_webhook(
    hub_mode: str = None,
    hub_verify_token: str = None,
    hub_challenge: str = None
):
    """
    Webhook verification endpoint for WhatsApp Business API
    This endpoint is called by WhatsApp to verify the webhook URL
    """
    logger.info(f"Webhook verification request received: mode={hub_mode}, token={hub_verify_token}")
    
    if hub_mode == "subscribe" and hub_verify_token == WEBHOOK_VERIFY_TOKEN:
        logger.info("Webhook verified successfully")
        return Response(content=hub_challenge, media_type="text/plain")
    else:
        logger.warning("Webhook verification failed")
        raise HTTPException(status_code=403, detail="Verification failed")

@app.post("/webhook")
async def receive_webhook(request: Request):
    """
    Webhook endpoint to receive WhatsApp messages and notifications
    This endpoint will handle incoming messages from WhatsApp
    """
    try:
        # Get the raw body
        body = await request.json()
        logger.info(f"Webhook received: {body}")
        
        # Basic validation
        if body.get("object") != "whatsapp_business_account":
            return JSONResponse(
                status_code=400,
                content={"error": "Invalid webhook object type"}
            )
        
        # Process the webhook data
        entries = body.get("entry", [])
        for entry in entries:
            entry_id = entry.get("id")
            changes = entry.get("changes", [])
            
            for change in changes:
                value = change.get("value", {})
                
                # Check if it's a message
                messages = value.get("messages", [])
                for message in messages:
                    from_number = message.get("from")
                    message_type = message.get("type")
                    
                    if message_type == "text":
                        text_body = message.get("text", {}).get("body")
                        logger.info(f"Received text message from {from_number}: {text_body}")
                        # TODO: Process the message with AI agent
                    
                    elif message_type == "image":
                        logger.info(f"Received image message from {from_number}")
                        # TODO: Handle image messages
                    
                    elif message_type == "audio":
                        logger.info(f"Received audio message from {from_number}")
                        # TODO: Handle audio messages
                    
                    else:
                        logger.info(f"Received {message_type} message from {from_number}")
        
        # Return success response
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Webhook processed successfully"
            }
        )
        
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": "Internal server error processing webhook"
            }
        )

@app.post("/test-webhook")
async def test_webhook(data: Dict[str, Any]):
    """
    Test endpoint to simulate webhook calls for development
    """
    logger.info(f"Test webhook received: {data}")
    return {
        "status": "success",
        "message": "Test webhook received",
        "data_received": data
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)