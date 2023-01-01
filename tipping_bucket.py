import RPi.GPIO as GPIO
import time
import csv
import sys
import shutil
import os
from datetime import datetime


# Set the file path
csv_dir = '/home/pi/rainfall/rainfall_data.csv'

# Check if the directories exist
if not os.path.exists(os.path.dirname(csv_dir)):
  # If the directories don't exist, create them
  os.makedirs(os.path.dirname(csv_dir))

# Check if the file exists
if not os.path.exists(csv_dir):
  # If the file doesn't exist, create it
  open(csv_dir, 'a').close()

# Set up the GPIO pin for reading
GPIO.setmode(GPIO.BCM)
GPIO.setup(21,GPIO.IN,pull_up_down=GPIO.PUD_UP)

# Open a file for writing
with open(csv_dir , 'a', newline='') as csvfile:
    # Create a CSV writer object
    writer = csv.writer(csvfile)
    start_time = time.time()
    try:
        while True:
            # Wait for an edge on the GPIO pin
            GPIO.wait_for_edge(21, GPIO.FALLING)
            # Write the data to the CSV file
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "tipped"])
            # Print the event to the console
            print("tipped at " + datetime.now().strftime("%Y-%m-%d %H:%M:%S\n"))
            # Slight pause to debounce
            time.sleep(0.4)
            # Check if it's time to create a backup
            current_time = time.time()
            if current_time - start_time >= 3600:  # 1 hour
                # Create a backup of the file
                shutil.copy('rainfall_data.csv', 'rainfall_data_backup.csv')
                # Reset the start time
                start_time = current_time
    except KeyboardInterrupt:
        # Save the data and close the file when the script is interrupted
        csvfile.close()
        sys.exit()
