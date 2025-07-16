import requests
from PIL import Image
from io import BytesIO


def get_mars_image(sol = 1000):
    url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol={sol}&api_key=DEMO_KEY"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        image_urls = []
        for image in data["photos"]:
            image_urls.append(image["img_src"])
        return image_urls
    else:
        print(response.status_code)
        
images = get_mars_image()
for img_url in images:
    response = requests.get(img_url)
    img = Image.open(BytesIO(response.content))
    img.show()
    input()

