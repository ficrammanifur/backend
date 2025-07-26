from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import json
import os
from datetime import datetime
import uuid
from typing import List, Optional

app = FastAPI(
    title="Portfolio Backend API",
    description="Backend API for portfolio website messages",
    version="1.0.0"
)

# CORS Configuration - More specific and secure
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ficrammanifur.github.io",
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080",
        "https://localhost:3000",
        "https://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# File untuk menyimpan pesan
MESSAGES_FILE = 'messages.json'
MAX_MESSAGES = 10

# Pydantic models
class MessageCreate(BaseModel):
    fullName: str
    email: EmailStr
    position: str
    message: str

class MessageResponse(BaseModel):
    id: str
    fullName: str
    email: str
    position: str
    message: str
    timestamp: str
    created_at: str

class ApiResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    messages: Optional[List[MessageResponse]] = None
    count: Optional[int] = None
    data: Optional[MessageResponse] = None
    error: Optional[str] = None

def load_messages():
    """Load messages from JSON file"""
    if os.path.exists(MESSAGES_FILE):
        try:
            with open(MESSAGES_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except Exception as e:
            print(f"Error loading messages: {e}")
            return []
    return []

def save_messages(messages):
    """Save messages to JSON file"""
    try:
        with open(MESSAGES_FILE, 'w', encoding='utf-8') as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)
        print(f"Saved {len(messages)} messages to file")
    except Exception as e:
        print(f"Error saving messages: {e}")

def cleanup_old_messages(messages):
    """Keep only the latest MAX_MESSAGES"""
    if len(messages) > MAX_MESSAGES:
        messages.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        return messages[:MAX_MESSAGES]
    return messages

# Handle preflight requests explicitly
@app.options("/{full_path:path}")
async def options_handler():
    return {"message": "OK"}

@app.get("/")
async def root():
    return {
        "message": "Portfolio Backend API - Ficram Manifur Farissa",
        "version": "1.0.0",
        "status": "running",
        "cors_enabled": True,
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "GET /api/messages": "Get all messages",
            "POST /api/messages": "Submit new message",
            "DELETE /api/messages/{id}": "Delete specific message",
            "GET /docs": "API Documentation",
            "GET /health": "Health check"
        }
    }

@app.get("/api/messages")
async def get_messages():
    """Get all messages"""
    try:
        messages = load_messages()
        print(f"Retrieved {len(messages)} messages")
        return {
            "success": True,
            "messages": messages,
            "count": len(messages)
        }
    except Exception as e:
        print(f"Error in get_messages: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/messages")
async def submit_message(message_data: MessageCreate):
    """Submit new message"""
    try:
        # Load existing messages
        messages = load_messages()
        
        # Create new message
        new_message = {
            "id": str(uuid.uuid4()),
            "fullName": message_data.fullName.strip(),
            "email": message_data.email.strip().lower(),
            "position": message_data.position.strip(),
            "message": message_data.message.strip(),
            "timestamp": datetime.now().isoformat(),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Add to beginning of list (newest first)
        messages.insert(0, new_message)
        
        # Cleanup old messages
        messages = cleanup_old_messages(messages)
        
        # Save messages
        save_messages(messages)
        
        print(f"New message added from {new_message['fullName']}")
        
        return {
            "success": True,
            "message": "Message submitted successfully",
            "data": new_message
        }
        
    except Exception as e:
        print(f"Error in submit_message: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/messages/{message_id}")
async def delete_message(message_id: str):
    """Delete specific message"""
    try:
        messages = load_messages()
        
        # Find and remove message
        original_count = len(messages)
        messages = [msg for msg in messages if msg.get('id') != message_id]
        
        if len(messages) == original_count:
            raise HTTPException(status_code=404, detail="Message not found")
        
        save_messages(messages)
        
        return {
            "success": True,
            "message": "Message deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in delete_message: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/messages/cleanup")
async def cleanup_messages():
    """Manual cleanup - keep only latest 5 messages"""
    try:
        messages = load_messages()
        
        if len(messages) > 5:
            messages.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
            messages = messages[:5]
            save_messages(messages)
        
        return {
            "success": True,
            "message": f"Cleanup completed. {len(messages)} messages remaining"
        }
        
    except Exception as e:
        print(f"Error in cleanup_messages: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    messages_count = len(load_messages())
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Portfolio Backend API",
        "cors_enabled": True,
        "messages_count": messages_count,
        "file_exists": os.path.exists(MESSAGES_FILE)
    }

@app.get("/test-cors")
async def test_cors():
    """Test CORS endpoint"""
    return {
        "cors_test": "success",
        "origin_allowed": True,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == '__main__':
    import uvicorn
    
    # Create messages file if it doesn't exist
    if not os.path.exists(MESSAGES_FILE):
        save_messages([])
        print("Created empty messages.json file")
    
    port = int(os.environ.get('PORT', 8000))
    print(f"Starting server on port {port}")
    uvicorn.run("main:app", host='0.0.0.0', port=port, reload=False)
