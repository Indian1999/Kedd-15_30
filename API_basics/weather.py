import requests

def get_weather(city, format = 3, lang="hu"):
    url = f"https://wttr.in/{city}?format={format}&lang={lang}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.text
    else:
        print("ERROR:", response.status_code)
    
    
budapest = get_weather("Budapest", "%l:%c%C+%m+%t+%T+%Z")
print(budapest)

budapest = get_weather("Wroclaw", "%l:%c%C+%m+%t+%T+%Z", "pl")
print(budapest)


"""
    c    Weather condition,
    C    Weather condition textual name,
    x    Weather condition, plain-text symbol,
    h    Humidity,
    t    Temperature (Actual),
    f    Temperature (Feels Like),
    w    Wind,
    l    Location,
    m    Moon phase 🌑🌒🌓🌔🌕🌖🌗🌘,
    M    Moon day,
    p    Precipitation (mm/3 hours),
    P    Pressure (hPa),
    u    UV index (1-12),

    D    Dawn*,
    S    Sunrise*,
    z    Zenith*,
    s    Sunset*,
    d    Dusk*,
    T    Current time*,
    Z    Local timezone.

(*times are shown in the local timezone)
"""