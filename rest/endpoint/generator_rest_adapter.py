from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from rest.model.chat_request import ChatRequest
from rest.model.conversation_response import ConversationResponse

from domain.port.driving.generator_controller_port import GeneratorControllerPort

# REST adapter to handle HTTP requests
class GeneratorRestAdapter:
    def __init__(self, controller: GeneratorControllerPort):
        self.controller = controller
        
    async def get_generated_text(self, request: ChatRequest) -> JSONResponse:
        """
        Generates text from a given prompt.
        """
        try:
            generated_text = self.controller.generate_message(request.prompt)
            return JSONResponse(
                content={"generated_text": generated_text},
                status_code=200
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    async def get_all_conversations(self) -> JSONResponse:
        """
        Retrieves all available conversations.
        """
        try:
            conversations = self.controller.get_conversations()
            return JSONResponse(
                content={"conversation_ids": conversations},
                status_code=200
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve conversations: {str(e)}")
    
    async def create_conversation(self) -> JSONResponse:
        """
        Creates a new conversation and returns its identifier.
        """
        try:
            conversation_id = self.controller.create_conversation()
            return JSONResponse(
                content={"conversation_id": conversation_id},
                status_code=201
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to create a new conversation: {str(e)}")
    
    async def get_conversation(self, conversation_guid: str) -> ConversationResponse:
        """
        Retrieves the history of a specific conversation.
        """
        conversation = self.controller.get_history(conversation_guid)
        if conversation is None:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        return ConversationResponse(guid=conversation_guid, history=conversation.messages)

    async def generate_message_for_conversation(self, conversation_guid: str, request: ChatRequest) -> ConversationResponse:
        """
        Generates a message for a specific conversation.
        """
        try:
            updated_conversation = self.controller.generate_message_in_conversation(conversation_guid, request.prompt)
            return ConversationResponse(guid=conversation_guid, history=updated_conversation.messages)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    async def clear_conversation(self, conversation_guid: str) -> JSONResponse:
        """
        Clears the history of a specific conversation.
        """
        try:
            self.controller.clear_history(conversation_guid)
            return JSONResponse(
                content={"message": f"Conversation {conversation_guid} cleared successfully."},
                status_code=200
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    def get_router(self) -> APIRouter:
        router = APIRouter()
        router.post("/chat")(self.get_generated_text)
        router.get("/conversation")(self.get_all_conversations)
        router.post("/conversation")(self.create_conversation)
        router.get("/conversation/{conversation_guid}")(self.get_conversation)
        router.post("/conversation/{conversation_guid}")(self.generate_message_for_conversation)
        router.delete("/conversation/{conversation_guid}")(self.clear_conversation)
        return router
