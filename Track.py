import requests
import os
from discord_webhook import DiscordWebhook, DiscordEmbed

print("  _               _           __       _                  _             ")
print(" | |             | |         / _|     | |                | |            ")
print(" | |__   ___  ___| |__   ___| |_ ___  | |_ _ __ __ _  ___| | _____ _ __ ")
print(" | '_ \ / _ \/ __| '_ \ / _ \  _/ __| | __| '__/ _\` |/ __| |/ / _ \ '__|")
print(" | |_) |  __/ (__| | | |  __/ | \__ \ | |_| | | (_| | (__|   <  __/ |   ")
print(" |_.__/ \___|\___|_| |_|\___|_| |___/  \__|_|  \__,_|\___|_|\_\___|_|   ")
print("                                                                        ")
print("by @Lander#0001\n")


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


hook = ""

if os.stat("webhook.txt").st_size == 0:
    print('No webhook found.\n')
    input("Press enter to leave...")
else:
    with open("webhook.txt") as file:
        for line in file:
            line = line.replace("\r", "").replace("\n", "")
            hook = line
    print(bcolors.OKGREEN + "Successfully loaded webhook" + bcolors.ENDC)

courir = int(input("Choose your courir:\n1. BPost\n2. PostNL\n3. DPD\n> "))

# ===========BPOST===========
if courir == 1:
    def bpostHook(status, sender):
        webhook = DiscordWebhook(url=hook, username="BeChefs BPost Tracker")

        embed = DiscordEmbed(title='Bpost Parcel info', color=15158332)
        embed.set_footer(text='BeChefs Bpost Tracker | By Lander#0001')
        embed.set_timestamp()
        embed.set_thumbnail(
            url="https://bpost.media/wp-content/uploads/2017/01/bpost-logo.jpg")
        embed.add_embed_field(name='Tracking Code', value=key, inline='false')
        embed.add_embed_field(name='Parcel Status', value=status +
                              f" {item['activeStep']['label']['detail']['EN']}", inline='false')
        embed.add_embed_field(name='Sender', value=sender, inline='false')

        webhook.add_embed(embed)
        webhook.execute()
    trackingCodes = {}
    if os.stat("bpost.txt").st_size == 0:
        print('No tracking codes found.\n')
    else:
        with open("bpost.txt") as file:
            for line in file:
                line = line.replace("\r", "").replace("\n", "")
                (key, val) = line.split(':')
                trackingCodes[int(key)] = val

    for key, value in trackingCodes.items():
        r = requests.get(
            f"https://trackapi.bpost.cloud/track/items?itemIdentifier={key}&postalCode={value}")
        items = r.json()
        try:
            for item in items['items']:
                print(f"\n======= BPOST PARCEL {key} =======")
                try:
                    print(f"Parcel from: {item['sender']['email']}")
                except KeyError:
                    print(f"Parcel from: {item['sender']['name']}")
                if {item['activeStep']['name']} == {'delivered'}:
                    print(f"Parcel status: {item['activeStep']['label']['main']['EN']} {item['activeStep']['label']['detail']['EN']} on {item['actualDeliveryInformation']['actualDeliveryTime']['day']} at {item['actualDeliveryInformation']['actualDeliveryTime']['time']}")
                else:
                    print(
                        f"Parcel status: {item['activeStep']['label']['main']['EN']} {item['activeStep']['label']['detail']['EN']}")
                print(f"===============================================\n")
            bpostHook(item['activeStep']['label']['main']
                      ['EN'], item['sender']['name'])

            print(bcolors.OKGREEN + "Successfully sent webhook" + bcolors.ENDC)
        except KeyError:
            print(f"======= PARCEL {key} =======")
            print(f"Error: Parcel not found")
            print(f"===============================================\n")


# ===========POSTNL===========
elif courir == 2:
    def postnlHook(status, sender):
        webhook = DiscordWebhook(url=hook, username="BeChefs PostNL Tracker")

        embed = DiscordEmbed(title='PostNL Parcel info', color=15105570)
        embed.set_footer(text='BeChefs PostNL Tracker | By Lander#0001')
        embed.set_timestamp()
        embed.set_thumbnail(
            url="https://seeklogo.com/images/P/postnl-logo-4DA6C08E55-seeklogo.com.png")
        embed.add_embed_field(name='Tracking Code', value=key, inline='false')
        embed.add_embed_field(name='Parcel Status', value=status)
        embed.add_embed_field(name='Sender', value=sender, inline='false')

        webhook.add_embed(embed)
        webhook.execute()

    trackingCodes = {}
    if os.stat("postnl.txt").st_size == 0:
        print('No tracking codes found.\n')
    else:
        with open("postnl.txt") as file:
            for line in file:
                line = line.replace("\r", "").replace("\n", "")
                (key, val) = line.split(':')
                trackingCodes[key] = val
    for key, value in trackingCodes.items():
        r = requests.get(
            f"https://jouw.postnl.be/track-and-trace/api/trackAndTrace/{key}-BE-{value}?language=en")
        items = r.json()
        trackingcode = key
        for item in items['colli']:
            print(f"\n======= POSTNL PARCEL {key} =======")
            if items['colli'][key]['sender']['names']['companyName'] != "":
                print(
                    f"Parcel from: {items['colli'][key]['sender']['names']['companyName']}")
            else:
                print(
                    f"Parcel from: {items['colli'][key]['sender']['names']['personName']}")
            print(
                f"Parcel status: {items['colli'][key]['statusPhase']['message']}")

            print(f"===============================================\n")
            status = items['colli'][key]['statusPhase']['message']
            sender = items['colli'][key]['sender']['names']['companyName']
            postnlHook(status, sender)
            print(bcolors.OKGREEN + "Successfully sent webhook" + bcolors.ENDC)

        if len(items['colli']) == 0:
            print(f"======= PARCEL {key} =======")
            print(f"Error: Parcel not found")
            print(f"===============================================\n")


# ===========DPD===========
elif courir == 3:
    def dpdHook(status, location):
        webhook = DiscordWebhook(url=hook, username="BeChefs DPD Tracker")

        embed = DiscordEmbed(title='DPD Parcel info', color=15158332)
        embed.set_footer(text='BeChefs DPD Tracker | By Lander#0001')
        embed.set_timestamp()
        embed.set_thumbnail(
            url="https://play-lh.googleusercontent.com/60IgxaBiFGQVSqq7WHSRqr2hIl2OQNaS-vhmcNtLbA9QmG-OiIjfFQpwzWQ45j7wlsM")
        embed.add_embed_field(name='Tracking Code',
                              value=line, inline='false')
        embed.add_embed_field(name='Parcel Status', value=status)
        embed.add_embed_field(name='Current Location',
                              value=location, inline='false')

        webhook.add_embed(embed)
        webhook.execute()

    dpdcodes = []
    if os.stat("dpd.txt").st_size == 0:
        print('No tracking codes found.\n')
    else:
        with open("dpd.txt") as file:
            for line in file:
                line = line.replace("\r", "").replace("\n", "")
                dpdcodes.append(line)
    for i in dpdcodes:
        r = requests.get(f"https://tracking.dpd.de/rest/plc/en_BE/{i}")
        items = r.json()
        last_status = items['parcellifecycleResponse']['parcelLifeCycleData']['statusInfo']
        for s in last_status:
            if s['isCurrentStatus'] == True:
                print(f"\n======= DPD PARCEL {i} =======")
                print(f"Parcel Status: {s['description']['content'][0]}")
                print(f"Parcel Location: {s['location']}")
                print(f"===============================================\n")
                status = s['description']['content'][0]
                location = s['location']
                dpdHook(status, location)
                print(bcolors.OKGREEN + "Successfully sent webhook" + bcolors.ENDC)
            else:
                pass


elif type(courir) is not int:
    print("Invalid input.")

input("Press enter to leave...")
