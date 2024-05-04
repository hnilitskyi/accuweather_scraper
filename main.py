from bs4 import BeautifulSoup
import requests
from xlwt import XFStyle, Alignment
import xlwt

year_start = 1937
year_stop = 2024
hurricanes_list = []
sustained = 'Peak Sustained Winds'
gusts = 'Peak Wind Gusts'
rowcount = 0

headers_browser = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

workbook = xlwt.Workbook()
sheet = workbook.add_sheet('Hurricanes')

column_widths = [1600, 2800, 1800, 1200, 2600, 2200, 2600, 2200, 2400, 2400]
for i, width in enumerate(column_widths):
    sheet.col(i).width = width

style = XFStyle()
style.alignment.horz = Alignment.HORZ_CENTER
style.alignment.vert = Alignment.VERT_CENTER

headers = ['Ordinal', 'Storm Name', 'Status', 'Year', 'Start Date', 'Start Time', 'Stop Date', 'Stop Time',
           'Peak\nSustained\nWinds km/h', 'Peak\nWind\nGusts km/h']
for col, header in enumerate(headers):
    sheet.write(0, col, header, style=style)

while year_stop >= year_start:
    storm_link = f'https://www.accuweather.com/en/hurricane'
    hurricane_history = storm_link + f'/history/?year={year_stop}'

    response = requests.get(hurricane_history, headers=headers_browser)

    if response.status_code == 200:

        response_data = requests.get(hurricane_history, headers=headers_browser).text
        soup = BeautifulSoup(response_data, 'lxml')
        hurricanes = soup.findAll(class_='storm-row')

        for hurricane in hurricanes:
            hurricane_link = hurricane['href']
            hurricanes_list.append('https://www.accuweather.com' + hurricane_link)

        for i, storm in enumerate(hurricanes_list):
            response_current = requests.get(storm, headers=headers_browser).text
            soup_current = BeautifulSoup(response_current, 'lxml')
            storm_name = soup_current.find(class_='storm-overview__title').text.strip()
            storm_status = soup_current.find(class_='storm-overview__status').text
            storm_start_date = soup_current.find(class_='storm-overview__local-impacts-start').find(
                class_='impacts-date').text[-5:].replace(',', '').replace('/', '.').strip()
            storm_start_time = soup_current.find(class_='storm-overview__local-impacts-start').find(
                class_='impacts-time').text.strip()
            storm_stop_date = soup_current.find(class_='storm-overview__local-impacts-end').find(
                class_='impacts-date').text[-5:].replace(',', '').replace('/', '.').strip()
            storm_stop_time = soup_current.find(class_='storm-overview__local-impacts-end').find(
                class_='impacts-time').text.strip()
            storm_wind = soup_current.find(class_='impacts-table')
            wind_items = storm_wind.find(class_='impacts-table__content').find_all('span')
            wind_sustained = None
            wind_gusts = None

            for item in wind_items:

                if item.text == sustained:
                    wind_sustained = int(item.find_next('span').text.replace('km/h', '').strip())

                if item.text == gusts:
                    wind_gusts = int(item.find_next('span').text.replace('km/h', '').strip())
            rowcount += 1
            row = rowcount
            sheet.write(row, 0, row, style=style)
            sheet.write(row, 1, storm_name.upper())
            sheet.write(row, 2, storm_status, style=style)
            sheet.write(row, 3, year_stop, style=style)
            sheet.write(row, 4, storm_start_date+'.'+str(year_stop), style=style)
            sheet.write(row, 5, storm_start_time, style=style)
            sheet.write(row, 6, storm_stop_date+'.'+str(year_stop), style=style)
            sheet.write(row, 7, storm_stop_time, style=style)
            sheet.write(row, 8, wind_sustained, style=style)
            sheet.write(row, 9, wind_gusts, style=style)
            workbook.save('hurricanes_data.xls')

    else:

        break
    hurricanes_list = []
    year_stop -= 1
