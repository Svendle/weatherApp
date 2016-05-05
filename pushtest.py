import settings
from pushbullet import Pushbullet
pb = Pushbullet(settings.pushBulletApiKey)
print(pb.devices)

address = " 25 E 85th St, 10028 New York, NY"
# push = pb.push_address("home", address)

to_buy = ["milk", "bread", "cider"]
# push = pb.push_list("Shopping list", to_buy)

push = pb.push_link("Cool site", "https://github.com")

pushes = pb.get_pushes()

for p in pushes:
    print(p)
