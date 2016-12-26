import sys
from yahoo_finance import Share
import csv
import time
import datetime

stat_order = [
    "Name",
    "price",
    "change",
    "percent_change",
    "volume",
    "prev_close",
    "open",
    "avg_daily_volume",
    "stock_exchange",
    "market_cap",
    "book_value",
    "ebitda",
    "dividend_share",
    "dividend_yield",
    "earnings_share",
    "days_high",
    "days_low",
    "year_high",
    "year_low",
    "50day_moving_avg",
    "200day_moving_avg",
    "price_earnings_ratio",
    "price_earnings_growth_ratio",
    "price_sales",
    "price_book",
    "short_ratio",
    "trade_datetime",
    "percent_change_from_year_high",
    "percent_change_from_year_low",
    "change_from_year_low",
    "change_from_year_high",
    "percent_change_from_200_day_moving_average",
    "change_from_200_day_moving_average",
    "percent_change_from_50_day_moving_average",
    "change_from_50_day_moving_average",
    "EPS_estimate_next_quarter",
    "EPS_estimate_next_year",
    "ex_dividend_date",
    "EPS_estimate_current_year",
    "price_EPS_estimate_next_year",
    "price_EPS_estimate_current_year",
    "one_yr_targetprice",
    "change_percent_change",
    "dividend_pay_date",
    "currency",
    "last_trade_with_time",
    "days_range",
    "year_range",
]

def main():
    now = datetime.datetime.now()
    output_file_name = str(now.year) + '-' + str(now.month) + '-' + str(now.day) + '-' + str(now.hour) + 'h' + str(now.minute) + 'm' + str(now.second) + 's'
    tickers = process_input(sys.argv)

    stock_info = []

    for ndx, ticker in enumerate(tickers):
        sys.stdout.write('(' + str(ndx + 1) + '/' + str(len(tickers)) + ')\r')
        stock_info.append(Share(ticker))
    
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

def write_output(stock_info, filename):
    with open('output/' + filename + '.csv', 'a', newline='') as csvfile:
        row_writer = csv.writer(csvfile)
        
        row_writer.writerow([filename])
        row_writer.writerow(stat_order)

        for stock in stock_info:
            row = []       

            row.append(stock.get_name())
            row.append(stock.get_price())
            row.append(stock.get_change())
            row.append(stock.get_percent_change())
            row.append(stock.get_volume())
            row.append(stock.get_prev_close())
            row.append(stock.get_open())
            row.append(stock.get_avg_daily_volume())
            row.append(stock.get_stock_exchange())
            row.append(stock.get_market_cap())
            row.append(stock.get_book_value())
            row.append(stock.get_ebitda())
            row.append(stock.get_dividend_share())
            row.append(stock.get_dividend_yield())
            row.append(stock.get_earnings_share())
            row.append(stock.get_days_high())
            row.append(stock.get_days_low())
            row.append(stock.get_year_high())
            row.append(stock.get_year_low())
            row.append(stock.get_50day_moving_avg())
            row.append(stock.get_200day_moving_avg())
            row.append(stock.get_price_earnings_ratio())
            row.append(stock.get_price_earnings_growth_ratio())
            row.append(stock.get_price_sales())
            row.append(stock.get_price_book())
            row.append(stock.get_short_ratio())
            row.append(stock.get_trade_datetime())
            row.append(stock.get_percent_change_from_year_high())
            row.append(stock.get_percent_change_from_year_low())
            row.append(stock.get_change_from_year_low())
            row.append(stock.get_change_from_year_high())
            row.append(stock.get_percent_change_from_200_day_moving_average())
            row.append(stock.get_change_from_200_day_moving_average())
            row.append(stock.get_percent_change_from_50_day_moving_average())
            row.append(stock.get_change_from_50_day_moving_average())
            row.append(stock.get_EPS_estimate_next_quarter())
            row.append(stock.get_EPS_estimate_next_year())
            row.append(stock.get_ex_dividend_date())
            row.append(stock.get_EPS_estimate_current_year())
            row.append(stock.get_price_EPS_estimate_next_year())
            row.append(stock.get_price_EPS_estimate_current_year())
            row.append(stock.get_one_yr_target_price())
            row.append(stock.get_change_percent_change())
            row.append(stock.get_dividend_pay_date())
            row.append(stock.get_currency())
            row.append(stock.get_last_trade_with_time())
            row.append(stock.get_days_range())
            row.append(stock.get_year_range())

            row_writer.writerow(row)

if __name__ == '__main__':
    main()