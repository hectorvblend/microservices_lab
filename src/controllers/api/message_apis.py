#!/usr/bin/env python3
'''
This file includes the API endpoints for the application.
'''
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from src.controllers.pub_sub.publisher import Publisher
from src.controllers.api.schemas.message_schemas import SendMessage
from src.connectors.long_process.async_process import AsyncProcess

router = APIRouter()

@router.post("/message/", tags=["Message APIs"])
async def insert_message(body_params : SendMessage):
    """
    Endpoint to insert a message into the async process system and publish it.

    Args:
    -----
    body_params : SendMessage
        The input body parameters containing the message and user information.

    Returns:
    --------
    dict
        A dictionary representation of the inserted message record.
    """

    message = AsyncProcess()
    message = message.insert_message(
        event_type='message',
        status='pending',
        input=dict(body_params),
        attempts=0,
        created_by=body_params.user,
        updated_by=body_params.user,
    )
    Publisher().publish_message(message=message['id'].decode())
    return message


@router.get("/stream")
async def stream():
    """
    Endpoint to stream messages from the async process system.

    This endpoint returns a Server-Sent Events (SSE) stream of messages,
    where each message is a JSON object with the keys 'id', 'output', and 'status'.
    The 'status' key is set to 'successful' if the message was processed successfully,
    'failed' if it failed, and 'pending' if it is still waiting to be processed.

    Returns:
    --------
    StreamingResponse
        A StreamingResponse object with the SSE stream.
    """
    return StreamingResponse(AsyncProcess.event_stream(), media_type="text/event-stream")