import settings
import forecastio
import sys
from pushbullet import Pushbullet
from geopy.geocoders import Nominatim


geolocator = Nominatim()

pb = Pushbullet(settings.pushBulletApiKey)

print(pb.devices)
# push = pb.push_note("Today's Weather Update", "It's so cold. You should wear a jacket.")

location = geolocator.geocode(settings.home)

forecast = forecastio.load_forecast(settings.forecastioKey,location.latitude ,location.longitude )

print("Choose for when you want to see the weather (Please select a number):")
print("1.Right Now")
print("2.Now to n hours from now(max n = 48)")
print("3.From now to n days onward(max n = 7)")
choice = input("Choice: ")
day = forecast.currently()
if choice == '1':
    day = forecast.currently()
    print(day.summary)
    print(day.temperature)
    print(day.precipProbability)
    sys.exit()
elif choice == '2':
    day = forecast.hourly()
    print(day.summary);
elif choice == '3':
    day = forecast.daily();
    print(day.summary);
else:
    print("Incorrect choice");
    sys.exit();

maxPrecipProb = 0
for x in day.data:
    print(x.precipProbability)
    if x.precipProbability > maxPrecipProb:
        maxPrecipProb = x.precipProbability

if maxPrecipProb > .85:
    pb.push_note("Today's Weather Update", "It is going to rain")
elif maxPrecipProb > .50:
    pb.push_note("Today's Weather Update", "It's probably going to rain")
elif maxPrecipProb > .20:
    pb.push_note("Today's Weather Update", "It's probably not going to rain")
else:
    pb.push_note("Today's Weather Update", "It's not going to rain")
