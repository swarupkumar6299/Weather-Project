from django.shortcuts import render
from django.contrib import messages
import requests
import datetime

# Create your views here.
def home(request):

    if request.method == 'POST' and 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'Hyderabad'

    weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid='

    weather_params = {'units': 'metric'}
# Google Searc API
    API_KEY = ''

    SEARCH_ENGINE_ID = ''

    query = city + " 1920x1080"
    search_url = (
        f"https://www.googleapis.com/customsearch/v1?"
        f"key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&searchType=image&imgSize=xlarge"
    )
    try:
        #Get Weather Data
        weather_response = requests.get(weather_url, params=weather_params)
        weather_data = weather_response.json()
        #Handel invalid data
        if weather_response.status_code != 200 or 'main' not in weather_data:
            raise ValueError("City not found")
        description = weather_data['weather'][0]['description']
        icon = weather_data['weather'][0]['icon']
        temp = weather_data['main']['temp']
        day = datetime.date.today()

        #Chat Gpt for weather
        #weather_data = requests.get(url, params=PARAMS).json()
        #description = weather_data['weather'][0]['description']
        #icon = weather_data['weather'][0]['icon']
        #temp = weather_data['main']['temp']
        #day = datetime.date.today()

        #Image Search Data
        image_data = requests.get(search_url).json()
        search_items = image_data.get("items", [])
        image_url = search_items[0]['link'] if search_items else ''
        
        return render(request, 'index.html', {
            'description': description,
            'icon': icon,
            'temp': temp,
            'day': day,
            'city': city,
            'exception_occurred': False,
            'image_url': image_url
        })

    except ValueError as ve:
        # City not found or weather data missing
        messages.error(request, f"City '{city}' not found. Please enter a valid city name.")
    except Exception as e:
        #Any othe message
        messages.error(request, 'Something went wrong while fetching data.')

    
        # Default fallback data
    day = datetime.date.today()
    return render(request, 'index.html', {
        'description': 'clear sky',
        'icon': '01d',
        'temp': 25,
        'day': day,
        'city': 'Hyderabad',
        'exception_occurred': True,
        'image_url': ''
    })