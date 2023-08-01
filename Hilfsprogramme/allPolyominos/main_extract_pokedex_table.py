import os
import re
import requests
from bs4 import BeautifulSoup


def extract_table_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', attrs={'class': 'pokesprite'})

    data = []
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        if cols:
            if 'dex-gen7' in url or 'dex-gen8' in url or 'dex-gen8-new' in url:
                if len(cols) > 2:
                    dex = cols[1]
                    name = cols[2]
                    data.append([dex, name])
            elif 'inventory' in url:
                if len(cols) > 2:
                    item_id = cols[1]
                    name = cols[2]
                    data.append([item_id, name])
            elif 'misc' in url:
                if len(cols) > 1:
                    number = cols[0]
                    name = cols[1]
                    data.append([number, name])

    return data


def main():
    urls = ['https://msikma.github.io/pokesprite/overview/dex-gen7.html',
            'https://msikma.github.io/pokesprite/overview/dex-gen8.html',
            'https://msikma.github.io/pokesprite/overview/dex-gen8-new.html',
            'https://msikma.github.io/pokesprite/overview/inventory.html',
            'https://msikma.github.io/pokesprite/overview/misc.html']

    for url in urls:
        data = extract_table_data(url)
        filename = url.split('/')[-1].split('.')[0] + '.txt'
        with open(filename, 'w') as f:
            for item in data:
                f.write('\t'.join(item))
                f.write('\n')

        # Bereinigung der Dateien
        with open(filename, 'r') as f:
            lines = f.readlines()

        cleaned_lines = []
        replacement_counter = 1000
        symbol = "– "
        for line in lines:
            line = line.replace('\t', ' ')  # Ersetze Tabulator durch Leerzeichen
            if filename == 'inventory.txt' and line.startswith(symbol):  # Überprüfe, ob die Zeile mit "-" beginnt
                line = line.replace(symbol, f'item_{replacement_counter} ', 1)
                replacement_counter += 1
            elif line.startswith(symbol):
                line = line.replace(symbol, f'#{replacement_counter} ', 1)
                replacement_counter += 1
            if line.strip():  # Ignoriere leere Zeilen
                cleaned_lines.append(line)

        # Wenn die geöffnete Datei misc.txt ist, lösche Zeilen, die nur Zahlen enthalten
        if filename == 'misc.txt':
            cleaned_lines = [line for line in cleaned_lines if not line.strip().isdigit()]

        # Entfernen von Duplikaten basierend auf dem Namen
        seen_names = set()
        deduplicated_lines = []
        for line in cleaned_lines:
            _, name = line.split(' ', 1)
            if name not in seen_names:
                deduplicated_lines.append(line)
                seen_names.add(name)

        with open(filename, 'w') as f:
            f.writelines(deduplicated_lines)


if __name__ == '__main__':
    main()