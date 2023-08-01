import matplotlib.pyplot as plt
import pandas as pd


# Pfad zur Datei
file_path = '/Users/mama/Documents/Mappe3.xlsx' # Ersetzen Sie diesen Pfad mit dem tatsächlichen Pfad zu Ihrer Datei

# Lese Excel-Datei
data = pd.read_excel(file_path)
print(data.head())


# Make your plot
plt.figure()
plt.scatter(data['Spielfeld-Größe nxn'], data['Summe Variablen'])
plt.title('Korrelation zwischen Spielfeld-Größe und Summe Variablen')
plt.xlabel('Spielfeld-Größe n x n')
plt.ylabel('Summe Variablen')
plt.savefig('plot1.png', dpi=300)

# Repeat for the second plot
plt.figure()
plt.scatter(data['Spielfeld-Größe nxn'], data['Anzahl Klauseln AtMostOne'])
plt.title('Korrelation zwischen Spielfeld-Größe und Anzahl Klauseln AtMostOne')
plt.xlabel('Spielfeld-Größe n x n')
plt.ylabel('Anzahl Klauseln AtMostOne')
plt.savefig('plot2.png', dpi=300)

# Erstellt eine Grafik mit den ersten 20 Datensätzen
plt.figure()
# Erster Datensatz in blau
plt.scatter(data['Spielfeld-Größe nxn'][:20], data['Summe Variablen'][:20], color='blue', label='Summe Variablen')
# Zweiter Datensatz in rot
plt.scatter(data['Spielfeld-Größe nxn'][:20], data['Anzahl Klauseln AtMostOne'][:20], color='red', marker='x', label='Anzahl Klauseln aus AtMostOne')
plt.scatter(data['Spielfeld-Größe nxn'][:20], data['ExactlyOne-Klauseln'][:20], color='green', label='ExactlyOne-Klauseln')
plt.title('Korrelation zwischen Spielfeld-Größe und Anzahl Klauseln aus AtMostOne (Erste 20 Einträge)')
plt.xlabel('Spielfeld-Größe n x n')
plt.ylabel('Klauseln')
plt.legend()
plt.savefig('plot3.png', dpi=300)

# Erstellt eine Grafik mit beiden Datensätzen
plt.figure()
ax = plt.gca()  # get current axis
ax.set_yscale('log')  # set logarithmic scale on y-axis
# Erster Datensatz in blau
plt.scatter(data['Spielfeld-Größe nxn'], data['Summe Variablen'], color='blue', label='Summe Variablen')
# Zweiter Datensatz in rot
plt.scatter(data['n'], data['Summe Klauseln'], color='red', marker='x', label='Anzahl Klauseln aus AtMostOne')
plt.title('Korrelation zwischen Spielfeld-Größe und Anzahl Klauseln aus AtMostOne')
plt.xlabel('Spielfeld-Größe n x n')
plt.ylabel('Klauseln')
plt.legend()
plt.savefig('plot4.png', dpi=300)

#----------------------------------------------------------------
# Load the Excel file
df = pd.read_excel("/Users/mama/Documents/Mappe5.xlsx")

# Rename the column "Tabelle 1: 1" to "p"
df.rename(columns={"Tabelle 1: 1": "p"}, inplace=True)

# Create a new DataFrame, dropping rows where all the 'BenTime' values are null
df_time = df[['p', 'Ben1Time', 'Ben2Time', 'Ben3Time', 'Ben4Time', 'Ben5Time']].dropna(how='all')

# Define a dictionary to map existing column names to the desired ones in the legend
legend_labels = {'Ben1Time': 'Benchmark 1',
                 'Ben2Time': 'Benchmark 2',
                 'Ben3Time': 'Benchmark 3',
                 'Ben4Time': 'Benchmark 4',
                 'Ben5Time': 'Benchmark 5'}

# Plotting
plt.figure(figsize=(12, 8))

for column in df_time.columns[1:]:
    plt.semilogy(df_time['p'], df_time[column], label=legend_labels[column])

plt.xlabel('Parameter p')
plt.ylabel('Zeit in Sekunden (log Skala)')
plt.legend()
plt.grid(True)
plt.savefig('plot5.png', dpi=300)

#----------------------------------------------------------------

# Load the Excel file
df = pd.read_excel("/Users/mama/Documents/Mappe5.xlsx")

# Rename the column "Tabelle 1: 1" to "p"
df.rename(columns={"Tabelle 1: 1": "p"}, inplace=True)

# Create a new DataFrame, dropping rows where all the 'BenTime' and 'BenRuntime' values are null
df_time = df[['p',
              'Ben1Runtime', 'Ben2Runtime', 'Ben3Runtime', 'Ben4Runtime', 'Ben5Runtime']].dropna(how='all')

# Define a dictionary to map existing column names to the desired ones in the legend
legend_labels = {'Ben1Runtime': 'Benchmark 1 Laufzeit', 'Ben2Runtime': 'Benchmark 2 Laufzeit',
                 'Ben3Runtime': 'Benchmark 3 Laufzeit', 'Ben4Runtime': 'Benchmark 4 Laufzeit', 'Ben5Runtime': 'Benchmark 5 Laufzeit'}

# Plotting
plt.figure(figsize=(12, 8))

for column in df_time.columns[1:]:
    plt.semilogy(df_time['p'], df_time[column], label=legend_labels[column])

plt.xlabel('Parameter p')
plt.ylabel('Zeit in Sekunden (log Skala)')
plt.legend()
plt.grid(True)
plt.savefig('plot5_5.png', dpi=300)


#----------------------------------------------------------------
import pandas as pd
import matplotlib.pyplot as plt

def ram_to_mb(ram_str):
    if pd.isnull(ram_str):
        return None
    if isinstance(ram_str, float):  # Handle numeric values
        return ram_str
    if ' ' in ram_str:  # If there's a space, split into number and unit
        number, unit = ram_str.split()
        number = float(number)
    else:  # If there's no space, assume the last character is the unit
        number = float(ram_str[:-1])
        unit = ram_str[-1]
    unit = unit.lower()  # Make the unit check case-insensitive
    if unit == 'g':
        return number * 1024  # Convert GB to MB
    elif unit == 'm':
        return number  # No conversion needed
    else:
        raise ValueError(f"Unerwartete Einheit {unit} im RAM-String {ram_str}")

df = pd.read_excel("/Users/mama/Documents/Mappe5.xlsx")  # Geben Sie hier Ihren Dateipfad ein

# Apply the function to the RAM columns
for i in range(1, 6):
    df[f'Ben{i}RAM'] = df[f'Ben{i}RAM'].apply(ram_to_mb)

# Create a new DataFrame, dropping rows where all the 'BenRAM' values are null
df_ram = df[['p', 'Ben1RAM', 'Ben2RAM', 'Ben3RAM', 'Ben4RAM', 'Ben5RAM']].dropna(how='all')

# Define a dictionary to map existing column names to the desired ones in the legend
legend_labels = {'Ben1RAM': 'Benchmark 1',
                 'Ben2RAM': 'Benchmark 2',
                 'Ben3RAM': 'Benchmark 3',
                 'Ben4RAM': 'Benchmark 4',
                 'Ben5RAM': 'Benchmark 5'}

# Plotting
plt.figure(figsize=(12, 8))

for column in df_ram.columns[1:]:
    plt.semilogy(df_ram['p'], df_ram[column], label=legend_labels[column])

plt.xlabel('Parameter p')
plt.ylabel('RAM-Verbrauch in MB (log Skala)')
plt.legend()
plt.grid(True)
plt.savefig('plot6.png', dpi=300)



if __name__ == "__main__":
    pass

