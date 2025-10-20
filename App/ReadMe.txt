AI Product Detection and Local Price Finder
🧩 Overview

This application combines computer vision and real-time web data to identify products from an uploaded image and retrieve current market prices and store locations in the specified city.

It integrates:

YOLOv8 for object detection,

SerpAPI (Google Shopping) for structured price data, and

Google Places API for accurate geolocation of market branches.

🧠 Core Functionality

The user uploads an image of a product and specifies a location (e.g., London, Dubai).

The YOLO model detects the dominant object or product in the image.

The detected product name is used to query SerpAPI, which returns real-time price listings from multiple online markets.

For each market, Google Places API identifies the corresponding physical branch location.

The final structured output includes:

Product name

Market name

Price

Product URL

Market latitude and longitude

Results are displayed on an interactive map (e.g., via Leaflet.js) for intuitive visualisation.

⚙️ System Requirements

Python 3.8+

Flask web framework

Ultralytics YOLOv8

pandas, requests, time

A stable internet connection for API queries