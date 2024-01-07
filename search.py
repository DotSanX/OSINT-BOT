import pandas as pd
import json
import re
from utils import PATH, stats

async def send_results(bot, results, chat_id):
    for result in results:
        await bot.send_message(chat_id, result)

def search_in_file(filename, text):
    results = []
    try:
        if filename.endswith('.csv'):
            df = pd.read_csv(os.path.join(PATH, filename))
            process_file(df, filename, results, text)
        elif filename.endswith('.txt'):
            with open(os.path.join(PATH, filename), 'r') as f:
                lines = f.readlines()
                process_file(lines, filename, results, text)
        elif filename.endswith('.json'):
            with open(os.path.join(PATH, filename), 'r') as f:
                data = json.load(f)
                process_file(data, filename, results, text)
        stats['files_processed'] += 1
    except Exception as e:
        print(f"Error processing file {filename}: {e}")
        stats['errors'] += 1
    return results

def process_file(data, filename, results, text):
    if isinstance(data, pd.DataFrame):
        for i, row in data.iterrows():
            if re.search(text, str(row.to_string()), re.IGNORECASE):
                result = f"Found in CSV ({filename}), row {i+1}:\n\n"
                for column in data.columns:
                    result += f"{column}: {row[column]}\n"
                results.append(result)
    elif isinstance(data, list):
        for i, line in enumerate(data):
            if re.search(text, line, re.IGNORECASE):
                result = f"Found in TXT ({filename}), line {i+1}:\n{line}"
                results.append(result)
    elif isinstance(data, dict):
        for key, value in data.items():
            if re.search(text, str(value), re.IGNORECASE):
                result = f"Found in JSON ({filename}), key {key}:\n{value}"
                results.append(result)