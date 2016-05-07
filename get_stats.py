import sys
from bs4 import BeautifulSoup
import urllib.request
import csv
import time
import datetime

baseURL = 'http://finance.yahoo.com'
stat_order = [
    "Name",
    "Ticker",
    "Bid",
    "Ask",
    "Prev Close",
    "Open",
    "Volume",
    "Avg Vol (3 month)",
    "Avg Vol (10 day)",
    "Forward Annual Dividend Rate",
    "Forward Annual Dividend Yield",
    "Trailing Annual Dividend Yield",
    "5 Year Average Dividend Yield",
    "Payout Ratio",
    "Dividend Date",
    "Ex-Dividend Date",
    "Beta",
    "52-Week Change",
    "S&P500 52-Week Change",
    "52-Week High",
    "52-Week Low",
    "50-Day Moving Average",
    "200-Day Moving Average",
    "Shares Outstanding",
    "Float",
    "% Held by Insiders",
    "% Held by Institutions",
    "Shares Short",
    "Short Ratio",
    "Short % of Float",
    "Market Cap",
    "Enterprise Value",
    "Trailing P/E",
    "Forward P/E",
    "PEG Ratio",
    "Price/Sales",
    "Price/Book",
    "Enterprise Value/Revenue",
    "Enterprise Value/EBITDA",
    "Fiscal Year Ends",
    "Most Recent Quarter",
    "Profit Margin",
    "Operating Margin",
    "Return on Assets",
    "Return on Equity",
    "Revenue",
    "Revenue Per Share",
    "Qtrly Revenue Growth",
    "Gross Profit",
    "EBITDA",
    "Net Income Avl to Common",
    "Diluted EPS",
    "Qtrly Earnings Growth",
    "Total Cash",
    "Total Cash Per Share",
    "Total Debt",
    "Total Debt/Equity",
    "Current Ratio",
    "Book Value Per Share",
    "Operating Cash Flow",
    "Levered Free Cash Flow",
    "Last Split Factor",
    "Last Split Date",
    "Earnings Date"
]

stats_to_format = [
    "Shares Outstanding",
    "Float",
    "Shares Short",
    "Market Cap",
    "Enterprise Value",
    "Revenue",
    "EBITDA",
    "Net Income Avl to Common",
    "Total Cash",
    "Total Debt",
    "Operating Cash Flow",
    "Levered Free Cash Flow"
]

def main():
    now = datetime.datetime.now()
    output_file_name = str(now.year) + '-' + str(now.month) + '-' + str(now.day) + '-' + str(now.hour) + 'h' + str(now.minute) + 'm' + str(now.second) + 's'
    tickers = process_input(sys.argv)

    stock_info = []

    for ndx, ticker in enumerate(tickers):
        sys.stdout.write('(' + str(ndx + 1) + '/' + str(len(tickers)) + ')\r')
        stock_info.append(scrape_all_info(ticker))
    
    write_output(stock_info, output_file_name)

def process_input(argv):
    if len(argv) != 2:
        print("USAGE: python get_stats.py input_file")
        print("Input file should be line seperated stock tickers on the TSX")
        exit(1)
    else:
        tickers = []
        with open(argv[1], 'r') as fp:
            for line in fp:
                ticker = line.strip().upper().replace('.', '-')
                ticker += '.TO'
                tickers.append(ticker)
    return set(tickers)

def scrape_all_info(ticker):
    ticker_url = baseURL + '/q?s=' + ticker

    with urllib.request.urlopen(ticker_url) as response:
        finance_page = response.read()

    soup = BeautifulSoup(finance_page)
    keystats_link = soup.find(id='yfi_key_stats').find('a')

    stock_info = scrape_basic_info(soup)

    if keystats_link and keystats_link.has_attr('href'):
        stock_info.update(scrape_more_stats(keystats_link['href']))

    return stock_info

def scrape_basic_info(basic_page):
    title = basic_page.find(id='yfi_rt_quote_summary').find('h2').get_text()
    name = title.split('(')[0].strip()
    ticker = title.split('(')[1].strip().rstrip(')')
    
    stats = {'Name': name, 'Ticker': ticker}

    for row in basic_page.find(id='yfi_quote_summary_data').find_all('tr'):
        label = row.th.get_text().strip().strip(':')
        value = row.td.get_text().strip()

        if label in ('Prev Close', 'Open', 'Bid', 'Ask', 'Earnings Date', 'Volume'):
            stats[label] = value
        elif label == "Day's Range:":
            values = [x.strip() for x in value.split('-')]
            stats[label + ' Min'] = values[0]
            stats[label + ' Max'] = values[1]

    return stats

def scrape_more_stats(link):
    more_stats_url = baseURL + link

    with urllib.request.urlopen(more_stats_url) as response:
        more_stats_page = response.read()

    soup = BeautifulSoup(more_stats_page)

    tables = soup.find(class_='yfnc_modtitlew1').find_all('tr')
    tables += soup.find(class_='yfnc_modtitlew2').find_all('tr')

    stats = {}

    for row in tables:
        cells = row.find_all('td')
        if len(cells) == 2:
            full_label = cells[0].get_text()
            value = cells[1].get_text()

            if 'Avg Vol' in full_label:
                label = full_label.strip(': ')
            else:
                label = full_label.split('(')[0].strip(': ')
            
            try: 
                int(label[-1])
                label = label[:-1]
            except:
                pass

            if label in stats_to_format:
                value = format_ending(value)

            stats[label] = value

    return stats

def format_ending(value):
    if value =='N/A':
        return 'N/A'

    ending = value[-1]
    number = float(value[:-1])

    if ending == 'K':
        number *= 1000
    elif ending == 'M':
        number *= 1000000
    elif ending == 'B':
        number *= 1000000000
    elif ending == 'T':
        number *= 1000000000000

    return number


def write_output(stock_info, filename):
    with open('output/' + filename + '.csv', 'a', newline='') as csvfile:
        row_writer = csv.writer(csvfile)
        
        row_writer.writerow([filename])
        row_writer.writerow(stat_order)

        for info_dict in stock_info:
            row = []
            for column in stat_order:
                try:
                    row.append(info_dict[column])
                except:
                    row.append('N/A')

            row_writer.writerow(row)

if __name__ == '__main__':
    main()