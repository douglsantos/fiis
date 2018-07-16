import pandas
import requests

from bs4 import BeautifulSoup


MAIN_URL = 'http://www.fundsexplorer.com.br/funds'


def get_funds():
    resp = requests.get(MAIN_URL)
    soup = BeautifulSoup(resp.content)
    table = soup.findAll('table')[0]
    links = table.findAll('a')
    funds = []
    for i in range(0, len(links), 2):
        funds.append(links[i].contents[0])

    return funds


def get_specific_fund(fund_name):
    def format_val(val):
        try:
            return float(val)
        except ValueError:
            return val

    resp = requests.get(MAIN_URL + '/' + fund_name)
    soup = BeautifulSoup(resp.content)
    values = [val.contents[0].strip().replace(',', '.') for val in
              soup.findAll('div', {'class': 'count'})
              ]
    values = dict(
        fund=fund_name,
        price=format_val(values[0]),
        share=format_val(values[2]),
        interest=format_val(values[3]),
        percent=format_val(values[5].replace('%', ''))
    )
    return values


if __name__ == '__main__':
    funds = get_funds()
    results = []
    for fund in funds:
        results.append(get_specific_fund(fund))

    data_frame = pandas.DataFrame(results)
    data_frame.set_index('fund', inplace=True)

    # funds that worth it
    for fund_name, values in data_frame.iterrows():
        try:
            percent = values.share / values.price
            if percent > 0.008:
                print(fund_name, ' - ', percent * 100)
        except:
            continue
