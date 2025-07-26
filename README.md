# Portfolio Backend API

Backend API untuk website portfolio Ficram Manifur Farissa dengan FastAPI.

## 🚀 Features

- ✅ REST API dengan FastAPI
- ✅ Penyimpanan tanpa database (JSON file)
- ✅ Auto-cleanup pesan lama (maksimal 10 pesan)
- ✅ Validasi input dengan Pydantic
- ✅ CORS support
- ✅ Health check endpoint
- ✅ Email validation
- ✅ Automatic documentation (Swagger UI)

## 📋 API Endpoints

### Messages
- `GET /api/messages` - Get all messages
- `POST /api/messages` - Submit new message
- `DELETE /api/messages/{id}` - Delete specific message
- `POST /api/messages/cleanup` - Manual cleanup (keep latest 5)

### System
- `GET /` - API info
- `GET /health` - Health check
- `GET /docs` - Swagger UI documentation
- `GET /redoc` - ReDoc documentation

## 🛠 Local Development

\`\`\`bash
# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Access API documentation
# Swagger UI: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
\`\`\`

## 🚀 Railway Deployment

1. **Connect Repository to Railway**
   - Go to [Railway](https://railway.app)
   - Create new project from GitHub repo

2. **Automatic Deployment**
   - Railway will detect `Procfile` and `requirements.txt`
   - Deployment will start automatically

3. **Environment Variables** (Optional)
   - `PORT` - Automatically set by Railway

## 📝 Message Schema

\`\`\`json
{
  "fullName": "John Doe",
  "email": "john@example.com",
  "position": "Software Developer",
  "message": "Great portfolio!"
}
\`\`\`

## 🔧 Configuration

### Procfile
\`\`\`
web: uvicorn main:app --host 0.0.0.0 --port $PORT
\`\`\`

## 📊 Auto-Cleanup Features

- Automatically keeps only the latest 10 messages
- Manual cleanup endpoint available
- Sorted by timestamp (newest first)

## 🔍 Monitoring

### Health Check
\`\`\`bash
curl https://your-app.railway.app/health
\`\`\`

### API Documentation
- Swagger UI: `https://your-app.railway.app/docs`
- ReDoc: `https://your-app.railway.app/redoc`

## 👨‍💻 Author

**Ficram Manifur Farissa**
- GitHub: [@ficrammanifur](https://github.com/ficrammanifur)
- Portfolio: [Your Portfolio URL]

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
