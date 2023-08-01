import os
import shutil

import pandas as pd

def main():
    # Pfad zu den Ordnern
    base_path = '/Volumes/MasterArbeit 3/runs/'

    # Erstelle eine leere Dataframe
    df = pd.DataFrame()

    # Durchlaufe jeden Ordner
    for i in range(1, 14):
        # Ordnername definieren
        folder_name = f"polyomino-{str(i).zfill(2)}"

        # Gesamtpfad zum Ordner
        folder_path = os.path.join(base_path, folder_name)

        # Prüfe, ob der Ordner existiert und Dateien enthält
        if os.path.isdir(folder_path) and os.listdir(folder_path):
            # Erhalte die Liste der Dateien im Ordner
            files = os.listdir(folder_path)

            # Erstelle eine temporäre Dataframe mit den Dateinamen und der Ordnerinformation
            temp_df = pd.DataFrame(files, columns=['filename'])
            temp_df[folder_name] = 1

            # Füge die temporäre Dataframe zur Haupt-Dataframe hinzu
            if df.empty:
                df = temp_df
            else:
                df = pd.merge(df, temp_df, on='filename', how='outer')

        # Drucke eine Meldung, nachdem der Ordner durchlaufen wurde
        print(f"Fertig mit dem Durchlaufen des Ordners {folder_name}")

    # Ersetze NaN durch 0
    df = df.fillna(0)

    # Speichere die Dataframe als .csv-Datei
    df.to_csv('file_report.csv', index=False)
    df.to_excel('file_report.xlsx', index=False)

    # Rückgabe der Dataframe
    return df

def copy_images(df):
    # Pfad zu den Bildern
    source_base_path = '/Volumes/MasterArbeit 3/runs/all_pokemons/'

    # Pfad zu dem Ordner, wo die Dateien hinkopiert werden sollen
    target_base_path = os.getcwd() # der aktuelle Arbeitsverzeichnis

    # Durchlaufe jede Spalte in der Dataframe (außer der ersten Spalte, die die Dateinamen enthält)
    for column in df.columns[1:]:
        # Erstelle den Zielordner, wenn er noch nicht existiert
        target_folder_path = os.path.join(target_base_path, column)
        os.makedirs(target_folder_path, exist_ok=True)

        # Hole die Zeilen, in denen in dieser Spalte eine 0 steht
        missing_files = df[df[column] == 0]['filename']

        # Kopiere jede fehlende Datei in den Zielordner
        for filename in missing_files:
            # Füge die Endung .png hinzu
            filename_png = filename.replace('.txt', '.png')

            # Erstelle den Pfad zur Quelldatei und zur Zieldatei
            source_file_path = os.path.join(source_base_path, filename_png)
            target_file_path = os.path.join(target_folder_path, filename_png)

            # Kopiere die Datei, wenn sie existiert
            if os.path.isfile(source_file_path):
                shutil.copy2(source_file_path, target_file_path)

        # Drucke eine Meldung, nachdem der Ordner durchlaufen wurde
        print(f"Fertig mit dem Kopieren von Dateien in den Ordner {column}")


# Aufrufen der Hauptmethode
if __name__ == "__main__":
    df = main()
    copy_images(df)
