from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import torch
import clip
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from serpapi import GoogleSearch
import os
from datetime import datetime

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define database models
class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    predicted_product = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Upload {self.filename}>"

class SearchResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    upload_id = db.Column(db.Integer, db.ForeignKey('upload.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    link = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f"<SearchResult {self.title}>"

# Create the database and tables
with app.app_context():
    db.create_all()

# Load CLIP model and processor
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# Load BLIP model for description generation
blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)

# Define categories
categories = ["sneakers", "laptop", "backpack", "watch", "smartphone", "shirt", "t-shirt", "pants", "jeans", "jacket", "dress", "shorts", "sweater", "coat", "hat", "gloves", "scarf", "sunglasses", "handbag", "wallet"]

# Function to recognize product
def recognize_product(image_path, categories):
    image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
    text_inputs = clip.tokenize(categories).to(device)
    
    with torch.no_grad():
        image_features = model.encode_image(image)
        text_features = model.encode_text(text_inputs)
    
    similarities = (image_features @ text_features.T).squeeze(0)
    best_match_idx = similarities.argmax().item()
    return categories[best_match_idx]

# Function to generate product description
def generate_description(image_path):
    image = Image.open(image_path).convert("RGB")
    inputs = blip_processor(images=image, return_tensors="pt").to(device)
    with torch.no_grad():
        caption = blip_model.generate(**inputs)
    return blip_processor.decode(caption[0], skip_special_tokens=True)

# Function to search Google for similar products using SerpAPI
def search_google(product_name, description):
    query = f"Buy {product_name} {description} online"
    params = {
        "q": query,
        "hl": "en",
        "gl": "us",
        "api_key": "5a91fb4ef78a13b9165c5584da9cee19ff67e7bcd6c1aef1a62a1855662a3852"  # Replace with your actual SerpAPI key
    }
    
    search = GoogleSearch(params)
    results = search.get_dict()
    search_results = []
    
    if "organic_results" in results:
        for result in results["organic_results"][:5]:  # Top 5 results
            title = result.get("title", "No Title")
            link = result.get("link", "#")
            search_results.append({"title": title, "link": link})
    
    return search_results if search_results else [{"title": "No results found", "link": "#"}]

# Serve the frontend
@app.route("/")
def index():
    return render_template("index.html")

# API endpoint to handle image upload and processing
@app.route("/upload", methods=["POST"])
def upload_image():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400
    
    # Save the uploaded file temporarily
    image_path = os.path.join("uploads", file.filename)
    file.save(image_path)
    
    # Recognize product and generate description
    predicted_product = recognize_product(image_path, categories)
    description = generate_description(image_path)
    
    # Search for similar products
    search_results = search_google(predicted_product, description)
    
    # Save upload and search results to the database
    upload = Upload(filename=file.filename, predicted_product=predicted_product, description=description)
    db.session.add(upload)
    db.session.commit()

    for result in search_results:
        search_result = SearchResult(upload_id=upload.id, title=result["title"], link=result["link"])
        db.session.add(search_result)
    
    db.session.commit()
    
    # Clean up: Delete the uploaded file
    os.remove(image_path)
    
    # Return results as JSON
    return jsonify({
        "product": predicted_product,
        "description": description,
        "search_results": search_results
    })

if __name__ == "__main__":
    # Create uploads directory if it doesn't exist
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    
    # Run the Flask app
    app.run(debug=True)

    # Get all uploads
uploads = Upload.query.all()

# Get search results for a specific upload
upload = Upload.query.get(1)
search_results = SearchResult.query.filter_by(upload_id=upload.id).all()

@app.route("/history")
def history():
    uploads = Upload.query.order_by(Upload.created_at.desc()).all()
    return render_template("history.html", uploads=uploads)