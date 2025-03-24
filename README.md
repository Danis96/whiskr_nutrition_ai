# Whiskr Nutrition AI

A FastAPI-based application that provides nutrition-related AI-powered services using LangChain and Ollama.

## 🚀 Features

- FastAPI-based REST API with SSL support
- Integration with LangChain and Ollama for AI capabilities
- MySQL database integration with SQLAlchemy
- Alembic for database migrations
- Environment-based configuration

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **AI/ML**: LangChain, Ollama
- **Database**: MySQL
- **ORM**: SQLAlchemy, SQLModel
- **Migration Tool**: Alembic
- **Server**: Uvicorn
- **Environment Management**: python-dotenv

## 📋 Prerequisites

- Python 3.x
- MySQL Server
- Ollama installed and running locally

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/whiskr_nutrition_ai.git
cd whiskr_nutrition_ai
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with the following variables:
```env
SSL_KEYFILE=path/to/your/ssl/key
SSL_CERTFILE=path/to/your/ssl/cert
# Add other required environment variables
```

## 🚀 Running the Application

1. Start the server:
```bash
python main.py
```

The application will be available at `https://localhost:8800`

## 📁 Project Structure

```
whiskr_nutrition_ai/
├── main.py              # Main application entry point
├── llm.py              # LangChain and Ollama integration
├── llm_validation.py   # LLM validation utilities
├── routes/             # API routes
│   ├── nutrition_routes.py
│   └── __init__.py
├── requirements.txt    # Project dependencies
└── .env               # Environment variables
```

## 🔒 Security

- SSL/TLS encryption enabled
- Environment variable-based configuration
- Secure API endpoints

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- Your Name - Initial work

## 🙏 Acknowledgments

- FastAPI team for the amazing framework
- LangChain community for the AI tools
- Ollama team for the local LLM capabilities 