# Price Tracker with Discord Notifications

This Python script monitors the price of one or more items from specified websites and sends a Discord notification if the price changes.

## Features

- Configurable per item via an INI file  
- Tracks any site using CSS selectors  
- Sends alerts to a Discord channel via webhook  
- Automatic retry tracking and failure alerts  
- Cron-compatible for periodic checking  

## Requirements

- Python 3.7+  
- `beautifulsoup4`  
- `lxml`  
- `discord-notify` (for Discord webhook integration)  

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/coralcarl/pricetrackr.git
   cd pricetrackr
   ```

2. **Install dependencies**:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Create your config file**:
   Change the `config.ini` file in the project directory with the following structure:

   ```ini
   [DEFAULT]
   discord_webhook = https://discord.com/api/webhooks/yourwebhookurl
   max_retries = 10
   user_agent = Mozilla/5.0 Chrome/125.0.0.0 Safari/537.36

   # ~~ example item ~~
   [Radon Swoop]
   url = https://www.bike-discount.de/de/radon-swoop-10.0-4
   css_selector = #netz-price
   ```

   Optional keys:  
   - `last_seen` — last known price (auto-updated)  
   - `retries` — failed fetch count (auto-updated)  

   Each key can be overwritten by the specific item. For example: You could specify a custom webhook for each one.

## Usage

Run the script manually:

```bash
python3 tracker.py
```

If the price has changed since the last check, a notification will be sent to your Discord webhook.

## Automate with Cron (Linux/macOS)

To run the script every 5 minutes:

1. Open the crontab editor:

   ```bash
   crontab -e
   ```

2. Add the following line (adjust the path as needed):

   ```
   */5 * * * * cd /full/path/to/pricetrackr/ . .venv/bin/activate /usr/bin/python3 tracker.py
   ```

> Tip: You can find the correct Python path with \`which python3\`.

## Notes

- The script directly modifies `config.ini` to store the last seen price and retry count.  
- Ensure `config.ini` is writable by the script.  
