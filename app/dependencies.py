"""
FastAPI dependencies for webhook processing
"""
from typing import Optional, Annotated
from fastapi import Depends
from app.schemas import Payload, Message, User, Audio, Image
from app.services import message_service


def parse_message(payload: Payload) -> Optional[Message]:
    """Extract the first message from the webhook payload"""
    try:
        if (payload.entry and 
            payload.entry[0].changes and 
            payload.entry[0].changes[0].value.messages and
            len(payload.entry[0].changes[0].value.messages) > 0):
            return payload.entry[0].changes[0].value.messages[0]
    except (IndexError, AttributeError):
        pass
    return None


def get_current_user(message: Annotated[Optional[Message], Depends(parse_message)]) -> Optional[User]:
    """Get or create user from message sender"""
    if not message:
        return None
    return message_service.authenticate_user_by_phone_number(message.from_)


def parse_audio_file(message: Annotated[Optional[Message], Depends(parse_message)]) -> Optional[Audio]:
    """Extract audio from message if present"""
    if message and message.type == "audio":
        return message.audio
    return None


def parse_image_file(message: Annotated[Optional[Message], Depends(parse_message)]) -> Optional[Image]:
    """Extract image from message if present"""
    if message and message.type == "image":
        return message.image
    return None


def message_extractor(
        message: Annotated[Optional[Message], Depends(parse_message)],
        audio: Annotated[Optional[Audio], Depends(parse_audio_file)],
) -> Optional[str]:
    """Extract text content from message or transcribe audio"""
    if audio:
        return message_service.transcribe_audio(audio)
    if message and message.text:
        return message.text.body
    return None