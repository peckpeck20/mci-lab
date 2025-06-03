import pandas as pd
import glob
from pathlib import Path

# Load all CSVs
csv_files = glob.glob('../collectedData/*.csv') 

# Read and concatenate
df = pd.concat((pd.read_csv(f) for f in csv_files), ignore_index=True)

df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y-%m-%d %H:%M:%S')

df = df.sort_values('timestamp')

# Define datasets/ path in root
datasets_path = Path(__file__).resolve().parents[1] / "datasets"
# Save file
output_file = datasets_path / "sensor_dataset.csv"
df.to_csv(output_file, index=False)
