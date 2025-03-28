# Projects
# Travel Booking App

## Overview
The **Travel Booking App** is a web-based application that allows users to search for flights and hotels while also providing chatbot support. The project is built using **HTML, CSS, JavaScript (Frontend)** and **Flask (Backend)**.

## Features
- ✈️ **Search Flights and Hotels** by destination and date.
- 🤖 **Chatbot Integration** for travel-related queries.
- 🎨 **Responsive Design** with a clean and modern UI.
- ⚡ **Fast and Lightweight** using Flask and JavaScript.

## Technologies Used
### Frontend
- **HTML** (Structure)
- **CSS** (Styling)
- **JavaScript** (Client-Side Logic)

### Backend
- **Flask (Python)** (Server-Side Logic)
- **JSON** (Data Exchange)
- **.env** (Environment Variables for Security)

## Project Structure
```
📁 Travel-Booking-App
│── 📄 index.html        # Main HTML file (User Interface)
│── 📄 styles.css        # Styling for the webpage
│── 📄 app.js            # Frontend logic and API calls
│── 📄 main.py           # Flask backend (Handles API requests)
│── 📄 .env              # Environment variables (API keys, credentials)
```

## Installation & Setup
1. **Clone the repository**
```sh
git clone https://github.com/yourusername/Travel-Booking-App.git
cd Travel-Booking-App
```

2. **Set up a virtual environment** (Recommended)
```sh
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

3. **Install dependencies**
```sh
pip install -r requirements.txt
```

4. **Run the Flask server**
```sh
python main.py
```

5. **Open the web app**
- Visit `http://127.0.0.1:5000/` in your browser.

## How It Works
1. **User enters a destination & date** → Clicks "Search"
2. **App sends request to Flask backend** (`/search` API)
3. **Flask returns flight and hotel data** → Displays results on UI
4. **User can chat with the bot** → Queries are sent to `/chat` API
5. **Bot responds with predefined messages**

## API Endpoints
### `GET /search`
**Parameters:**
- `destination` (string)
- `date` (string)

**Response:**
```json
{
  "flights": [{"airline": "XYZ Airlines", "price": "$300"}],
  "hotels": [{"name": "Grand Hotel", "price": "$150/night"}]
}
```

### `POST /chat`
**Request Body:**
```json
{ "message": "Hello" }
```

**Response:**
```json
{ "reply": "I can help with flights and hotels!" }
```
