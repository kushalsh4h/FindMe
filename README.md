# 🛍️ AI-Powered Product Recognition and Search

This project is a **Flask-based web application** that recognizes products from images, generates descriptions, and finds similar items online. It leverages **OpenAI's CLIP, Salesforce's BLIP, and Google Search via SerpAPI** to provide an AI-powered shopping experience.

## 🚀 Features
- Upload an image and get the **predicted product category**.
- Generate an **AI-powered description** for the product.
- **Search for similar products** online using Google Search (via SerpAPI).
- Store **search history** in an SQLite database.
- A simple **web interface** to interact with the system.

## 🛠️ Tech Stack
- **Backend**: Flask, SQLAlchemy
- **AI Models**: CLIP (for product recognition), BLIP (for description generation)
- **Database**: SQLite
- **Search API**: Google Search (via SerpAPI)
- **Frontend**: Jinja2 templates (HTML, CSS)

## 📦 Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
