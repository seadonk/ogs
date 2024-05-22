import json

# Load the data from the file
with open('output.json', 'r') as f:
    data = json.load(f)

# Sort the data by 'meeting_number'
data.sort(key=lambda x: x['meeting_number'], reverse=True)

# Write the sorted data back to the file
with open('output.json', 'w') as f:
    json.dump(data, f, indent=4)