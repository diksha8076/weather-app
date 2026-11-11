from django.shortcuts import render
import requests
import datetime

def get_location_image(lat, lon, city_name):
    try:
        # 1. lat/lon ke aas paas kya famous hai, Wikipedia se pucho
        geo_url = f"https://en.wikipedia.org/w/api.php?action=query&list=geosearch&gscoord={lat}|{lon}&gsradius=10000&gslimit=1&format=json"
        headers = {'User-Agent': 'WeatherApp/1.0'}
        geo_data = requests.get(geo_url, headers=headers, timeout=5).json()

        if geo_data['query']['geosearch']:
            place = geo_data['query']['geosearch'][0]['title']
            # 2. Us place ki photo lo
            summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{place}"
            summary = requests.get(summary_url, headers=headers, timeout=5).json()
            if 'originalimage' in summary:
                return summary['originalimage']['source']

        # Agar paas me kuch na mile to seedha city ki photo lo
        summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{city_name}"
        summary = requests.get(summary_url, headers=headers, timeout=5).json()
        if 'originalimage' in summary:
            return summary['originalimage']['source']
        if 'thumbnail' in summary:
            return summary['thumbnail']['source']

    except:
        pass

    # Last backup - ye bhi city ke naam se fix hai, random nahi
    return f"https://picsum.photos/seed/{city_name.lower()}/1600/900"

def home(request):
    city = 'Indore'
    if request.method == 'POST':
        city = request.POST.get('city', 'Indore')

    api_key = 'c64f5333aeac9f47bcc8b6e3e2ec8942'
    weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'

    try:
        data = requests.get(weather_url).json()
        temp = data['main']['temp']
        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        main_city = data['name']
        lat = data['coord']['lat']
        lon = data['coord']['lon']
    except:
        temp = 28.67
        description = "scattered clouds"
        icon = "03d"
        main_city = city
        lat = 22.7196
        lon = 75.8577

    # Ab image lat/lon se aa rahi hai - location based
    city_image = get_location_image(lat, lon, main_city)
    day = datetime.date.today()

    return render(request, 'weatherapp/index.html', {
        'temp': temp,
        'city': main_city.upper(),
        'description': description,
        'icon': icon,
        'day': day,
        'city_image': city_image,
    })