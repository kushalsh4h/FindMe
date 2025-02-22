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

## 🔍 How It Works
- Upload an image on the web interface.
![image](https://github.com/user-attachments/assets/e5fe6b59-b394-45ac-a818-b86cea351c92)

- The system uses CLIP to classify the product into categories like "sneakers," "laptop," "watch," etc.
![image](https://github.com/user-attachments/assets/4125b6e6-493b-4a12-bca6-05a7b7e842e6)

- The BLIP model generates a descriptive caption for the product.
![image](https://github.com/user-attachments/assets/a279d57b-4fa0-41f2-a257-9f281487febb)

- A Google search (via SerpAPI) retrieves relevant product listings.
![image](https://github.com/user-attachments/assets/44addd0c-4f30-4dc6-8549-a2ba771ddf2b)

- The search history is stored in SQLite and accessible via /history.
![image](https://github.com/user-attachments/assets/e17fb0fb-3b18-40fb-a10b-1bd6f121dbc3)
