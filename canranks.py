import aiohttp
import asyncio
from bs4 import BeautifulSoup
import unidecode
import csv
import os
from functools import partial
import pandas as pd
import requests

MAX_RETRY = 5 # maximum number of retries for each request

async def fetch_url(session, url):
    retry_count = 0
    while retry_count < MAX_RETRY:
        try:
            async with session.get(url) as response:
                return await response.text()
        except Exception as e:
            if isinstance(e, ConnectionAbortedError): # catch WinError 10053
                print(f'Error: ConnectionAbortedError (WinError 10053) for URL: {url}. Retry #{retry_count}')
                retry_count += 1
                continue
            print(f'Error fetching URL: {url}\nError: {str(e)}')
            return None
    return None # after MAX_RETRY attempts


async def scrape_wca(i, session, wcaidv, namesv, photos_dict, **kwargs):
    total_tasks = kwargs['total_tasks']
    completed_tasks = kwargs['completed_tasks']
    # Initialize variables with default values
    bufferpr3 = "NaN"
    buffersing3 = "NaN"
    bufferpr2 = "NaN"
    buffersing2 = "NaN"
    bufferpr4 = "NaN"
    buffersing4 = "NaN"
    bufferpr5 = "NaN"
    buffersing5 = "NaN"
    bufferpr6 = "NaN"
    buffersing6 = "NaN"
    bufferpr7 = "NaN"
    buffersing7 = "NaN"
    bufferpr3bld = "NaN"
    buffersing3bld = "NaN"
    bufferprfmc = "NaN"
    buffersingfmc = "NaN"
    bufferproh = "NaN"
    buffersingoh = "NaN"
    bufferprclock = "NaN"
    buffersingclock = "NaN"
    bufferprmega = "NaN"
    buffersingmega = "NaN"
    bufferprpyra = "NaN"
    buffersingpyra = "NaN"
    bufferprskewb = "NaN"
    buffersingskewb = "NaN"
    bufferprsq1 = "NaN"
    buffersingsq1 = "NaN"
    bufferpr4bld = "NaN"
    buffersing4bld = "NaN"
    bufferpr5bld = "NaN"
    buffersing5bld = "NaN"
    bufferprmbld = "NaN"
    buffersingmbld = "NaN"
    buffernames = []
    photo = ""


    icap = "".join([x.upper() for x in i])

    try:
        response = requests.get(
            f"https://raw.githubusercontent.com/robiningelbrecht/wca-rest-api/master/api/persons/{icap}.json")
        data = response.json()
        name = data.get('name')
        namesv.append([i, name])
        print(f'Name: {name}')
        singles = data['rank']['singles']
        averages = data['rank']['averages']

        def format_time(time_in_seconds):
            if isinstance(time_in_seconds, (int, float)):
                if time_in_seconds < 60:
                    # Format times under 60 seconds as x.xx or xx.xx
                    return '{:.2f}'.format(time_in_seconds)
                else:
                    minutes, seconds = divmod(time_in_seconds, 60)
                    centiseconds = int((seconds - int(seconds)) * 100)  # Convert centiseconds to an integer
                    centiseconds_str = f'{centiseconds:02d}'  # Ensure two decimal places for centiseconds
                    return '{:02d}:{:02d}.{}'.format(int(minutes), int(seconds), centiseconds_str)
            else:
                # Return a placeholder value for non-numeric input
                return 'NaN'

        for single in singles:
            event_id = single.get('eventId')
            result = single['best'] / 100 if event_id != '333mbf' else single['best']
            if result == result and event_id != '333mbf':
                result = format_time(result)
            if event_id == '333':
                buffersing3 = result
            if event_id == '222':
                buffersing2 = result
            if event_id == '444':
                buffersing4 = result
            if event_id == '555':
                buffersing5 = result
            if event_id == '666':
                buffersing6 = result
            if event_id == '777':
                buffersing7 = result
            if event_id == '333bf':
                buffersing3bld = result
            if event_id == '333fm':
                buffersingfmc = single['best']
            if event_id == '333oh':
                buffersingoh = result
            if event_id == 'clock':
                buffersingclock = result
            if event_id == 'minx':
                buffersingmega = result
            if event_id == 'pyram':
                buffersingpyra = result
            if event_id == 'skewb':
                buffersingskewb = result
            if event_id == 'sq1':
                buffersingsq1 = result
            if event_id == '444bf':
                buffersing4bld = result
            if event_id == '555bf':
                buffersing5bld = result
            if event_id == '333mbf':
                buffersingmbld = single['best']

        for average in averages:
            event_id = average.get('eventId')
            result = average['best'] / 100 if event_id != '333mbf' else average['best']
            if result == result and event_id != '333mbf':
                result = format_time(result)
            if event_id == '333':
                bufferpr3 = result
            if event_id == '222':
                bufferpr2 = result
            if event_id == '444':
                bufferpr4 = result
            if event_id == '555':
                bufferpr5 = result
            if event_id == '666':
                bufferpr6 = result
            if event_id == '777':
                bufferpr7 = result
            if event_id == '333bf':
                bufferpr3bld = result
            if event_id == '333fm':
                bufferprfmc = result
            if event_id == '333oh':
                bufferproh = result
            if event_id == 'clock':
                bufferprclock = result
            if event_id == 'minx':
                bufferprmega = result
            if event_id == 'pyram':
                bufferprpyra = result
            if event_id == 'skewb':
                bufferprskewb = result
            if event_id == 'sq1':
                bufferprsq1 = result
            if event_id == '444bf':
                bufferpr4bld = result
            if event_id == '555bf':
                bufferpr5bld = result
            if event_id == '333mbf':
                bufferprmbld = average['best']



    except:
        print(f"Error getting results for {icap}")



    url = f'https://www.worldcubeassociation.org/persons/{i}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    div = soup.find('div', {'class': 'text-center'})
    if div is not None:
        rows = div.find_all('img', {'class': 'avatar'})
        for row in rows:
            photos_dict[i] = row['src']


    # photos_dict[i] = 'https://www.worldcubeassociation.org/assets/missing_avatar_thumb-d77f478a307a91a9d4a083ad197012a391d5410f6dd26cb0b0e3118a5de71438.png'  # Store the photo link in the dictionary'

    return i, bufferpr3, namesv, buffersing3, bufferpr2, buffersing2, bufferpr4, buffersing4, bufferpr5, buffersing5, bufferpr6, buffersing6, bufferpr7, buffersing7, bufferpr3bld, buffersing3bld, bufferprfmc, buffersingfmc, bufferproh, buffersingoh, bufferprclock, buffersingclock, bufferprmega, buffersingmega, bufferprpyra, buffersingpyra, bufferprskewb, buffersingskewb, bufferprsq1, buffersingsq1, bufferpr4bld, buffersing4bld, bufferpr5bld, buffersing5bld, bufferprmbld, buffersingmbld

async def main():
    wcaidv = []
    providv = []
    namesv = [['wcaid', 'name']]
    photos_dict = {}

    df = pd.read_csv('provinceID.csv', delimiter=',')

    # List DataFrame column names
    print(df.columns)

    # Remove whitespaces from column names if necessary
    df.columns = df.columns.str.strip()

    # Convert to lower case
    df.columns = df.columns.str.lower()

    df.drop_duplicates(subset='wcaid', keep='first', inplace=True)
    wcaidv = df['wcaid'].to_list()
    providv = df['provid'].to_list()

    results = [['wcaid', '0', 'name', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']]
    idlength = len(wcaidv)

    async with aiohttp.ClientSession() as session:
        partial_scrape = partial(scrape_wca, total_tasks=idlength, completed_tasks=0, wcaidv=wcaidv, namesv=namesv, photos_dict=photos_dict)
        tasks = [partial_scrape(wcaid, session) for wcaid in wcaidv]

        completed_tasks = 0
        for task in asyncio.as_completed(tasks):
            try:
                wcaid, bufferpr3, namesv, buffersing3, bufferpr2, buffersing2, bufferpr4, buffersing4, bufferpr5, buffersing5, bufferpr6, buffersing6, bufferpr7, buffersing7, bufferpr3bld, buffersing3bld, bufferprfmc, buffersingfmc, bufferproh, buffersingoh, bufferprclock, buffersingclock, bufferprmega, buffersingmega, bufferprpyra, buffersingpyra, bufferprskewb, buffersingskewb, bufferprsq1, buffersingsq1, bufferpr4bld, buffersing4bld, bufferpr5bld, buffersing5bld, bufferprmbld, buffersingmbld = await task
                results.append([wcaid, bufferpr3, namesv, buffersing3, bufferpr2, buffersing2, bufferpr4, buffersing4, bufferpr5, buffersing5, bufferpr6, buffersing6, bufferpr7, buffersing7, bufferpr3bld, buffersing3bld, bufferprfmc, buffersingfmc, bufferproh, buffersingoh, bufferprclock, buffersingclock, bufferprmega, buffersingmega, bufferprpyra, buffersingpyra, bufferprskewb, buffersingskewb, bufferprsq1, buffersingsq1, bufferpr4bld, buffersing4bld, bufferpr5bld, buffersing5bld, bufferprmbld, buffersingmbld])
                completed_tasks += 1
                completion_percentage = (completed_tasks / idlength) * 100
                print(f"Completed: {completed_tasks}/{idlength} ({completion_percentage:.2f}%)")
            except Exception as e:
                print(f'An error occurred while processing WCA ID {wcaid}: {str(e)}')

    for wcaid in wcaidv:
        # file_path = f'newresults{wcaid}.csv'
        # if os.path.exists(file_path):
        #     os.remove(file_path)
        file_path = f'name{wcaid}.csv'
        if os.path.exists(file_path):
            os.remove(file_path)

    # Sorting and saving to CSV
    sorted_RESULTS = sorted(results, key=lambda x: (float(x[1]) if isinstance(x[1], str) and x[1].replace('.', '', 1).isdigit() else float('inf')))

    final_sorted_RESULTS = []

    for row in sorted_RESULTS:
        wcaid = row[0]
        bufferpr3 = row[1]
        buffernames = row[2]
        buffersing3 = row[3]
        bufferpr2 = row[4]
        buffersing2 = row[5]
        bufferpr4 = row[6]
        buffersing4 = row[7]
        bufferpr5 = row[8]
        buffersing5 = row[9]
        bufferpr6 = row[10]
        buffersing6 = row[11]
        bufferpr7 = row[12]
        buffersing7 = row[13]
        bufferpr3bld = row[14]
        buffersing3bld = row[15]
        bufferprfmc = row[16]
        buffersingfmc = row[17]
        bufferproh = row[18]
        buffersingoh = row[19]
        bufferprclock = row[20]
        buffersingclock = row[21]
        bufferprmega = row[22]
        buffersingmega = row[23]
        bufferprpyra = row[24]
        buffersingpyra = row[25]
        bufferprskewb = row[26]
        buffersingskewb = row[27]
        bufferprsq1 = row[28]
        buffersingsq1 = row[29]
        bufferpr4bld = row[30]
        buffersing4bld = row[31]
        bufferpr5bld = row[32]
        buffersing5bld = row[33]
        bufferprmbld = row[34]
        buffersingmbld = row[35]
        photo = photos_dict.get(wcaid, "")  # Get the photo link for this WCA ID

        if wcaid in wcaidv:
            province_id = providv[wcaidv.index(wcaid)]
        else:
            province_id = "N/A"

        final_sorted_RESULTS.append([wcaid, bufferpr3, province_id, buffersing3, photo, bufferpr2, buffersing2, bufferpr4, buffersing4, bufferpr5, buffersing5, bufferpr6, buffersing6, bufferpr7, buffersing7, bufferpr3bld, buffersing3bld, bufferprfmc, buffersingfmc, bufferproh, buffersingoh, bufferprclock, buffersingclock, bufferprmega, buffersingmega, bufferprpyra, buffersingpyra, bufferprskewb, buffersingskewb, bufferprsq1, buffersingsq1, bufferpr4bld, buffersing4bld, bufferpr5bld, buffersing5bld, bufferprmbld, buffersingmbld])

    with open(f'final_wcaid_names.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for row in namesv:
            writer.writerow(row)

    with open(f'final_sorted_RESULTS.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for row in final_sorted_RESULTS:
            writer.writerow(row)

    df1 = pd.read_csv('final_sorted_RESULTS.csv')
    df2 = pd.read_csv('final_wcaid_names.csv')
    merged_df = pd.merge(df1, df2, on='wcaid', how='left')
    merged_df.to_csv('FINAL.csv', index=False, encoding='utf-8')

    # Converting to HTML
    df = pd.read_csv('FINAL.csv')
    html_table = df.to_html(classes='table table-bordered table-hover', index=False, escape=False)
    html_table = html_table.replace('[', '').replace(']', '')

    with open('final_sorted_RESULTS.html', 'w', encoding='utf-8') as f:
        f.write(html_table)

if __name__ == '__main__':
    asyncio.run(main())
