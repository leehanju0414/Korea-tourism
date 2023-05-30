from PIL import ImageTk, Image
import requests
from io import BytesIO
import googlemaps


def Map_Update(lat, lng, zoom=13):

    Google_API_Key = ""

    map_url = f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{lng}&zoom={zoom}&size=400x400&maptype=roadmap"

    response = requests.get(map_url+'&key='+Google_API_Key)
    image = Image.open(BytesIO(response.content))
    photo = ImageTk.PhotoImage(image)

    return photo