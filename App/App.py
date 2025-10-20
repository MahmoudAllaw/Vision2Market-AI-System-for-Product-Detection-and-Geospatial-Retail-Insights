from flask import Flask, render_template, request, jsonify
from ultralytics import YOLO
import pandas as pd
import requests
import os
import time

# -------------------------------------------------
# Flask Application Setup
# -------------------------------------------------
app = Flask(__name__)

# Load trained YOLO model
model = YOLO(
    r"C:\Users\mahmo\Downloads\AI-Product detect & search\runs\detect\train\weights\best.pt"
)

# Load SerpAPI key (either from environment or direct definition)
SERPAPI_KEY = "62c95b506e9c712133633fab29d34963139ade2b6e7e50f408a244e42dd37237"

# -------------------------------------------------
# Utility Functions
# -------------------------------------------------
def detect_region(area: str) -> str:
    """Infer the geographical region code for Google Shopping."""
    area = area.lower()
    if "dubai" in area or "uae" in area or "abu dhabi" in area:
        return "ae"
    elif "london" in area or "uk" in area or "england" in area:
        return "uk"
    elif "new york" in area or "us" in area or "america" in area:
        return "us"
    elif "france" in area or "paris" in area:
        return "fr"
    else:
        return "uk"  # default fallback


def geocode_area(area: str):
    """Return approximate coordinates for the main supported cities."""
    area = area.lower()
    if "dubai" in area or "uae" in area:
        return 25.276987, 55.296249
    elif "london" in area or "uk" in area:
        return 51.5074, -0.1278
    elif "new york" in area or "us" in area:
        return 40.7128, -74.0060
    elif "paris" in area or "france" in area:
        return 48.8566, 2.3522
    else:
        return 25.2048, 55.2708  # Default (Dubai)


def geocode_market(market_name: str, area: str):
    """
    Use OpenStreetMap's Nominatim API to estimate the coordinates
    of a market branch within the provided city.
    """
    try:
        query = f"{market_name}, {area}"
        url = f"https://nominatim.openstreetmap.org/search?q={query}&format=json&limit=1"
        headers = {"User-Agent": "MarketLocator/1.0"}
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        data = r.json()
        if not data:
            return None, None
        return float(data[0]["lat"]), float(data[0]["lon"])
    except Exception:
        return None, None


def get_prices_from_serpapi(product_name: str, area: str) -> pd.DataFrame:
    """Fetch structured product and price data from SerpAPI."""
    region = detect_region(area)
    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google_shopping",
        "q": product_name,
        "hl": "en",
        "gl": region,
        "api_key": SERPAPI_KEY
    }

    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()
    data = response.json()
    shopping_results = data.get("shopping_results", [])
    results = []

    for item in shopping_results:
        title = item.get("title", "")
        price = item.get("price", "")
        link = item.get("link", "")
        source = item.get("source", "")
        thumbnail = item.get("thumbnail", "")

        if not title or not price:
            continue

        results.append({
            "Market": source if source else "Unknown",
            "Description": title,
            "Price": price,
            "URL": link,
            "Image": thumbnail
        })

    if not results:
        return pd.DataFrame([{
            "Market": "N/A",
            "Description": "No price data available for this region.",
            "Price": "-",
            "URL": "",
            "Image": ""
        }])

    return pd.DataFrame(results)

# -------------------------------------------------
# Flask Routes
# -------------------------------------------------
@app.route("/")
def index():
    """Render the home page."""
    return render_template("index.html")


@app.route("/detect", methods=["POST"])
def detect():
    """
    Handle uploaded image, run YOLO product detection,
    fetch prices from SerpAPI, and append geolocation data.
    """
    image = request.files.get("image")
    area = request.form.get("area", "")

    if not image or not area:
        return jsonify({"error": "Missing image or location input."}), 400

    os.makedirs("static", exist_ok=True)
    img_path = os.path.join("static", "upload.jpg")
    image.save(img_path)

    # Perform YOLO inference
    results = model.predict(img_path)
    classes = results[0].names
    detected_classes = [classes[int(box.cls)] for box in results[0].boxes]

    if not detected_classes:
        return jsonify({"error": "No products detected in the image."})

    product_name = detected_classes[0]

    # Fetch pricing information
    try:
        df = get_prices_from_serpapi(product_name, area)
    except Exception as e:
        return jsonify({"error": f"API request failed: {e}"})

    data = df.to_dict(orient="records")

    # Add coordinates for each market (branch-level where possible)
    for item in data:
        lat, lon = geocode_market(item["Market"], area)
        if not lat or not lon:
            lat, lon = geocode_area(area)
        item["Latitude"] = lat
        item["Longitude"] = lon
        time.sleep(1)  # Respect Nominatim rate limit

    return jsonify({
        "product": product_name,
        "data": data
    })


# -------------------------------------------------
# Main Entry Point
# -------------------------------------------------
if __name__ == "__main__":
    if not SERPAPI_KEY:
        print("⚠️  Warning: SERPAPI_KEY not found. Please set it using:")
        print("   setx SERPAPI_KEY \"your_api_key_here\"   (Windows)")
        print("   export SERPAPI_KEY=\"your_api_key_here\"  (Linux/macOS)")
    app.run(debug=True)
