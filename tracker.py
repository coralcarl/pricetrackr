import urllib.request
import discord_notify as dn
import html
from bs4 import BeautifulSoup
from datetime import datetime
from configparser import ConfigParser

def notify(webhook, message):
    try:
        notifier = dn.Notifier(webhook)
        notifier.send(message)
    except Exception as err:
        print(f"Could not notify: {err}\n")
        return False
    return True


if __name__ == "__main__":
    config = ConfigParser()
    config.read('config.ini')

    for section in config:
        if section == 'DEFAULT':
            continue

        headers = {
            "User-Agent": config.get(section, 'user_agent')
        }

        req = urllib.request.Request(config.get(section, 'url'), headers=headers)

        try:
            response = urllib.request.urlopen(req)
            contents = response.read().decode('utf-8')
            contents = html.unescape(contents)

        except Exception as err:
            retries = config.getint(section, 'retries', fallback=0)

            if retries == config.getint(section, 'max_retries'):
                notify(config.get(section, 'discord_webhook'), f"Maximum retries exceeded for {section}")

            config[section]['retries'] = str(retries + 1)

        else:
            config[section]['retries'] = '0'
            soup = BeautifulSoup(contents, 'lxml')
            price = soup.select_one(config.get(section,'css_selector')).text.strip()

            if price != config.get(section, 'last_seen', fallback=0):
                if notify(config.get(section, 'discord_webhook'), f'New price for {section}: {price}'):
                    config[section]['last_seen'] = price

    with open('config.ini', 'w') as f:
        config.write(f)
