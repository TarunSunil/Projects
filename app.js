document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('search-form');
    const flightsList = document.getElementById('flights-list');
    const hotelsList = document.getElementById('hotels-list');
    const loading = document.getElementById('loading');
    const noFlights = document.getElementById('no-flights');
    const noHotels = document.getElementById('no-hotels');
    const chatForm = document.getElementById('chat-form');
    const userMessage = document.getElementById('userMessage');
    const chatMessages = document.getElementById('chat-messages');
    const chatSubmitBtn = chatForm.querySelector('button');
    const startPointSelect = document.getElementById('startPoint');
    const destinationSelect = document.getElementById('destination');
    const budgetInput = document.getElementById('budget');
    const minPriceDisplay = document.createElement('div');
    minPriceDisplay.className = 'min-price-display';
    budgetInput.parentNode.insertBefore(minPriceDisplay, budgetInput.nextSibling);

    // Function to update destination options based on start point
    function updateDestinationOptions() {
        const startPoint = startPointSelect.value;
        const options = destinationSelect.options;
        
        // Reset all options
        for (let i = 0; i < options.length; i++) {
            options[i].disabled = false;
        }
        
        // Disable the selected start point in destination dropdown
        if (startPoint) {
            for (let i = 0; i < options.length; i++) {
                if (options[i].value === startPoint) {
                    options[i].disabled = true;
                }
            }
        }
        
        // Reset destination if it's the same as start point
        if (destinationSelect.value === startPoint) {
            destinationSelect.value = '';
        }

        // Update minimum prices
        updateMinPrices();
    }

    // Function to update minimum prices display
    async function updateMinPrices() {
        const startPoint = startPointSelect.value;
        const destination = destinationSelect.value;

        if (startPoint && destination) {
            try {
                const response = await fetch('/get_min_prices', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: `startPoint=${encodeURIComponent(startPoint)}&destination=${encodeURIComponent(destination)}`
                });
                const data = await response.json();
                
                if (!data.error) {
                    minPriceDisplay.innerHTML = `
                        <p>Minimum flight price: $${data.minFlightPrice}</p>
                        <p>Minimum hotel price per night: $${data.minHotelPrice}</p>
                    `;
                    minPriceDisplay.style.display = 'block';
                } else {
                    minPriceDisplay.style.display = 'none';
                }
            } catch (error) {
                console.error('Error fetching minimum prices:', error);
                minPriceDisplay.style.display = 'none';
            }
        } else {
            minPriceDisplay.style.display = 'none';
        }
    }

    // Update destination options when start point changes
    startPointSelect.addEventListener('change', updateDestinationOptions);
    destinationSelect.addEventListener('change', updateMinPrices);

    // Enable chat input after destination is selected
    destinationSelect.addEventListener('change', function() {
        userMessage.disabled = false;
        chatSubmitBtn.disabled = false;
    });

    // Handle search form submission
    searchForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const startPoint = startPointSelect.value;
        const destination = destinationSelect.value;
        const budget = document.getElementById('budget').value;

        if (!startPoint || !destination) {
            alert('Please select both your location and destination');
            return;
        }

        // Show loading
        loading.style.display = 'block';
        flightsList.innerHTML = '';
        hotelsList.innerHTML = '';
        noFlights.style.display = 'none';
        noHotels.style.display = 'none';

        try {
            // Search flights
            const flightsResponse = await fetch('/search_flights', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `startPoint=${encodeURIComponent(startPoint)}&destination=${encodeURIComponent(destination)}&startDate=${encodeURIComponent(document.getElementById('startDate').value)}`
            });
            const flights = await flightsResponse.json();

            // Search hotels
            const hotelsResponse = await fetch('/search_hotels', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `destination=${encodeURIComponent(destination)}&budget=${encodeURIComponent(budget)}`
            });
            const hotels = await hotelsResponse.json();

            // Display results
            displayFlights(flights);
            displayHotels(hotels);

        } catch (error) {
            console.error('Error:', error);
            flightsList.innerHTML = '<li>Error fetching results. Please try again.</li>';
            hotelsList.innerHTML = '<li>Error fetching results. Please try again.</li>';
        } finally {
            loading.style.display = 'none';
        }
    });

    // Handle chat form submission
    chatForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const message = userMessage.value.trim();
        if (!message) return;

        // Disable input and button while processing
        userMessage.disabled = true;
        chatSubmitBtn.disabled = true;

        // Add user message to chat
        addMessage(message, 'user');
        userMessage.value = '';

        // Add loading message
        const loadingMessage = addMessage('Thinking...', 'bot');

        try {
            const startDate = document.getElementById('startDate').value;
            const endDate = document.getElementById('endDate').value;
            const dateRange = startDate && endDate ? `&startDate=${encodeURIComponent(startDate)}&endDate=${encodeURIComponent(endDate)}` : '';
            
            const response = await fetch('/chatbot', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `message=${encodeURIComponent(message)}&destination=${encodeURIComponent(document.getElementById('destination').value)}${dateRange}`
            });
            const data = await response.json();
            
            // Remove loading message
            loadingMessage.remove();
            
            // Add bot response
            addMessage(data.response, 'bot');
        } catch (error) {
            console.error('Error:', error);
            loadingMessage.remove();
            addMessage('Sorry, I encountered an error. Please try again.', 'bot');
        } finally {
            // Re-enable input and button
            userMessage.disabled = false;
            chatSubmitBtn.disabled = false;
            userMessage.focus();
        }
    });

    // Set minimum date for date inputs to today
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('startDate').min = today;
    document.getElementById('endDate').min = today;

    // Update end date minimum when start date changes
    document.getElementById('startDate').addEventListener('change', function() {
        document.getElementById('endDate').min = this.value;
        if (document.getElementById('endDate').value && document.getElementById('endDate').value < this.value) {
            document.getElementById('endDate').value = this.value;
        }
    });

    // Helper functions
    function displayFlights(flights) {
        if (flights.length === 0) {
            noFlights.style.display = 'block';
            noFlights.innerHTML = 'No flights available for this route.';
            return;
        }

        flights.forEach(flight => {
            const li = document.createElement('li');
            li.innerHTML = `
                <strong>${flight.airline}</strong><br>
                From: ${flight.from}<br>
                To: ${flight.to}<br>
                Date: ${flight.display_date || flight.date}<br>
                Price: $${flight.price}
            `;
            flightsList.appendChild(li);
        });
    }

    function displayHotels(hotels) {
        if (hotels.length === 0) {
            noHotels.style.display = 'block';
            return;
        }

        hotels.forEach(hotel => {
            const li = document.createElement('li');
            li.innerHTML = `
                <strong>${hotel.name}</strong><br>
                Location: ${hotel.location}<br>
                Price per night: $${hotel.pricePerNight}<br>
                Rating: ${hotel.rating}/5
            `;
            hotelsList.appendChild(li);
        });
    }

    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        messageDiv.innerHTML = text;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return messageDiv;
    }
}); 
