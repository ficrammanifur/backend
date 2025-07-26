from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import json
import os
from datetime import datetime
import uuid

app = FastAPI(
    title="Portfolio Backend API",
    description="Backend API for portfolio website messages",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# File untuk menyimpan pesan
MESSAGES_FILE = 'messages.json'
MAX_MESSAGES = 10  # Maksimal 10 pesan, otomatis hapus yang lama

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

def load_messages():
    """Load messages from JSON file"""
    if os.path.exists(MESSAGES_FILE):
        try:
            with open(MESSAGES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_messages(messages):
    """Save messages to JSON file"""
    with open(MESSAGES_FILE, 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

def cleanup_old_messages(messages):
    """Keep only the latest MAX_MESSAGES"""
    if len(messages) > MAX_MESSAGES:
        # Sort by timestamp and keep only the latest
        messages.sort(key=lambda x: x['timestamp'], reverse=True)
        return messages[:MAX_MESSAGES]
    return messages

@app.get('/')
async def index():
    return {
        "message": "Portfolio Backend API",
        "version": "1.0.0",
        "endpoints": {
            "GET /api/messages": "Get all messages",
            "POST /api/messages": "Submit new message",
            "DELETE /api/messages/<id>": "Delete specific message"
        }
    }

@app.get('/api/messages')
async def get_messages():
    """Get all messages"""
    try:
        messages = load_messages()
        return {
            "success": True,
            "messages": messages,
            "count": len(messages)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/api/messages')
async def submit_message(message: MessageCreate):
    """Submit new message"""
    try:
        # Load existing messages
        messages = load_messages()
        
        # Create new message
        new_message = {
            "id": str(uuid.uuid4()),
            "fullName": message.fullName.strip(),
            "email": message.email.strip().lower(),
            "position": message.position.strip(),
            "message": message.message.strip(),
            "timestamp": datetime.now().isoformat(),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Add to beginning of list (newest first)
        messages.insert(0, new_message)
        
        # Cleanup old messages
        messages = cleanup_old_messages(messages)
        
        # Save messages
        save_messages(messages)
        
        return {
            "success": True,
            "message": "Message submitted successfully",
            "data": new_message
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete('/api/messages/{message_id}')
async def delete_message(message_id: str):
    """Delete specific message"""
    try:
        messages = load_messages()
        
        # Find and remove message
        messages = [msg for msg in messages if msg['id'] != message_id]
        
        save_messages(messages)
        
        return {
            "success": True,
            "message": "Message deleted successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/api/messages/cleanup')
async def cleanup_messages():
    """Manual cleanup - keep only latest 5 messages"""
    try:
        messages = load_messages()
        
        if len(messages) > 5:
            messages.sort(key=lambda x: x['timestamp'], reverse=True)
            messages = messages[:5]
            save_messages(messages)
        
        return {
            "success": True,
            "message": f"Cleanup completed. {len(messages)} messages remaining"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/health')
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == '__main__':
    import uvicorn
    # Create messages file if it doesn't exist
    if not os.path.exists(MESSAGES_FILE):
        save_messages([])
    
    port = int(os.environ.get('PORT', 8000))
    uvicorn.run("app:app", host='0.0.0.0', port=port, reload=False)
