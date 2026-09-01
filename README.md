# Soai-initial-backend

# SoAI — AI-Powered Online Learning Platform (Backend)

SoAI is the backend of an online education platform that combines traditional course management with an integrated AI assistant to support learners. Built with Django, it provides secure user authentication, course and exercise management, and an AI-driven chat feature to help students throughout their learning journey.

> This repository contains a curated, public subset of the backend codebase, shared to showcase architecture and implementation. UI templates and certain internal modules have been excluded.

## ✨ Features

- **Custom User Authentication** — Email/OTP-based account verification and login using a custom Django user model.
- **Course Management** — Create, organize, and serve courses with structured exercises.
- **AI Assistant** — An integrated chat-based AI assistant to answer learner questions and support the study process.
- **Environment-based Configuration** — Secrets and environment-specific settings (database, email, secret keys) are managed via environment variables, never hardcoded.
- **Production-ready Setup** — Includes a build script for streamlined deployment.

## 🛠️ Tech Stack

- **Backend Framework:** Django
- **Language:** Python
- **Configuration:** `python-decouple` for environment variable management
- **Database:** Configurable via environment variables (e.g. PostgreSQL/SQLite)
- **Deployment:** Shell-based build script (`build.sh`) for platform deployment

## 📂 Project Structure

```
├── accounts/          # Custom user model, authentication & OTP verification
├── ai_assistant/       # AI chat assistant app
├── course/             # Course & exercise management
├── mysite/              # Project settings, URLs, WSGI/ASGI config
├── requirements.txt     # Python dependencies
├── build.sh             # Deployment build script
└── manage.py
```

## ⚙️ Environment Variables

The project expects the following environment variables (see `.env.example`):

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | Debug mode toggle |
| `EMAIL_HOST_PASSWORD` | Password for the email service used for OTP delivery |

## 🚀 Getting Started

```bash
# Clone the repository
git clone https://github.com/sofiamoj/Soai-initial-backend.git
cd Soai-initial-backend

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# then edit .env with your own values

# Run migrations
python manage.py migrate

# Start the development server
python manage.py runserver
```

## 📌 Note

This is a public, backend-only excerpt of a larger private project. Some modules (UI templates, static assets, and certain internal services) are intentionally not included in this repository.

## 👤 Author

**Sofia**
[GitHub](https://github.com/sofiamoj)
