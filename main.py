from flask import Flask, render_template, request, jsonify
import random
import os
import requests
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
app = Flask(__name__)

# Mock data for demonstration
mock_flights = [
    # New York flights
    {"id": 1, "from": "New York", "to": "Paris", "price": 450, "date": "2023-12-15", "airline": "Air France"},
    {"id": 2, "from": "New York", "to": "Paris", "price": 520, "date": "2023-12-15", "airline": "Delta"},
    {"id": 3, "from": "New York", "to": "Tokyo", "price": 850, "date": "2023-12-16", "airline": "Japan Airlines"},
    {"id": 4, "from": "New York", "to": "London", "price": 400, "date": "2023-12-22", "airline": "British Airways"},
    {"id": 5, "from": "New York", "to": "Sydney", "price": 950, "date": "2023-12-18", "airline": "Qantas"},
    {"id": 6, "from": "New York", "to": "San Francisco", "price": 300, "date": "2023-12-19", "airline": "United"},
    {"id": 7, "from": "New York", "to": "Dubai", "price": 750, "date": "2023-12-20", "airline": "Emirates"},
    {"id": 8, "from": "New York", "to": "Singapore", "price": 900, "date": "2023-12-21", "airline": "Singapore Airlines"},
    
    # London flights
    {"id": 9, "from": "London", "to": "Tokyo", "price": 780, "date": "2023-12-20", "airline": "British Airways"},
    {"id": 10, "from": "London", "to": "Paris", "price": 120, "date": "2023-12-19", "airline": "EasyJet"},
    {"id": 11, "from": "London", "to": "Sydney", "price": 950, "date": "2023-12-21", "airline": "Qantas"},
    {"id": 12, "from": "London", "to": "New York", "price": 400, "date": "2023-12-26", "airline": "Virgin Atlantic"},
    {"id": 13, "from": "London", "to": "San Francisco", "price": 550, "date": "2023-12-24", "airline": "British Airways"},
    {"id": 14, "from": "London", "to": "Dubai", "price": 450, "date": "2023-12-25", "airline": "Emirates"},
    {"id": 15, "from": "London", "to": "Singapore", "price": 700, "date": "2023-12-26", "airline": "Singapore Airlines"},
    
    # San Francisco flights
    {"id": 16, "from": "San Francisco", "to": "Tokyo", "price": 750, "date": "2023-12-17", "airline": "United"},
    {"id": 17, "from": "San Francisco", "to": "Sydney", "price": 900, "date": "2023-12-18", "airline": "Qantas"},
    {"id": 18, "from": "San Francisco", "to": "London", "price": 550, "date": "2023-12-24", "airline": "United"},
    {"id": 19, "from": "San Francisco", "to": "Paris", "price": 600, "date": "2023-12-25", "airline": "Air France"},
    {"id": 20, "from": "San Francisco", "to": "New York", "price": 300, "date": "2023-12-26", "airline": "United"},
    {"id": 21, "from": "San Francisco", "to": "Dubai", "price": 850, "date": "2023-12-27", "airline": "Emirates"},
    {"id": 22, "from": "San Francisco", "to": "Singapore", "price": 950, "date": "2023-12-28", "airline": "Singapore Airlines"},
    
    # Paris flights
    {"id": 23, "from": "Paris", "to": "Tokyo", "price": 800, "date": "2023-12-23", "airline": "Air France"},
    {"id": 24, "from": "Paris", "to": "London", "price": 120, "date": "2023-12-19", "airline": "EasyJet"},
    {"id": 25, "from": "Paris", "to": "Sydney", "price": 1000, "date": "2023-12-27", "airline": "Air France"},
    {"id": 26, "from": "Paris", "to": "New York", "price": 450, "date": "2023-12-28", "airline": "Air France"},
    {"id": 27, "from": "Paris", "to": "San Francisco", "price": 600, "date": "2023-12-29", "airline": "Air France"},
    {"id": 28, "from": "Paris", "to": "Dubai", "price": 500, "date": "2023-12-30", "airline": "Emirates"},
    {"id": 29, "from": "Paris", "to": "Singapore", "price": 750, "date": "2023-12-31", "airline": "Singapore Airlines"},
    
    # Tokyo flights
    {"id": 30, "from": "Tokyo", "to": "Sydney", "price": 700, "date": "2023-12-25", "airline": "Japan Airlines"},
    {"id": 31, "from": "Tokyo", "to": "London", "price": 780, "date": "2023-12-30", "airline": "Japan Airlines"},
    {"id": 32, "from": "Tokyo", "to": "Paris", "price": 800, "date": "2023-12-31", "airline": "Japan Airlines"},
    {"id": 33, "from": "Tokyo", "to": "New York", "price": 850, "date": "2024-01-01", "airline": "Japan Airlines"},
    {"id": 34, "from": "Tokyo", "to": "San Francisco", "price": 750, "date": "2024-01-02", "airline": "Japan Airlines"},
    {"id": 35, "from": "Tokyo", "to": "Dubai", "price": 650, "date": "2024-01-03", "airline": "Emirates"},
    {"id": 36, "from": "Tokyo", "to": "Singapore", "price": 450, "date": "2024-01-04", "airline": "Singapore Airlines"},
    
    # Sydney flights
    {"id": 37, "from": "Sydney", "to": "London", "price": 950, "date": "2023-12-28", "airline": "Qantas"},
    {"id": 38, "from": "Sydney", "to": "Paris", "price": 1000, "date": "2024-01-03", "airline": "Qantas"},
    {"id": 39, "from": "Sydney", "to": "Tokyo", "price": 700, "date": "2024-01-04", "airline": "Qantas"},
    {"id": 40, "from": "Sydney", "to": "New York", "price": 950, "date": "2024-01-05", "airline": "Qantas"},
    {"id": 41, "from": "Sydney", "to": "San Francisco", "price": 900, "date": "2024-01-06", "airline": "Qantas"},
    {"id": 42, "from": "Sydney", "to": "Dubai", "price": 850, "date": "2024-01-07", "airline": "Emirates"},
    {"id": 43, "from": "Sydney", "to": "Singapore", "price": 600, "date": "2024-01-08", "airline": "Singapore Airlines"},
    
    # Dubai flights
    {"id": 44, "from": "Dubai", "to": "New York", "price": 750, "date": "2024-01-09", "airline": "Emirates"},
    {"id": 45, "from": "Dubai", "to": "London", "price": 450, "date": "2024-01-10", "airline": "Emirates"},
    {"id": 46, "from": "Dubai", "to": "Paris", "price": 500, "date": "2024-01-11", "airline": "Emirates"},
    {"id": 47, "from": "Dubai", "to": "Tokyo", "price": 650, "date": "2024-01-12", "airline": "Emirates"},
    {"id": 48, "from": "Dubai", "to": "Sydney", "price": 850, "date": "2024-01-13", "airline": "Emirates"},
    {"id": 49, "from": "Dubai", "to": "San Francisco", "price": 850, "date": "2024-01-14", "airline": "Emirates"},
    {"id": 50, "from": "Dubai", "to": "Singapore", "price": 400, "date": "2024-01-15", "airline": "Emirates"},
    
    # Singapore flights
    {"id": 51, "from": "Singapore", "to": "New York", "price": 900, "date": "2024-01-16", "airline": "Singapore Airlines"},
    {"id": 52, "from": "Singapore", "to": "London", "price": 700, "date": "2024-01-17", "airline": "Singapore Airlines"},
    {"id": 53, "from": "Singapore", "to": "Paris", "price": 750, "date": "2024-01-18", "airline": "Singapore Airlines"},
    {"id": 54, "from": "Singapore", "to": "Tokyo", "price": 450, "date": "2024-01-19", "airline": "Singapore Airlines"},
    {"id": 55, "from": "Singapore", "to": "Sydney", "price": 600, "date": "2024-01-20", "airline": "Singapore Airlines"},
    {"id": 56, "from": "Singapore", "to": "San Francisco", "price": 950, "date": "2024-01-21", "airline": "Singapore Airlines"},
    {"id": 57, "from": "Singapore", "to": "Dubai", "price": 400, "date": "2024-01-22", "airline": "Singapore Airlines"}
]

mock_hotels = [
    # Paris hotels
    {"id": 1, "name": "Grand Hotel", "location": "Paris", "pricePerNight": 120, "rating": 4.5},
    {"id": 2, "name": "Budget Inn", "location": "Paris", "pricePerNight": 75, "rating": 3.8},
    {"id": 3, "name": "Eiffel View Hotel", "location": "Paris", "pricePerNight": 180, "rating": 4.6},
    {"id": 4, "name": "Louvre View Hotel", "location": "Paris", "pricePerNight": 220, "rating": 4.8},
    {"id": 5, "name": "Champs-Élysées Hotel", "location": "Paris", "pricePerNight": 160, "rating": 4.3},
    
    # Tokyo hotels
    {"id": 6, "name": "Luxury Suites", "location": "Tokyo", "pricePerNight": 200, "rating": 4.8},
    {"id": 7, "name": "Tokyo Tower Hotel", "location": "Tokyo", "pricePerNight": 150, "rating": 4.3},
    {"id": 8, "name": "Shibuya Station Hotel", "location": "Tokyo", "pricePerNight": 120, "rating": 4.2},
    {"id": 9, "name": "Ginza Hotel", "location": "Tokyo", "pricePerNight": 180, "rating": 4.5},
    {"id": 10, "name": "Sakura Inn", "location": "Tokyo", "pricePerNight": 90, "rating": 3.9},
    
    # Sydney hotels
    {"id": 11, "name": "Backpacker Hostel", "location": "Sydney", "pricePerNight": 40, "rating": 4.0},
    {"id": 12, "name": "Sydney Harbour Hotel", "location": "Sydney", "pricePerNight": 160, "rating": 4.4},
    {"id": 13, "name": "Opera House Hotel", "location": "Sydney", "pricePerNight": 200, "rating": 4.7},
    {"id": 14, "name": "Bondi Beach Resort", "location": "Sydney", "pricePerNight": 180, "rating": 4.3},
    {"id": 15, "name": "Darling Harbour Inn", "location": "Sydney", "pricePerNight": 140, "rating": 4.1},
    
    # London hotels
    {"id": 16, "name": "London Bridge Inn", "location": "London", "pricePerNight": 90, "rating": 4.1},
    {"id": 17, "name": "Big Ben Hotel", "location": "London", "pricePerNight": 150, "rating": 4.5},
    {"id": 18, "name": "Buckingham Palace Hotel", "location": "London", "pricePerNight": 250, "rating": 4.8},
    {"id": 19, "name": "Tower Bridge Hotel", "location": "London", "pricePerNight": 180, "rating": 4.4},
    {"id": 20, "name": "Hyde Park Inn", "location": "London", "pricePerNight": 120, "rating": 4.0},
    
    # New York hotels
    {"id": 21, "name": "Times Square Hotel", "location": "New York", "pricePerNight": 180, "rating": 4.3},
    {"id": 22, "name": "Central Park Inn", "location": "New York", "pricePerNight": 140, "rating": 4.0},
    {"id": 23, "name": "Empire State Hotel", "location": "New York", "pricePerNight": 220, "rating": 4.6},
    {"id": 24, "name": "Brooklyn Bridge Hotel", "location": "New York", "pricePerNight": 160, "rating": 4.2},
    {"id": 25, "name": "Manhattan Suites", "location": "New York", "pricePerNight": 200, "rating": 4.5},
    
    # San Francisco hotels
    {"id": 26, "name": "San Francisco Bay Hotel", "location": "San Francisco", "pricePerNight": 160, "rating": 4.4},
    {"id": 27, "name": "Golden Gate Inn", "location": "San Francisco", "pricePerNight": 120, "rating": 4.1},
    {"id": 28, "name": "Fisherman's Wharf Hotel", "location": "San Francisco", "pricePerNight": 180, "rating": 4.3},
    {"id": 29, "name": "Alcatraz View Hotel", "location": "San Francisco", "pricePerNight": 200, "rating": 4.5},
    {"id": 30, "name": "Cable Car Hotel", "location": "San Francisco", "pricePerNight": 140, "rating": 4.0},
    
    # Dubai hotels
    {"id": 31, "name": "Burj Al Arab", "location": "Dubai", "pricePerNight": 500, "rating": 4.9},
    {"id": 32, "name": "Dubai Marina Hotel", "location": "Dubai", "pricePerNight": 200, "rating": 4.5},
    {"id": 33, "name": "Palm Jumeirah Resort", "location": "Dubai", "pricePerNight": 300, "rating": 4.7},
    {"id": 34, "name": "Downtown Dubai Hotel", "location": "Dubai", "pricePerNight": 180, "rating": 4.4},
    {"id": 35, "name": "Dubai Creek Inn", "location": "Dubai", "pricePerNight": 120, "rating": 4.0},
    
    # Singapore hotels
    {"id": 36, "name": "Marina Bay Sands", "location": "Singapore", "pricePerNight": 400, "rating": 4.9},
    {"id": 37, "name": "Orchard Road Hotel", "location": "Singapore", "pricePerNight": 180, "rating": 4.4},
    {"id": 38, "name": "Sentosa Resort", "location": "Singapore", "pricePerNight": 250, "rating": 4.6},
    {"id": 39, "name": "Chinatown Hotel", "location": "Singapore", "pricePerNight": 120, "rating": 4.2},
    {"id": 40, "name": "Little India Inn", "location": "Singapore", "pricePerNight": 100, "rating": 4.0}
]

# Dictionary to store minimum prices for each location-destination combination
min_prices = {
    "New York": {
        "Paris": {"flight": 450, "hotel": 75},  # From Air France and Budget Inn
        "Tokyo": {"flight": 850, "hotel": 90},  # From Japan Airlines and Sakura Inn
        "London": {"flight": 400, "hotel": 90},  # From British Airways and London Bridge Inn
        "Sydney": {"flight": 950, "hotel": 40},  # From Qantas and Backpacker Hostel
        "San Francisco": {"flight": 300, "hotel": 120},  # From United and Golden Gate Inn
        "Dubai": {"flight": 750, "hotel": 120},  # From Emirates and Dubai Creek Inn
        "Singapore": {"flight": 900, "hotel": 100}  # From Singapore Airlines and Little India Inn
    },
    "London": {
        "Paris": {"flight": 120, "hotel": 75},  # From EasyJet and Budget Inn
        "Tokyo": {"flight": 780, "hotel": 90},  # From British Airways and Sakura Inn
        "New York": {"flight": 400, "hotel": 140},  # From Virgin Atlantic and Central Park Inn
        "Sydney": {"flight": 950, "hotel": 40},  # From Qantas and Backpacker Hostel
        "San Francisco": {"flight": 550, "hotel": 120},  # From British Airways and Golden Gate Inn
        "Dubai": {"flight": 450, "hotel": 120},  # From Emirates and Dubai Creek Inn
        "Singapore": {"flight": 700, "hotel": 100}  # From Singapore Airlines and Little India Inn
    },
    "San Francisco": {
        "Tokyo": {"flight": 750, "hotel": 90},  # From United and Sakura Inn
        "Sydney": {"flight": 900, "hotel": 40},  # From Qantas and Backpacker Hostel
        "Paris": {"flight": 600, "hotel": 75},  # From Air France and Budget Inn
        "London": {"flight": 550, "hotel": 90},  # From United and London Bridge Inn
        "New York": {"flight": 300, "hotel": 140},  # From United and Central Park Inn
        "Dubai": {"flight": 850, "hotel": 120},  # From Emirates and Dubai Creek Inn
        "Singapore": {"flight": 950, "hotel": 100}  # From Singapore Airlines and Little India Inn
    },
    "Paris": {
        "London": {"flight": 120, "hotel": 90},  # From EasyJet and London Bridge Inn
        "Tokyo": {"flight": 800, "hotel": 90},  # From Air France and Sakura Inn
        "New York": {"flight": 450, "hotel": 140},  # From Air France and Central Park Inn
        "Sydney": {"flight": 1000, "hotel": 40},  # From Air France and Backpacker Hostel
        "San Francisco": {"flight": 600, "hotel": 120},  # From Air France and Golden Gate Inn
        "Dubai": {"flight": 500, "hotel": 120},  # From Emirates and Dubai Creek Inn
        "Singapore": {"flight": 750, "hotel": 100}  # From Singapore Airlines and Little India Inn
    },
    "Tokyo": {
        "New York": {"flight": 850, "hotel": 140},  # From Japan Airlines and Central Park Inn
        "London": {"flight": 780, "hotel": 90},  # From Japan Airlines and London Bridge Inn
        "Paris": {"flight": 800, "hotel": 75},  # From Japan Airlines and Budget Inn
        "Sydney": {"flight": 700, "hotel": 40},  # From Japan Airlines and Backpacker Hostel
        "San Francisco": {"flight": 750, "hotel": 120},  # From Japan Airlines and Golden Gate Inn
        "Dubai": {"flight": 650, "hotel": 120},  # From Emirates and Dubai Creek Inn
        "Singapore": {"flight": 450, "hotel": 100}  # From Singapore Airlines and Little India Inn
    },
    "Sydney": {
        "New York": {"flight": 950, "hotel": 140},  # From Qantas and Central Park Inn
        "London": {"flight": 950, "hotel": 90},  # From Qantas and London Bridge Inn
        "Paris": {"flight": 1000, "hotel": 75},  # From Qantas and Budget Inn
        "Tokyo": {"flight": 700, "hotel": 90},  # From Qantas and Sakura Inn
        "San Francisco": {"flight": 900, "hotel": 120},  # From Qantas and Golden Gate Inn
        "Dubai": {"flight": 850, "hotel": 120},  # From Emirates and Dubai Creek Inn
        "Singapore": {"flight": 600, "hotel": 100}  # From Singapore Airlines and Little India Inn
    },
    "Dubai": {
        "New York": {"flight": 750, "hotel": 140},  # From Emirates and Central Park Inn
        "London": {"flight": 450, "hotel": 90},  # From Emirates and London Bridge Inn
        "Paris": {"flight": 500, "hotel": 75},  # From Emirates and Budget Inn
        "Tokyo": {"flight": 650, "hotel": 90},  # From Emirates and Sakura Inn
        "Sydney": {"flight": 850, "hotel": 40},  # From Emirates and Backpacker Hostel
        "San Francisco": {"flight": 850, "hotel": 120},  # From Emirates and Golden Gate Inn
        "Singapore": {"flight": 400, "hotel": 100}  # From Emirates and Little India Inn
    },
    "Singapore": {
        "New York": {"flight": 900, "hotel": 140},  # From Singapore Airlines and Central Park Inn
        "London": {"flight": 700, "hotel": 90},  # From Singapore Airlines and London Bridge Inn
        "Paris": {"flight": 750, "hotel": 75},  # From Singapore Airlines and Budget Inn
        "Tokyo": {"flight": 450, "hotel": 90},  # From Singapore Airlines and Sakura Inn
        "Sydney": {"flight": 600, "hotel": 40},  # From Singapore Airlines and Backpacker Hostel
        "San Francisco": {"flight": 950, "hotel": 120},  # From Singapore Airlines and Golden Gate Inn
        "Dubai": {"flight": 400, "hotel": 120}  # From Singapore Airlines and Dubai Creek Inn
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_min_prices', methods=['POST'])
def get_min_prices():
    start_point = request.form['startPoint']
    destination = request.form['destination']
    
    if start_point and destination and start_point in min_prices and destination in min_prices[start_point]:
        min_price = min_prices[start_point][destination]
        return jsonify({
            "minFlightPrice": min_price["flight"],
            "minHotelPrice": min_price["hotel"]
        })
    return jsonify({"error": "Invalid location combination"})

@app.route('/search_flights', methods=['POST'])
def search_flights():
    start_point = request.form['startPoint']
    destination = request.form['destination']
    start_date = request.form.get('startDate', '')
    
    # Filter flights based on start point and destination only
    filtered_flights = [flight for flight in mock_flights 
                       if flight['from'].lower() == start_point.lower() 
                       and flight['to'].lower() == destination.lower()]
    
    # Add the user's start date to each flight object
    if start_date:
        for flight in filtered_flights:
            flight['display_date'] = start_date
    
    return jsonify(filtered_flights)

@app.route('/search_hotels', methods=['POST'])
def search_hotels():
    destination = request.form['destination']
    budget = int(request.form['budget'])
    filtered_hotels = [hotel for hotel in mock_hotels if hotel['location'].lower() == destination.lower() and hotel['pricePerNight'] <= budget]
    return jsonify(filtered_hotels)

@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_message = request.form['message']
    destination = request.form.get('destination', '').strip()
    start_date = request.form.get('startDate', '')
    end_date = request.form.get('endDate', '')

    if not GEMINI_API_KEY:
        return jsonify({"response": "API key is missing. Please check your configuration."})

    # Check if the question is about flights or hotels
    message_lower = user_message.lower()
    
    # Get relevant flights and hotels data
    relevant_flights = [flight for flight in mock_flights if flight['to'].lower() == destination.lower()]
    relevant_hotels = [hotel for hotel in mock_hotels if hotel['location'].lower() == destination.lower()]
    
    # If question is about flights
    if any(word in message_lower for word in ['flight', 'airline', 'fly', 'flying', 'airport']):
        if not relevant_flights:
            return jsonify({"response": f"I don't have any flight information available for {destination} at the moment."})
        
        # Format flight information
        response = f"Here are the available flights to {destination}:<br><br>"
        for flight in relevant_flights:
            response += f"• {flight['airline']}: ${flight['price']} on {flight['date']}<br>"
        return jsonify({"response": response})
    
    # If question is about hotels
    elif any(word in message_lower for word in ['hotel', 'accommodation', 'stay', 'lodging', 'room']):
        if not relevant_hotels:
            return jsonify({"response": f"I don't have any hotel information available for {destination} at the moment."})
        
        # Format hotel information
        response = f"Here are the available hotels in {destination}:<br><br>"
        for hotel in relevant_hotels:
            response += f"• {hotel['name']}: ${hotel['pricePerNight']}/night, Rating: {hotel['rating']}/5<br>"
        return jsonify({"response": response})

    # For other questions, use the Gemini API
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

    headers = {
        "Content-Type": "application/json"
    }

    # Add date context to the prompt if dates are provided
    date_context = ""
    if start_date and end_date:
        date_context = f"\nThe user is planning to visit from {start_date} to {end_date}. Please consider this date range when providing travel advice, especially for seasonal activities, weather, and events."

    data = {
        "contents": [{
            "parts": [{
                "text": f"""You are a helpful travel assistant. The user's question is: {user_message}
The destination is: {destination}{date_context}

Please provide a helpful response about travel, destinations, or tourism in general. If the user mentions a specific destination, focus on that destination. If not, provide general travel advice.

Please format your response in a clean, readable way:
1. Use proper spacing between paragraphs
2. Use bullet points for lists
3. Keep paragraphs short and focused
4. Use bold text sparingly for important points
5. Avoid excessive formatting or special characters
6. Make the response concise and easy to read
7. If providing an itinerary, make sure to complete all days and include a conclusion"""
            }]
        }],
        "generationConfig": {
            "temperature": 0.7,
            "topK": 40,
            "topP": 0.95,
            "maxOutputTokens": 2048,
            "stopSequences": [],
            "candidateCount": 1
        }
    }

    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()
        
        if response.status_code == 200:
            response_data = response.json()
            if 'candidates' in response_data and len(response_data['candidates']) > 0:
                ai_response = response_data['candidates'][0]['content']['parts'][0]['text']
                # Clean up the response formatting
                ai_response = ai_response.replace('**', '')
                ai_response = ai_response.replace('*', '•')
                ai_response = ai_response.replace('\n\n', '<br><br>')
                ai_response = ai_response.replace('\n', '<br>')
                
                # If the response seems incomplete (ends with a bullet point or mid-sentence)
                if ai_response.strip().endswith('•') or ai_response.strip().endswith(','):
                    # Make another request to complete the response
                    data['contents'][0]['parts'][0]['text'] = f"Complete this response: {ai_response}"
                    response = requests.post(api_url, headers=headers, json=data)
                    response_data = response.json()
                    if 'candidates' in response_data and len(response_data['candidates']) > 0:
                        completion = response_data['candidates'][0]['content']['parts'][0]['text']
                        ai_response += completion
            else:
                print(f"Unexpected API response format: {response_data}")
                ai_response = "I couldn't generate a response. Please try again."
        else:
            print(f"API Error: {response.status_code} - {response.text}")
            ai_response = "Sorry, I encountered an error. Please try again."
            
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {str(e)}")
        ai_response = "Sorry, I encountered an error. Please try again."
    except Exception as e:
        print(f"General Error: {str(e)}")
        ai_response = "Sorry, I encountered an error. Please try again."

    return jsonify({"response": ai_response})


if __name__ == '__main__':
    app.run(debug=True)
