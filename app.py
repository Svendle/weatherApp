import settings
import forecastio
from pushbullet import Pushbullet
from geopy.geocoders import Nominatim

geolocator = Nominatim()

pb = Pushbullet(settings.pushBulletApiKey)

print(pb.devices)
# push = pb.push_note("Today's Weather Update", "It's so cold. You should wear a jacket.")

location = geolocator.geocode(settings.home)
print((location.latitude, location.longitude))

forecast = forecastio.load_forecast(settings.forecastioKey,location.latitude ,location.longitude )
currCast = forecast.currently()
print(currCast.summary)
print(currCast.temperature)
print(currCast.precipProbability)

day = forecast.hourly()
print(day.summary)
