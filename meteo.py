import logging
import logging.handlers
import os

import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)

try:
    SOME_SECRET = os.environ["SOME_SECRET"]
except KeyError:
    SOME_SECRET = "Token not available!"
    #logger.info("Token not available!")
    #raise


if __name__ == "__main__":
    logger.info(f"Token value: {SOME_SECRET}")

    r = requests.get('https://weather.talkpython.fm/api/weather/?city=Douala&country=CM')
    if r.status_code == 200:
        data = r.json()
        temperature = data["forecast"]["temp"]
        ressenti = data["forecast"]['feels_like']
        humidity = data['forecast']['humidity']
        
        WEATHER_COMMENT = " "
        
        if ressenti > 35 :
            WEATHER_COMMENT = "Que calor ! Il fait chaud hydratez vous."
        elif ressenti <= 28 :
            WEATHER_COMMENT = "Il fait doux aujourd'hui profitez de la journee"
        else : 
            WEATHER_COMMENT = "C'est mieux que certaines fois :]"
            
        with open("meteo.txt", "w") as f:
            f.write("TEMPERATURE={}\nHUMIDITY={}\nWEATHER_COMMENT={}".format(temperature, humidity,WEATHER_COMMENT))
            
        logger.info(f'Weather in Douala: {temperature}')
