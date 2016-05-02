import settings
import forecastio
from pushbullet import Pushbullet
from geopy.geocoders import Nominatim

geolocator = Nominatim()

pb = Pushbullet(settings.pushBulletApiKey)

print(pb.devices)
# push = pb.push_note("Today's Weather Update", "It's so cold. You should wear a jacket.")

location = geolocator.geocode(settings.home)

forecast = forecastio.load_forecast(settings.forecastioKey,location.latitude ,location.longitude )
currCast = forecast.currently()
print(currCast.summary)
print(currCast.temperature)
print(currCast.precipProbability)

day = forecast.hourly()


maxPrecipProb = 0
for x in range(12):
    print(day.data[x].precipProbability)
    if day.data[x].precipProbability > maxPrecipProb:
        maxPrecipProb = day.data[x].precipProbability

if maxPrecipProb > .85:
    pb.push_note("Today's Weather Update", "It is going to rain")
elif maxPrecipProb > .50:
    pb.push_note("Today's Weather Update", "It's probably going to rain")
elif maxPrecipProb > .20:
    pb.push_note("Today's Weather Update", "It's probably not going to rain")
else:
    pb.push_note("Today's Weather Update", "It's not going to rain")
