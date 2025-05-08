import pandas as pd
import glob

# Load all CSVs
csv_files = glob.glob('./collectedData/*.csv')

# Read and concatenate
df = pd.concat((pd.read_csv(f) for f in csv_files), ignore_index=True)

# Parse timestamp (matches your format)
df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y-%m-%d %H:%M:%S')

# Sort and save
df = df.sort_values('timestamp')
df.to_csv('final_dataset.csv', index=False)
