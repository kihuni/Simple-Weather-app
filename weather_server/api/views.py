from django.http import JsonResponse
import requests

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_weather_and_location(ip):
    if ip == "127.0.0.1":
        # Mock data for local development
        return "New York", 11

    # Actual implementation for production
    location_api_url = f'http://ip-api.com/json/{ip}'
    weather_api_url = 'https://api.openweathermap.org/data/2.5/weather'
    weather_api_key = 'YOUR_WEATHER_API_KEY'

    try:
        location_response = requests.get(location_api_url).json()
        city = location_response.get('city', 'Unknown')
        lat = location_response.get('lat')
        lon = location_response.get('lon')

        if lat is None or lon is None:
            raise ValueError("Could not determine location from IP address")

        weather_response = requests.get(weather_api_url, params={
            'lat': lat,
            'lon': lon,
            'appid': weather_api_key,
            'units': 'metric'
        }).json()

        temperature = weather_response['main']['temp']
        return city, temperature

    except (requests.RequestException, ValueError, KeyError) as e:
        # Handle error and return a default response
        return "Unknown", 0

def hello(request):
    visitor_name = request.GET.get('visitor_name', 'Guest')
    client_ip = get_client_ip(request)
    city, temperature = get_weather_and_location(client_ip)

    response_data = {
        'client_ip': client_ip,
        'location': city,
        'greeting': f'Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {city}'
    }

    return JsonResponse(response_data)
