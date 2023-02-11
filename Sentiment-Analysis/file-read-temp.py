# Import the required libraries
import os

# Define the location of the directory
path =r"/Users/wasiflatifhussain/Documents/Projects_Nafis/tester-rev"
# Change the directory
os.chdir(path)

def read_files(file_path):
   with open(file_path, 'r') as file:
      print(file.read())

# Iterate over all the files in the directory
for file in os.listdir():
   print(file)
   print(type(file))
   if file.endswith('.txt'):
      # Create the filepath of particular file
      file_path =f"{path}/{file}"

      read_files(file_path)
   break