from Scraper import Scraper
from tabulate import tabulate
import pandas as pd
import openpyxl


def writeExcel(result):
    # df1 = pd.DataFrame(result)

    df1 = pd.DataFrame.from_dict(result)
    # print(result[0])
    # df1.columns = result[0].keys()

    with pd.ExcelWriter('out.xlsx') as writer:
        df1.to_excel(writer, sheet_name='x1')


def filter_result(raw_result):
    result = []
    ids =[]
    for item in raw_result:
        cs = (item['name'] + item['info']).lower()
        if ('ram' in cs or 'intel' in cs or 'gig' in cs or 'windows' in cs or 'linux' in cs
            or 'core' in cs or 'amd' in cs) and (item['price'] <= 50 or ('4gig' not in cs and '4 gig' not in cs
                                                 and '4gb' not in cs and '4 gb' not in cs)) and item['id'] not in ids:
            result.append(item)
            ids.append(item['id'])
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
        'max_price': 150
    }
    CAR = {
        'LINKS': [
            'https://sanmarcos.craigslist.org/d/for-sale/search/sss?query=computers&sort=rel',
            'https://austin.craigslist.org/search/sss?sort=rel&query=computers'
            # 'https://austin.craigslist.org/d/cars-trucks/search/cta?auto_make_model=toyota%20corolla'
        ],
        'min_price': 2500,
        'max_price': 7000
    }

    scraper = Scraper(**CPU)
    result = scraper.scrap
    result = filter_result(result)
    result.sort(key=lambda x: x['price'])
    print(result)
    print(tabulate(result, headers="keys", tablefmt="plain"))
    writeExcel(result)
