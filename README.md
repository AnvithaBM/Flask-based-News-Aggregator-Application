# InfoStream Media News App

A simple Flask-based news aggregator web application that fetches and displays the latest tech news articles using the NewsAPI

Users can browse news articles by topic (e.g., Business, Sports, Technology) with pagination support for smooth navigation.

## 1. Clone the Repository
https://github.com/AnvithaBM/Flask-based-News-Aggregator-Application.git

## 2. Create & Activate Virtual Environment
python -m venv .venv

### Windows
.venv\Scripts\activate

## 3. Setup Environment Variables

Create a .env file in the project root and add:

NEWS_API_KEY=your_api_key_here

Get your free API key from NewsAPI

## 4. Run the Application
python app.py


Open http://127.0.0.1:5000 in your browser.

## Deployment with ngrok

You can make your app accessible online using ngrok:

### Terminal 1: Run Flask
python app.py

### Terminal 2: Start ngrok
ngrok http 5000

Copy the public URL shown in the terminal (e.g., https://<random>.ngrok-free.app) and share it.

