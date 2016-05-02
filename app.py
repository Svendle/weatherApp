import settings
import forecastio
from pushbullet import Pushbullet

pb = Pushbullet(settings.pushBulletApiKey)

print(pb.devices)
