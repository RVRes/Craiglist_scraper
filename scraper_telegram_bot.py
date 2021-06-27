#!/home/roman/scripts/craiglis_scrap/venv/bin/python
import requests
import json
import pickle
from datetime import datetime, timedelta
import re
import os

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

CAR = {
    'LINKS': [
        'https://austin.craigslist.org/d/cars-trucks/search/cta'
        'https://austin.craigslist.org/d/cars-trucks/search/cta?s=120',
        'https://austin.craigslist.org/d/cars-trucks/search/cta?s=240',
        'https://austin.craigslist.org/d/cars-trucks/search/cta?s=360',
        'https://austin.craigslist.org/d/cars-trucks/search/cta?s=480',
        'https://austin.craigslist.org/d/cars-trucks/search/cta?s=600',
        'https://austin.craigslist.org/d/cars-trucks/search/cta?s=720',
        'https://austin.craigslist.org/d/cars-trucks/search/cta?s=840',
        'https://austin.craigslist.org/d/cars-trucks/search/cta?s=960',
        'https://austin.craigslist.org/d/cars-trucks/search/cta?s=1080',
        'https://austin.craigslist.org/d/cars-trucks/search/cta?s=1200',
        'https://austin.craigslist.org/d/cars-trucks/search/cta?s=1320',
        'https://austin.craigslist.org/d/cars-trucks/search/cta?s=1440',
        'https://austin.craigslist.org/d/cars-trucks/search/cta?s=1560',
        'https://austin.craigslist.org/d/cars-trucks/search/cta?s=1680',
        'https://austin.craigslist.org/d/cars-trucks/search/cta?s=1800',
        'https://austin.craigslist.org/d/cars-trucks/search/cta?s=1920',
        'https://austin.craigslist.org/d/cars-trucks/search/cta?s=2040',
        'https://austin.craigslist.org/d/cars-trucks/search/cta?s=2160',
        'https://austin.craigslist.org/d/cars-trucks/search/cta?s=2280',
        'https://austin.craigslist.org/d/cars-trucks/search/cta?s=2400',
        'https://austin.craigslist.org/d/cars-trucks/search/cta?s=2520',
        'https://austin.craigslist.org/d/cars-trucks/search/cta?s=2640',
        'https://austin.craigslist.org/d/cars-trucks/search/cta?s=2760',
        'https://austin.craigslist.org/d/cars-trucks/search/cta?s=2880'
    ],
    'type': 'car',
    'output_file': 'car_data',
    'scrap_time': None
}


def save_settings(opt: dict):
    with open(f'{THIS_DIR}/Secrets/settings.txt', 'w') as outfile:
        json.dump(opt, outfile)


def load_settings() -> dict:
    with open(f'{THIS_DIR}/Secrets/settings.txt') as json_file:
        data = json.load(json_file)
    return data


def send_telegram(channels: str, text: str):
    method = url + "/sendMessage"
    method_test = url + '/getUpdates'  # в ответе requests смотрим чат id

    # print(method)
    # r = requests.get(method_test)
    # print(r)
    for channel_id in channels:
        r = requests.post(method, data={
            "chat_id": channel_id,
            "text": text
        })
        if r.status_code != 200:
            raise Exception(r.status_code)


def find_model_year(input_list: list):
    pattern = '(20|19)\d\d'
    for item in input_list:
        cs = (item['name'] + item['info'] if 'info' in item.keys() else '')
        year = re.search(pattern, cs)
        item['year'] = str(year[0]) if year else None


def find_car_model(input_list: list):
    VENDORS = ['toyota', 'nissan', 'hyundai', 'ford', 'mitsubishi', 'mazda', 'honda', 'cadillac', 'chevrolet', 'kia',
               'audi', 'mercedes', 'lexus', 'jeep', 'volkswagen', 'dodge', 'bmw', 'chrysler', 'mini cooper',
               'range rover']
    MODELS = ['camry', 'corolla', 'elantra', 'focus', 'sentra', 'lancer', 'altima', 'civic', 'crown', 'fiesta',
              'accent',
              'tucson', 'accord', 'rogue', 'cube', 'prius', 'escape', 'cr-v', 'tundra', 'sienna', 'cruze', 'outlander',
              'avalon', 'murano', 'explorer', 'cx9', 'mustang', 'mazda 3', 'mazda3', 'optima', 'f250', 'soul', 'f-150',
              'f150', 'sonata', 'eclipse', 'flex', 'ranger', 'mirage', 'q5', 'veloster', 'glk 350', 'edge', 'es350',
              'srx', 'odyssey', 'juke', 'frontier', 'expedition', 'taurus', 'santa fe', 'compass', 'cherokee', 'golf',
              'durango', '535xi', 'charger', 'is 250', 'sorento', 'pathfinder', 'venza', 'e 350', 'pilot', 'f-350',
              'trax', 'mx-5', 'cx-5', 'forte', 'cts', 'scion', 'ats', 'versa', 'thunderbird', 'mazda 5', 'fusion',
              'tiguan', 'f-510', 'fit lx', 'ct 200h', 'sedona', '200 s', 'hardtop', 'mazda 6', '528i', 'chrysler 200',
              'range rover', 'transit', 'rav 4', 'rav4', 'endeavaor', 'sportage']

    for item in input_list:
        name = item['name'].lower() if item and 'name' in item.keys() and item['name'] else ''
        info = item['info'].lower() if item and 'info' in item.keys() and item['info'] else ''
        car_vendor = [vendor for vendor in VENDORS if vendor in name]
        car_model = [model for model in MODELS if model in name]
        car_vendor = car_vendor if car_vendor else [vendor for vendor in VENDORS if vendor in info]
        car_model = car_model if car_model else [model for model in MODELS if model in info]
        item['vendor'] = car_vendor[0].title() if isinstance(car_vendor, list) and car_vendor else ''
        item['model'] = car_model[0].title() if isinstance(car_model, list) and car_model else ''


def filter_car_result(arg, raw_result):
    EXCEPTIONS = []
    date_from = (datetime.today() - timedelta(days=2)).date()

    result = []
    ids = []
    pnotts = []
    for item in raw_result:
        item_date = datetime.strptime(item['datetime'], '%Y-%m-%d').date()
        cs = (str(item['price']) + item['name'] + item['info'] if 'info' in item.keys() else '').lower()
        pnott = (str(item['price']) + item['name'] +
                 item['fuel'] if 'fuel' in item.keys() else '' +
                                                            item[
                                                                'title status'] if 'title status' in item.keys() else '' +
                                                                                                                      item[
                                                                                                                          'condition'] if 'condition' in item.keys() else '' +
                                                                                                                                                                          item[
                                                                                                                                                                              'area'] if 'area' in item.keys() else '' +
                                                                                                                                                                                                                    item[
                                                                                                                                                                                                                        'paint color'] if 'paint color' in item.keys() else '').lower()
        if item_date >= date_from and item['id'] not in EXCEPTIONS \
                and item['id'] not in ids and pnott not in pnotts \
                and 3000 <= item['price'] <= 8000 \
                and ('toyota' in cs or 'mazda' in cs or 'nissan' in cs or 'ford' in cs
                     or 'honda' in cs or 'hyundai' in cs or 'mitsubishi' in cs or 'kia' in cs) \
                and ('odometer' in item.keys() and int(item['odometer']) <= 100000) \
                and ('area' in item.keys() and item['area'] == 'austin') \
                and ('year' in item.keys() and item['year'] is not None and int(item['year']) >= 2017) \
                and ('transmission' in item.keys() and item['transmission'] == 'automatic') \
                and ('title status' in item.keys() and item['title status'] == 'clean'):
            result.append(item)
            ids.append(item['id'])
            pnotts.append(pnott)
        if item_date >= date_from and item['id'] not in EXCEPTIONS \
                and item['id'] not in ids and pnott not in pnotts \
                and 8001 <= item['price'] <= 10000 \
                and ('toyota' in cs or 'mazda' in cs or 'nissan' in cs or 'ford' in cs
                     or 'honda' in cs or 'hyundai' in cs or 'mitsubishi' in cs or 'kia' in cs) \
                and ('odometer' in item.keys() and int(item['odometer']) <= 60000) \
                and ('area' in item.keys() and item['area'] == 'austin') \
                and ('year' in item.keys() and item['year'] is not None and int(item['year']) >= 2019) \
                and ('transmission' in item.keys() and item['transmission'] == 'automatic') \
                and ('title status' in item.keys() and item['title status'] == 'clean'):
            result.append(item)
            ids.append(item['id'])
            pnotts.append(pnott)
    return result


if __name__ == '__main__':
    # TODO сохранить файл c токеном odt в пароли
    print(THIS_DIR)

    settings = load_settings()
    url = settings['url'] + settings['token']
    channel_ids = settings['channel_ids_rvr']
    channel_rvr = settings['channel_ids_rvr']
    today = datetime.today().date()

    # send_telegram('test text')
    with open(f'{THIS_DIR}/Data/car_data.dat', 'rb') as filehandle:
        data = pickle.load(filehandle)
    result = data['data']
    find_model_year(result)
    find_car_model(result)
    result = filter_car_result(CAR, result)
    if not result:
        send_telegram(channel_rvr, f'{today}: no car matches. working')
    elif len(result) > 10:
        send_telegram(channel_rvr, f'{today}: too many results: {len(result)}. Check settings.')
        send_telegram(channel_rvr, f'{result[0]["link"]}')
        send_telegram(channel_rvr, f'{result[-1]["link"]}')
    else:
        send_telegram(channel_ids, f'{today}: {len(result)} cars found:')
        for item in result:
            send_telegram(channel_ids, f'{result[0]["link"]}')

    # print(result[0])
    # print(len(result))
