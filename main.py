from Scraper import Scraper
from tabulate import tabulate
import pandas as pd
from datetime import datetime, timedelta
import pickle
import openpyxl

DATA_DIR = 'Data'
REPORTS_DIR = 'Reports'


def writeExcel(filename, result):
    df1 = pd.DataFrame.from_dict(result)
    with pd.ExcelWriter(f'{REPORTS_DIR}\{filename}.xlsx') as writer:
        df1.to_excel(writer, sheet_name='x1')


def saveData(filename, data):
    data = {
        'data_time': datetime.now(),
        'data': data
    }
    with open(f'{DATA_DIR}\{filename}.dat', 'wb') as filehandle:
        pickle.dump(data, filehandle)


def loadData(filename):
    try:
        with open(f'{DATA_DIR}\{filename}.dat', 'rb') as filehandle:
            data = pickle.load(filehandle)
    except:
        return None, None
    return data['data_time'], data['data']


def filter_cpu_result(arg, raw_result):
    EXCEPTIONS = ['7334739070', '7336458858', '7335074640', '7332223384', '7335767507', '7335481330', '7335481271',
                  '7322295229', '7324437075', '7336595666', '7327643157', '7330286131', '7330808578', '7337716315',
                  '7337279290']
    date_from = datetime.strptime('2021-06-12', '%Y-%m-%d').date()
    result = []
    ids = []
    for item in raw_result:
        item_date = datetime.strptime(item['datetime'], '%Y-%m-%d').date()
        cs = (item['name'] + item['info']).lower()
        if item_date >= date_from and item['id'] not in EXCEPTIONS and arg['min_price'] <= item['price'] <= arg['max_price'] and \
                ('ram' in cs or 'intel' in cs or 'gig' in cs or 'windows' in cs or 'linux' in cs or 'core' in cs or 'amd' in cs) and (
                item['price'] <= 50 or ('4gig' not in cs and '4 gig' not in cs
                                        and '4gb' not in cs and '4 gb' not in cs)) and \
                item['id'] not in ids:
            result.append(item)
            ids.append(item['id'])
    return result


def filter_car_result(arg, raw_result):
    EXCEPTIONS = []
    date_from = datetime.strptime('2021-03-01', '%Y-%m-%d').date()
    result = []
    ids = []
    for item in raw_result:
        item_date = datetime.strptime(item['datetime'], '%Y-%m-%d').date()
        cs = (item['name'] + item['info']).lower()
        if item_date >= date_from and item['id'] not in EXCEPTIONS and item['id'] not in ids \
                and arg['min_price'] <= item['price'] <= arg['max_price']:
            result.append(item)
            ids.append(item['id'])
    return result


def get_raw(args):
    datatime, result = loadData(args['output_file'])
    if not datatime or datetime.now() - datatime > timedelta(hours=12):
        scraper = Scraper(**args)
        result = scraper.scrap
        result.sort(key=lambda x: x['price'])
        saveData(args['output_file'], result)
        datatime, result = loadData(args['output_file'])
    return result


if __name__ == '__main__':
    CPU = {
        'LINKS': [
            'https://sanmarcos.craigslist.org/d/for-sale/search/sss?query=computers&sort=rel',
            'https://austin.craigslist.org/search/sya?',
            'https://austin.craigslist.org/d/computers/search/sya?s=120',
            'https://austin.craigslist.org/d/computers/search/sya?s=240',
            'https://austin.craigslist.org/d/computers/search/sya?s=360',
            'https://austin.craigslist.org/d/computers/search/sya?s=480',
            'https://austin.craigslist.org/d/computers/search/sya?s=600',
            'https://austin.craigslist.org/d/computers/search/sya?s=720',
            'https://austin.craigslist.org/d/computers/search/sya?s=840',

            'https://sanantonio.craigslist.org/d/computers/search/sya',
            'https://sanantonio.craigslist.org/d/computers/search/sya?s=120',
            'https://sanantonio.craigslist.org/d/computers/search/sya?s=240',
            'https://sanantonio.craigslist.org/d/computers/search/sya?s=360'
        ],
        'min_price': 0,
        'max_price': 150,
        'type': 'cpu',
        'output_file': 'cpu_data',
        'scrap_time': None
    }
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
        'min_price': 2500,
        'max_price': 12000,
        'type': 'car',
        'output_file': 'car_data',
        'scrap_time': None
    }

    SEARCH = CPU
    result = get_raw(SEARCH)
    if SEARCH['type'] == 'car':
        result = filter_car_result(SEARCH, result)
    elif SEARCH['type'] == 'cpu':
        result = filter_cpu_result(SEARCH, result)

    print(tabulate(result, headers="keys", tablefmt="plain"))
    writeExcel(SEARCH['output_file'], result)

