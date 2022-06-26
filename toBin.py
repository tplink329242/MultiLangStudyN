import pickle
import csv
from lib.Process_Data import Process_Data


pickle_file = open('Repository_Stats.csv', 'r')

csv_data = csv.reader(pickle_file)

csv_list = []

# try:
#     csv_list = Process_Data.read_in_data('','Repository_Stats','class_name')
# except OverflowError as of:
#     print("After the Overflow error", of)

for eachLine in csv_data:
    csv_list.append(eachLine)
    
#csv_data = pickle.loads(pickle_file)
pickle_output_file = open('Repository_Stats', 'wb')
pickle.dump(csv_list, pickle_output_file)
pickle_file.close()
pickle_output_file.close()
