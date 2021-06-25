import aiohttp
import asyncio
from datetime import datetime
from bs4 import BeautifulSoup as bs


class Scraper:

    def __init__(self, **kwargs):
        self._PAGES = kwargs.get('LINKS')
        self._min_price = kwargs.get('min_price')
        self._max_price = kwargs.get('max_price')
        self._PRICE_ARGS = ('span', {'class': 'result-price'})
        self._ITEM_ARGS = ('li', {'class': 'result-row'})
        self._DATETIME_ARGS = ('time', {'class': 'result-date'})
        self._LINK_ARGS = ('a', {'class': 'result-title hdrlnk'})
        self._AREA_ARGS = ('li', {'class': 'crumb area'})

    @staticmethod
    async def fetch(session, url):
        async with session.get(url) as response:
            if response.status != 200:
                response.raise_for_status()
            return await response.text()

    @staticmethod
    async def fetch_all(session, urls):
        tasks = []
        for url in urls:
            task = asyncio.create_task(Scraper.fetch(session, url))
            tasks.append(task)
        results = await asyncio.gather(*tasks)
        return results

    @staticmethod
    async def start_session(urls):
        async with aiohttp.ClientSession() as session:
            htmls = await Scraper.fetch_all(session, urls)
            return htmls

    def _get_items(self, html: str):
        item_list = []
        soup = bs(html, 'html.parser')
        # get Area
        el_area = soup.find(*self._AREA_ARGS)
        area = el_area.find('a').get_text()
        # get items
        el_items = soup.findAll(*self._ITEM_ARGS)
        for el_item in el_items:
            item = {'area': area}
            # price
            el_price = el_item.find(*self._PRICE_ARGS)
            if not el_price:
                continue
            price = int(el_price.get_text()[1::].strip().replace(',', ''))
            # if not price or price <= self._min_price or price >= self._max_price:
            #     continue
            item['price'] = price
            # Datetime
            el_dt = el_item.find(*self._DATETIME_ARGS)
            item['datetime'] = el_dt['datetime'].split(' ')[0]
            # Good link & info
            el_good = el_item.find(*self._LINK_ARGS)
            item['id'] = el_good['data-id']
            item['name'] = el_good.get_text()
            item['link'] = el_good['href']
            item_list.append(item)
        return item_list

    def _get_sub_items(self, html: str):
        item_dict = {}
        soup = bs(html, 'html.parser')
        # id
        el_id = soup.find('div', {'class': 'postinginfos'})
        try:
            id = el_id.findChild().get_text().split(': ')[1]
        except:
            return None
        item_dict['id'] = id
        # Info
        el_info = soup.find('section', {'id': 'postingbody'})
        info = el_info.get_text().replace('QR Code Link to This Post', '').strip()
        item_dict['info'] = info
        # Attributes
        el_attr = soup.findAll('p', {'class': 'attrgroup'})
        if el_attr and len(el_attr) > 1:
            el_attr = el_attr[-1].findAll('span')
            for item in el_attr:
                at = item.get_text().split(': ')

                if at and len(at) == 2:
                    at_name, at_info = at[0], at[1]
                    item_dict[at_name] = at_info
        return item_dict


    def test_scrap(self):
        pages = asyncio.get_event_loop().run_until_complete(
            Scraper.start_session(['https://austin.craigslist.org/cto/d/seguin-smart-car-for-pure/7337517430.html']))
        soup = bs(pages[0], 'html.parser')
        # Attributes
        el_attr = soup.findAll('p', {'class': 'attrgroup'})
        if el_attr and len(el_attr) > 1:
            el_attr = el_attr[-1].findAll('span')
            for item in el_attr:
                at_name, at_info = item.get_text().split(': ')
                print(at_name, at_info)

    @property
    def scrap(self):
        # self.test_scrap()

        pages = asyncio.get_event_loop().run_until_complete(
            Scraper.start_session(self._PAGES))
        result = []
        for page in pages:
            result += self._get_items(page)
        # subpages search
        subpages = [item['link'] for item in result]
        pages = asyncio.get_event_loop().run_until_complete(
            Scraper.start_session(subpages))
        for page in pages:
            subresult = self._get_sub_items(page)
            #TODO переделать result в словарь, индекс сделать ключом, соединять по ключу.
            for item in result:
                if 'id' in item.keys() and 'id' in subresult.keys() and item['id'] == subresult['id']:
                    for k, v in subresult.items():
                        if k != 'id':
                            item[k] = v
        return result
