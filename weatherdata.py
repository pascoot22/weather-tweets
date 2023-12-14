# Import Meteostat library and dependencies
from datetime import datetime
import sys
import csv
from meteostat import Point, Daily
from datetime import datetime
from geopy.geocoders import Nominatim

csv.field_size_limit(sys.maxsize)

# Set time period
start = datetime(2018, 1, 1)
end = datetime(2018, 12, 31)

# Create Point for Vancouver, BC
location = Point(49.2497, -123.1193, 70)

# Get daily data for 2018
data = Daily(location, start, end)
data = data.fetch()

# Plot line chart including average, minimum and maximum temperature


def read_csv_column(file_path, column_name):
    try:
        with open(file_path, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            
            # Check if the specified column exists in the CSV file
            if column_name not in reader.fieldnames:
                print(f"Column '{column_name}' not found in the CSV file.")
                return None
            
            # Read the specified column values
            column_values = [row[column_name] for row in reader]
            return column_values
            
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None


file_path = 'tweets.csv'
location = 'location'
time = 'time'

locations = read_csv_column(file_path, location)
times = read_csv_column(file_path,time)

def write_column_to_csv(input_file, output_file, column_name, new_column_values):
    try:
        with open(input_file, 'r', newline='') as infile, open(output_file, 'w', newline='') as outfile:
            reader = csv.DictReader(infile)
            
            # Check if the specified column exists in the CSV file
            
            
            # Add the new column to the header if it doesn't exist
            if column_name not in reader.fieldnames:
                reader.fieldnames.append(column_name)
            
            writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
            
            # Write the header
            writer.writeheader()
            
            # Write rows with the new column values
            for row, new_value in zip(reader, new_column_values):
                row[column_name] = new_value
                writer.writerow(row)
            
            print(f"Column '{column_name}' successfully added to the CSV file.")

    except FileNotFoundError:
        print(f"File not found: {input_file}")

geolocator = Nominatim(user_agent="pat")
input_file_path = 'tweets.csv'
output_file_path = 'temps.csv'
column_name_to_add = 'temps'
new_column_values = []  
time_formatted = []
for t in times:
    month = (t[6:7] if t[5:6] == 0 else t[5:7])
    day = (t[9:10] if t[8:9] == 0 else t[8:10])
    time_formatted.append((datetime(int(t[0:4]),int(month),int(day))))

prev = 0
prevw = 0
w = 0
for i in range(100000):
    print(i)
    same = True
    start = time_formatted[i]
    if i > 0:
        if locations[i] == locations[i - 1]:
            location = prev
        else:
            location = geolocator.geocode(locations[i])
            same = False
        if time_formatted[i - 1] != time_formatted[i]:
            same = False
    else:
        location = geolocator.geocode(locations[i])
        same = False
    if same:
        w = prevw
    else:
        point = Point(location.latitude, location.longitude)
        data = Daily(point, start, start)
        data = data.fetch()
        if len(data.tavg.values) > 0:
            w = data.tavg.values[0]
        else:
            w = -1000
    new_column_values.append(w)
    prev = location
    prevw = w
    

write_column_to_csv(input_file_path, output_file_path, column_name_to_add, new_column_values)