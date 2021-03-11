import requests
import os

def get_current_conditions():
    """return a dict with the current weather information."""
    
    eng_to_french = {
        'clear sky': 'ciel clair',
        'few clouds': 'quelques nuages',
        'scattered clouds': 'nuages épars',
        'broken clouds': 'nuageux avec éclaircies',
        'shower rain': 'averses',
        'rain': 'pluie',
        'thunderstorm': 'orages',
        'snow': 'neige',
        'mist': 'brouillard',
        'overcast clouds': 'couvert'
    }
    lat, lon = (45.449213, 4.254920) # Coordonnées de la base nautique
    api_key = str(os.environ['OW_API_KEY']) 
    unit = 'metric'
    base_url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units={unit}'
    
    r = requests.get(base_url).json()    
    
    result = {}
    try:
        result['weather_descr'] = eng_to_french[r['weather'][0]['description'].lower()]
    except:
        result['weather_descr'] = 'Inconnu'
    result['weather_icon_url'] = f'http://openweathermap.org/img/wn/{r["weather"][0]["icon"]}@2x.png' 
    result['wind_deg'] = int(r['wind']['deg']) + 180
    result['wind_speed'] = round(float(r['wind']['speed']) * 1.94384)
    result['temp'] = round(float(r['main']['temp']))
    result['temp_felt'] = round(float(r['main']['feels_like']))   
    return result

def get_hourly_conditions():
    """return a dict with the weather information by slot of 3 hours."""
    
    lat, lon = (45.449213, 4.254920) # Coordonnées de la base nautique
    api_key = str(os.environ['OW_API_KEY']) 
    unit = 'metric'
    base_url = f'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units={unit}'
    
    r = requests.get(base_url).json()    

    forecast = {}
    for hour in r['list']:
        day = hour['dt_txt'].split(' ')[0]
        if day not in forecast:
            forecast[day] = {}

        time = int(hour['dt_txt'].split(' ')[1].split(':')[0])
        print(time)
        forecast[day][time] = {}
        forecast[day][time]['weather'] = hour['weather'][0]['description']
        forecast[day][time]['weather_icon_url'] = f'http://openweathermap.org/img/wn/{hour["weather"][0]["icon"]}@2x.png' 
        forecast[day][time]['temp'] = round(float(hour['main']['temp_max']))
        forecast[day][time]['wind_deg'] = int(hour['wind']['deg']) + 180
        forecast[day][time]['wind_speed'] = round(float(hour['wind']['speed']) * 1.94384)

    return forecast

