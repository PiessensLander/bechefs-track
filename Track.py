import requests
import os
import concurrent.futures
import random
from datetime import datetime
from discord_webhook import DiscordWebhook, DiscordEmbed


print("  _               _           __       _                  _             ")
print(" | |             | |         / _|     | |                | |            ")
print(" | |__   ___  ___| |__   ___| |_ ___  | |_ _ __ __ _  ___| | _____ _ __ ")
print(" | '_ \ / _ \/ __| '_ \ / _ \  _/ __| | __| '__/ _\` |/ __| |/ / _ \ '__|")
print(" | |_) |  __/ (__| | | |  __/ | \__ \ | |_| | | (_| | (__|   <  __/ |   ")
print(" |_.__/ \___|\___|_| |_|\___|_| |___/  \__|_|  \__,_|\___|_|\_\___|_|   ")
print("                                                                        ")
print("by @Lander#0001 & @Drerman#0001\n")


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

courir = int(input("What are you here for? \n1. Track BPost\n2. Track PostNL\n3. Track DPD\n4. Check Footlocker Orders \n > "))

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
            print(bcolors.OKGREEN + "Successfully sent webhook to Discord")
        except KeyError:
            print(f"======= PARCEL {key} =======")
            print(f"Error: Parcel not found")
            print(f"===============================================\n")

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
            print(bcolors.OKGREEN + "Successfully sent webhook to Discord")

        if len(items['colli']) == 0:
            print(f"======= PARCEL {key} =======")
            print(f"Error: Parcel not found")
            print(f"===============================================\n")

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
            else:
                pass
elif courir == 4:

    def ftlHook(order, item, status, tracking, image):
        webhook = DiscordWebhook(url=hook, username="BeChefs FTL Tracker", avatar_url="https://ih1.redbubble.net/image.1154630742.4997/poster,504x498,f8f8f8-pad,600x600,f8f8f8.jpg")
        embed = DiscordEmbed(title='FTL Order info', color=15158332)
        embed.set_footer(text='BeChefs FTL Tracker | By Lander#0001 & Drerman#0001')
        embed.set_timestamp()
        embed.add_embed_field(name='Order', value=order, inline='false')
        if(image != None):
            embed.set_thumbnail(url=image)
        if(item != None):
            embed.add_embed_field(name='Item', value=item, inline='false')
        embed.add_embed_field(name='Order Status', value=status, inline='false')
        if tracking != None:
            embed.add_embed_field(name='Tracking Code', value=tracking, inline='false')
        else:
            embed.add_embed_field(name='Tracking Code', value="Not available", inline='false')
        webhook.add_embed(embed)
        webhook.execute()


    def CheckFtlOrder(ordernumber, proxies):
        dateTimeObj = datetime.now()
        proxy = random.choice(proxies)

        x = proxy.split(':')
        
        usedproxy = {
            "http" : "http://{0}:{1}@{2}:{3}".format(x[2], x[3], x[0], x[1])
        }
        headers = {
        'x-forwarded-for' : '127.0.0.1',
        'accept': '*/*',
        'accept-encoding' : 'gzip, deflate, br',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent' : 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36',
        'referer': 'https://footlocker.narvar.com/footlocker/tracking/startrack?order_number={0}'.format(ordernumber)
        }
        url = ('https://footlocker.narvar.com/tracking/itemvisibility/v1/footlocker/orders/{0}?order_number={0}&tracking_url=https%3A%2F%2Ffootlocker.narvar.com%2Ffootlocker%2Ftracking%2Fstartrack%3Forder_number%3D{0}'.format(ordernumber))
        responsebefore = requests.get(url, headers= headers, proxies=usedproxy)
        if(responsebefore.status_code != 200):
            print(bcolors.WARNING + responsebefore.status_code)
        else:
            print("[",dateTimeObj.hour,':',dateTimeObj.minute,':',dateTimeObj.second,"]",end=" ")
            print(bcolors.OKGREEN + '[{0}]'.format(ordernumber), end=" ")
            print(bcolors.OKGREEN + '[{0}]'.format(responsebefore.status_code), end=" ")
            ftldata = responsebefore.json()
            try:
                image = 'http://' + ftldata['order_info']['order_items'][0]['item_image'][2:]
                name = ftldata['order_info']['order_items'][0]['name']
                #sizesku = ftldata['order_info']['order_items'][0]['sku']
            except:
                image= ""
                name = ""
            status = ""
            if(ftldata['status'] == "FAILURE"):
                print(bcolors.WARNING + "GHOST ORDER / NOT PROCESSED",bcolors.ENDC)
                status = "Ghost Order / Not Processed"
                ftlHook(ordernumber, None, status, "Not Available", None)
            else:
                if( not ftldata['order_info']['order_items']):
                    print(bcolors.WARNING + "ORDER OVERSOLD / CANCELLED",bcolors.ENDC)
                    status = "cancelled"
                    ftlHook(ordernumber, name, status, "Not Available", image)
                else:
                    for item in ftldata['order_info']['order_items']:
                        
                        print("{0} - ".format(item['name'] ), end=" ")

                        if('tracking_info' not in ftldata):
                            print(bcolors.WARNING + "NOT SHIPPED",bcolors.ENDC)
                            status = "NOT SHIPPED YET"
                            ftlHook(ordernumber, name, status, "Not Available", image)
                        else:
                            try:
                                print(bcolors.OKGREEN + 'SHIPPED',bcolors.ENDC)
                                status = ftldata['order_info']['order_items'][0]['fulfillment_status']
                                carrier = ftldata['order_info']['shipments'][0]['carrier']
                                trackingnumber = ftldata['order_info']['shipments'][0]['tracking_number']
                                ftlHook(ordernumber, name, status, f"{carrier} - {trackingnumber}", image)
                            except:
                                pass
                                    
    proxies = []
    ordernummers = []
    if os.stat("footlocker.txt").st_size == 0:
        print('No footlocker orders found.\n')
    else:
        if os.stat("proxies.txt").st_size == 0:
            print('No proxies file found.\n')
        else:
            orders = open('footlocker.txt', 'r+')
            for line in orders:
                fields = line.split("\n")
                for field in fields:
                    if field == "":
                        pass
                    else:
                        ordernummers.append(field)
            proxy = open('proxies.txt', 'r+')
            for line in proxy:
                fields = line.split("\n")
                for field in fields:
                    if field == "":
                        pass
                    else:
                        proxies.append(field)        
            for order in ordernummers:
               CheckFtlOrder(order,proxies)

elif type(courir) is not int:
    print("Invalid input.")

input("Press enter to leave...")
