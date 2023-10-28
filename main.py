import aiohttp
import asyncio
from bs4 import BeautifulSoup
import unidecode
import csv
import os
from functools import partial
import pandas as pd

async def fetch_url(session, url):
    try:
        async with session.get(url) as response:
            return await response.text()
    except Exception as e:
        print(f'Error fetching URL: {url}\nError: {str(e)}')
        return None

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
    url = f'https://www.worldcubeassociation.org/persons/{i}'
    html = await fetch_url(session, url)
    soup = BeautifulSoup(html, 'html.parser')

    div = soup.find('div', {'class': 'personal-records'})
    if div is not None:
        rows = div.find_all('tr')
        with open(f'newresults{i}.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            for row in rows:
                cells = row.find_all('td')
                data = [unidecode.unidecode(cell.get_text(strip=True)) for cell in cells]
                writer.writerow(data)

        with open(f'newresults{i}.csv', 'r') as file:
            csvreader = csv.reader(file)
            header = next(csvreader)
            bufferevents = csvreader
            # print(bufferevents[1][0])
            if bufferevents:
                    try:
                        for row in bufferevents:
                            if "3x3x3 Cube" in row:
                                bufferpr3 = row[5]
                                buffersing3 = row[4]
                            if "2x2x2 Cube" in row:
                                bufferpr2 = row[5]
                                buffersing2 = row[4]
                            if "4x4x4 Cube" in row:
                                bufferpr4 = row[5]
                                buffersing4 = row[4]
                            if "5x5x5 Cube" in row:
                                bufferpr5 = row[5]
                                buffersing5 = row[4]
                            if "6x6x6 Cube" in row:
                                bufferpr6 = row[5]
                                buffersing6 = row[4]
                            if "7x7x7 Cube" in row:
                                bufferpr7 = row[5]
                                buffersing7 = row[4]
                            if "3x3x3 Blindfolded" in row:
                                bufferpr3bld = row[5]
                                buffersing3bld = row[4]
                            if "3x3x3 Fewest Moves" in row:
                                bufferprfmc = row[5]
                                buffersingfmc = row[4]
                            if "3x3x3 One-Handed" in row:
                                bufferproh = row[5]
                                buffersingoh = row[4]
                            if "Clock" in row:
                                bufferprclock = row[5]
                                buffersingclock = row[4]
                            if "Megaminx" in row:
                                bufferprmega = row[5]
                                buffersingmega = row[4]
                            if "Pyraminx" in row:
                                bufferprpyra = row[5]
                                buffersingpyra = row[4]
                            if "Skewb" in row:
                                bufferprskewb = row[5]
                                buffersingskewb = row[4]
                            if "Square-1" in row:
                                bufferprsq1 = row[5]
                                buffersingsq1 = row[4]
                            if "4x4x4 Blindfolded" in row:
                                bufferpr4bld = row[5]
                                buffersing4bld = row[4]
                            if "5x5x5 Blindfolded" in row:
                                bufferpr5bld = row[5]
                                buffersing5bld = row[4]
                            if "3x3x3 Multi-Blind" in row:
                                bufferprmbld = row[4]
                                buffersingmbld = row[4]
                    except:
                        print(f"error extracting data for {i}")

    div = soup.find('div', {'class': 'text-center'})
    if div is not None:
        rows = div.find_all('img', {'class': 'avatar'})
        for row in rows:
            link = row['src']
            photo = link

    url = f'https://www.worldcubeassociation.org/search?q={i}'
    html = await fetch_url(session, url)
    if html is not None:
        soup = BeautifulSoup(html, 'html.parser')
        divtable = soup.find('table', {'class': 'table table-nonfluid table-vertical-align-middle'})
        if divtable is not None:
            rows = divtable.find_all('tr')
            with open(f'name{i}.csv', mode='w', newline='') as file:
                writer = csv.writer(file)
                for row in rows:
                    cells = row.find_all('td')
                    data = [unidecode.unidecode(cell.get_text(strip=True)) for cell in cells]
                    writer.writerow(data)

            with open(f'name{i}.csv', 'r') as file:
                csvreader = csv.reader(file)
                for row in csvreader:
                    namesv.append([i, row[2]])

    photos_dict[i] = photo  # Store the photo link in the dictionary

    return i, bufferpr3, namesv, buffersing3, bufferpr2, buffersing2, bufferpr4, buffersing4, bufferpr5, buffersing5, bufferpr6, buffersing6, bufferpr7, buffersing7, bufferpr3bld, buffersing3bld, bufferprfmc, buffersingfmc, bufferproh, buffersingoh, bufferprclock, buffersingclock, bufferprmega, buffersingmega, bufferprpyra, buffersingpyra, bufferprskewb, buffersingskewb, bufferprsq1, buffersingsq1, bufferpr4bld, buffersing4bld, bufferpr5bld, buffersing5bld, bufferprmbld, buffersingmbld

async def main():
    wcaidv = []
    providv = []
    namesv = [['wcaid', 'name']]
    photos_dict = {}

    with open('provinceID.csv', 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            if "\t" in row[0]:
                row[0] = row[0].replace("\t", "")
            wcaidv.append(row[0])
            providv.append(row[1])

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
    sorted_RESULTS = sorted(results, key=lambda x: float(x[1]) if x[1].replace('.', '', 1).isdigit() else float('inf'))

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

    with open(f'final_wcaid_names.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        for row in namesv:
            writer.writerow(row)

    with open(f'final_sorted_RESULTS.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        for row in final_sorted_RESULTS:
            writer.writerow(row)

    df1 = pd.read_csv('final_sorted_RESULTS.csv')
    df2 = pd.read_csv('final_wcaid_names.csv')
    merged_df = pd.merge(df1, df2, on='wcaid', how='left')
    merged_df.to_csv('FINAL.csv', index=False)

    # Converting to HTML
    df = pd.read_csv('FINAL.csv')
    html_table = df.to_html(
        classes='table table-bordered table-hover',
        index=False,
        escape=False
    )
    html_table = html_table.replace('[', '').replace(']', '')

    with open('final_sorted_RESULTS.html', 'w') as f:
        f.write(html_table)

if __name__ == '__main__':
    asyncio.run(main())
