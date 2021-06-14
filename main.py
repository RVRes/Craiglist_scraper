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


if __name__ == '__main__':
    LINKS = [
        # 'https://sanmarcos.craigslist.org/d/for-sale/search/sss?query=computers&sort=rel',
        # 'https://austin.craigslist.org/search/sss?sort=rel&query=computers',
        'https://austin.craigslist.org/d/cars-trucks/search/cta?auto_make_model=toyota%20corolla'
    ]
    min_price = 2500
    max_price = 7000

    scraper = Scraper(LINKS, min_price, max_price)
    result = scraper.scrap
    print(result)
    # print(tabulate(result, headers="keys", tablefmt="plain"))
    print(tabulate(result, headers="keys", tablefmt="plain"))
    writeExcel(result)
