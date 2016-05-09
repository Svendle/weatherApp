import settings
import gcal
import forecastio
import sys
from pushbullet import Pushbullet
from geopy.geocoders import Nominatim


def main(argv):
    geolocator = Nominatim()
    pb = Pushbullet(settings.pushBulletApiKey)
    print(pb.devices)
    # push = pb.push_note("Today's Weather Update", "It's so cold. You should wear a jacket.")

    location = geolocator.geocode(settings.home)
    forecast = forecastio.load_forecast(settings.forecastioKey,location.latitude ,location.longitude )

    precipType = 'None'
    precipIntensity = 0
    today = processDay(forecast)

    # Conditionally set precip type and intensity because they do not exist if
    # there is no chance of precipitation
    if forecast.daily().data[0].precipProbability is not 0:
        precipType = forecast.daily().data[0].precipType
        precipIntensity = forecast.daily().data[0].precipIntensity



    msg = 'You should wear '
    clothingOption = 'summer clothes, it\'s warm today'
    for key in sorted(settings.tempPreference, reverse=True):
        if today['avgTemp'] < key:
            clothingOption = settings.tempPreference[key]
        else:
            break

    msg += clothingOption + '. '

    if today['maxPrecipChance'] > settings.precipThreshold:
        if precipType is not 'snow':
            msg += 'Bring an umbrella, there is a ' + str(today['maxPrecipChance']*100) + '% chance of rain. '
        else:
            msg += 'You should layer up, there is a ' + str(today['maxPrecipChance']*100) + '% chance of snow. '

    if today['avgCloudCover'] < 0.25:
        msg += 'Consider some sunscreen/sunglasses, it\'s going to be sunny today.'



    msg += '\nIt\'s going to be about ' + str(round(today['avgTemp'])) + '˚F today. (Low: ' + str(round(today['minTemp'])) + ', High: ' + str(round(today['maxTemp'])) +')'

    print(msg)
    pb.push_note("Today's Update", msg)


def processDay(forecast):
    today = forecast.hourly().data
    avgTemp = 0;
    avgCloudCover = 0;
    maxPrecipChance = today[0].precipProbability
    maxTemp = today[0].apparentTemperature
    minTemp = maxTemp
    for i in range(settings.hoursAhead):  # look at the coming hours of today, default 12 hours ahead

        hr = today[i]
        temp = hr.apparentTemperature
        maxPrecipChance = hr.precipProbability if hr.precipProbability > maxPrecipChance else maxPrecipChance
        avgCloudCover += hr.cloudCover
        avgTemp += temp
        maxTemp = temp if temp > maxTemp else maxTemp
        minTemp = temp if temp < minTemp else minTemp

    avgTemp /= settings.hoursAhead
    avgCloudCover /= settings.hoursAhead

    return {'maxTemp':maxTemp, 'minTemp':minTemp, 'avgTemp':avgTemp, 'avgCloudCover':avgCloudCover, 'maxPrecipChance':maxPrecipChance}

if __name__ == '__main__':
    main(sys.argv)
