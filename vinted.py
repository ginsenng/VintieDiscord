# Updated at : 26/05/2022 15:07
# Version : 2
# Description : Vinted Bot
# Language : Python



import os
import json
import shutil
import threading
import time
import sys
try:
    import requests
    from bs4 import BeautifulSoup
except:
    os.system("pip install requests")
    os.system("pip install bs4")


class Spy:
    gris = "\033[1;30;1m"
    rouge = "\033[1;31;1m"
    vert = "\033[1;32;1m"
    jaune = "\033[1;33;1m"
    bleu = "\033[1;34;1m"
    violet = "\033[1;35;1m"
    cyan = "\033[1;36;1m"
    blanc = "\033[1;0;1m"


def get_info_post(url):
    try:
        time.sleep(2)
        print(f"{Spy.blanc}[{Spy.gris}RECHERCHE{Spy.blanc}] - Le bot recupere les informations de l'item...")
        headers = requests.utils.default_headers()
        headers.update({'User-agent': 'Mozilla/5.0'})
        reponse = requests.get(str(url), headers=headers)
        soup = BeautifulSoup(reponse.text, "html.parser")

        res = soup.findAll('script', {"class": "js-react-on-rails-component"})

        descindice = 0
        userinfoindice = 0
        for i in range(len(res)):
            if 'data-component-name="ItemDescription"' in str(res[i]).split():
                descindice = i
            if 'data-component-name="ItemUserInfo"' in str(res[i]).split():
                userinfoindice = i

        description = json.loads(res[descindice].text.replace(
            '<script class="js-react-on-rails-component" data-component-name="ItemDescription" data-dom-id="ItemDescription-react-component-3d79657d-a1b5-4f1d-b501-2f470f328c66" type="application/json">',
            "").replace("</script>", ''))

        userinfo = json.loads(res[userinfoindice].text.replace(
            '<script class="js-react-on-rails-component" data-component-name="ItemUserInfo" data-dom-id="ItemUserInfo-react-component-2105d904-b161-47d1-bfce-9b897a8c1cc6" type="application/json">',
            '').replace("</script>", ''))

        titre = description["content"]["title"]
        description = description["content"]["description"]
        positive = userinfo["user"]["positive_feedback_count"]
        negative = userinfo["user"]["negative_feedback_count"]
        username = userinfo["user"]["login"]
        pays = userinfo["user"]["country_title"]
        ville = userinfo["user"]["city"]

        lesinfo = {}

        if titre == "":
            titre = "Pas de donn??e"
        if description == "":
            description = "Pas de donn??e"
        if positive == "":
            positive = "Pas de donn??e"
        if negative == "":
            negative = "Pas de donn??e"
        if username == "":
            username = "Pas de donn??e"
        if pays == "":
            pays = "Pas de donn??e"
        if ville == "":
            ville = "Pas de donn??e"

        try:
            lesinfo["titre"] = titre
            lesinfo["description"] = description
            lesinfo["positive"] = positive
            lesinfo["negative"] = negative
            lesinfo["username"] = username
            lesinfo["pays"] = pays
            lesinfo["ville"] = ville
        except Exception as err:
            print(err)
        return lesinfo
    except:
        pass


def search(url):
    try:
        time.sleep(5)
        print(f"{Spy.blanc}[{Spy.gris}RECHERCHE{Spy.blanc}] - Le bot cherche des nouveaux items...")
        headers = requests.utils.default_headers()
        headers.update({'User-agent': 'Mozilla/5.0'})
        reponse = requests.get(str(url), headers=headers)
        if 429 == reponse.status_code:
            print(f"{Spy.blanc}[{Spy.rouge}ERREUR{Spy.blanc}] - Rate Limit !")
            time.sleep(10)
        soup = BeautifulSoup(reponse.text, "html.parser")

        res = soup.findAll('script')
        indices = 0
        for i in range(len(res) + 1):
            if 'data-js-react-on-rails-store="MainStore"' in str(res[i]).split():
                indices += i
                break
        value = res[indices].text.replace('<script z-js-react-on-rails-store="MainStore" type="application/json">', "")
        z = json.loads(value)
        return z
    except:
        pass

with open("config.json", 'r') as config:
    configs = json.load(config)

try:
    os.system('cls')
except:
    os.system('clear')



asciiart = f"""{Spy.rouge}
?????????   ??????????????????????????????  ????????????????????? ???????????????????????????
?????????   ???????????????????????????????????????????????????????????????????????????????????????
?????????   ??????????????????????????????????????????   ?????????   ?????????   
???????????? ?????????????????????????????????????????????   ?????????   ?????????   
 ????????????????????? ???????????????????????????????????????????????????   ?????????   
  ???????????????  ?????????????????????  ?????????????????????    ?????????   
                   \n\n"""

print(asciiart + "\n\n")

posting = []


sys.stdout.write("\x1b]2;Vinted Bot\x07")
class moniteur:
    def __init__(self, weburl, url):
        while True:
            try:
                z = search(str(url))
                x = z["items"]["catalogItems"]["byId"]
                dictlist = list(x)
                for i in range(9, -1, -1):
                    time.sleep(1)
                    post = dictlist[i - 1]
                    if str(post) in posting:
                        print(f"{Spy.blanc}[{Spy.rouge}{post}{Spy.blanc}] - Item d??j?? envoy?? !")
                        time.sleep(1)
                        continue
                    else:
                        print(f"{Spy.blanc}[{Spy.blanc}{post}{Spy.jaune}] - Nouvel item trouv?? !")
                        info = get_info_post(x[str(post)]["url"])

                        data = {"username": "Discord Vinted BOT",
                                "avatar_url": "https://cdn.discordapp.com/avatars/755734583005282334/158a0c81f5a3bd1f283bedd5f817a524.webp?size=1024",
                                "embeds": [
                                    {
                                        "color": configs["embed-color"],
                                        "fields": [

                                        ],
                                        "image": {
                                            "url": x[post]["photo"]["thumbnails"][4]["url"]
                                        },
                                        "url": x[post]['url'],
                                        "title": f"``?????????`` **{x[post]['title']}**",
                                        "footer": {
                                            "icon_url": "https://cdn.discordapp.com/avatars/755734583005282334/158a0c81f5a3bd1f283bedd5f817a524.webp?size=1024"
                                        }
                                    }]}
                        if configs["embed-config"]["prix"] == "oui":
                            data["embeds"][0]["fields"].append(
                                {
                                    "name": "**``???????``__Prix__**",
                                    "value": f"```{configs['embed-color-text']}\n{x[post]['price']}???```",
                                    "inline": True
                                })

                        if configs["embed-config"]["taille"] == "oui":
                            if x[post]['size_title'] == "":
                                size_title = "Pas de donn??e"
                            else:
                                size_title = x[post]['size_title']
                            data["embeds"][0]["fields"].append({
                                "name": "**``???????`` __Taille__**",
                                "value": f"```{configs['embed-color-text']}\n{size_title}```",
                                "inline": True
                            })

                        if configs["embed-config"]["marque"] == "oui":
                            data["embeds"][0]["fields"].append(
                                {
                                    "name": "**``????`` Marque**",
                                    "value": f"```{configs['embed-color-text']}\n{x[post]['brand_title']}```",
                                    "inline": True
                                }
                            )

                        if configs["embed-config"]["avis"] == "oui":
                            data["embeds"][0]["fields"].append({
                                "name": "``????``/``????`` **Note du vendeur**",
                                "value": f"```{configs['embed-color-text']}\n{str(info['positive'])} - {str(info['negative'])}```",
                                "inline": True
                            })

                        if configs["embed-config"]["localisation"] == "oui":
                            data["embeds"][0]["fields"].append({
                                "name": "**``????`` Emplacement **",
                                "value": f"```{configs['embed-color-text']}\n{info['pays']}, {info['ville']}```",
                                "inline": True
                            })

                        if configs["embed-config"]["vendeur"] == "oui":
                            data["embeds"][0]["fields"].append({
                                "name": "**``????`` Auteur**",
                                "value": f"```{configs['embed-color-text']}\n{info['username']}```",
                                "inline": True
                            })
                        result = requests.post(weburl, json=data)
                        posting.append(str(post))
                        print(f"{Spy.blanc}[{Spy.bleu}POSTE{Spy.blanc}] - Poste envoy?? !")
            except:
                time.sleep(10)


if len(configs["suburl"]) > 100:
    print(
        f"{Spy.blanc}[{Spy.rouge}ERREUR{Spy.blanc}] - Trop de salon veuillez en enlever car le bot se fera rate limit !")
else:
    for webhurl in configs["suburl"]:
        print(
            f"{Spy.blanc}[{Spy.violet}LANCEMENT{Spy.blanc}] - Lancement de la t??che dans le salon {Spy.jaune}{configs['suburl'][webhurl]['salon']}")

        t = threading.Thread(target=moniteur, args=[webhurl, configs["suburl"][str(webhurl)]["url"]])
        t.start()
