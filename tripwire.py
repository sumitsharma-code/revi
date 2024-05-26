import hashlib
import os
import sys

# Function to calculate the hash value of a file
def hash_value(file):
    with open(file, "rb") as f:
        data = f.read()
        fileHash = hashlib.md5(data).hexdigest()
        return fileHash


# Function to read the contents of a file
def read_file(directory, file_name):
    file_path = os.path.join(directory, file_name)
    file_hash = hash_value(file_path)
    data = f'{file_name} {file_hash}\n'
    return data


# Function to create a record of hash values for files in a directory
def create_record(directory,record_file):
    try:
        file_path = f"{directory}/{record_file}"
        file_list = os.listdir(directory)
    except FileNotFoundError:
        print(f"Error: The directory {directory} was not found.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred while accessing the directory {directory}: {e}")
        return False
    
    with open(file_path, 'w') as record:
        # Write the directory path to the record file
        record.write(os.path.abspath(directory) + '\n')
    with open(file_path, 'a') as record:
        for file_name in file_list:
            if file_name != record_file:
                record.write(read_file(directory, file_name)) 
    return True

# Function to check for modifications in the directory
def check_dir(record_file):
    modified = []
    removed = []
    added = []
    try:
        file_path_record = f"{directory}/{record_file}"
        with open(file_path_record, 'r') as record:
            lines = record.read()
            pairs = lines.split("\n")
            pairs = pairs[1:-1]
            static_data = []
            for pair in pairs:
                static_data.append(pair.split(" "))
            
            static_file_names = []
            for file_names in static_data:
                        static_file_names.append(file_names[0])
    except FileNotFoundError:
        print(f"Error: The directory {directory} was not found.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred while accessing the directory {directory}: {e}")
        return False

    new_file_list = os.listdir(f"{directory}")
    new_file_list.remove('tripwireRecord')
    
    for file_name in new_file_list:
        if file_name in static_file_names:
            new_hash_value = read_file(directory,file_name).split(" ")[1].rstrip('\n')
            for pair in static_data:
                if(file_name == pair[0]):
                    old_hash_value = pair[1]
            if new_hash_value != old_hash_value:
                modified.append(file_name)
        else:
            added.append(file_name)
    
    removed = list(set(static_file_names) - set(new_file_list))
    
    print("Modified:\n",modified)
    print("\nRemoved:\n",removed)
    print("\nadded:\n",added)

# Main loop to execute tasks
while True:    
    # python tripwire.py tripwireDir tripwireRecord c
    start = input("Start: ")
    task = start.split(" ")

    if len(task) == 5 and task[4] =='c':
        directory = task[2]
        record_file = task[3]
        if not create_record(directory,record_file):
            continue
    else:
        print("Please Enter Valid Arguments")
        continue
    #  python tripwire.py tripwireRecord
    compare = input("Compare: ")
    task = compare.split(" ")

    if len(task)==3 :
        record_file = task[2]
        check_dir(record_file)
    else:
        print("Please Enter Valid Arguments")