import os
import pandas as pd

data_dir = './sftp-downloads'  # Update this path if needed

for filename in os.listdir(data_dir):
    if filename.endswith('.csv'):
        file_path = os.path.join(data_dir, filename)
        try:
            df = pd.read_csv(file_path, nrows=5)
            print(f"\n📄 {filename}")
            print(df.columns.tolist())
        except Exception as e:
            print(f"\n❌ Error reading {filename}: {e}")