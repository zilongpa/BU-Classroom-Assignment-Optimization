import pickle
import numpy as np
import json
from datetime import datetime
import re
import pandas as pd

input_file = '../data/details.json'
output_file = '../data/details_cleaned.json'
classroom_json = '../data/classroom_data.json'
b2b_distance = "../data/b2b_walking_distance.csv"

def clean_large_json(input_file, output_file, keys_to_remove):
    with open(input_file, 'r', encoding='utf-8') as infile:
        data = json.load(infile)
    def remove_keys(obj, keys):
        if isinstance(obj, dict):
            for key in keys:
                obj.pop(key, None)
            for value in obj.values():
                remove_keys(value, keys)
        elif isinstance(obj, list):
            for item in obj:
                remove_keys(item, keys)
    remove_keys(data, keys_to_remove)
    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)
def remove_class_capacity_999():
    with open(output_file, 'r', encoding='utf-8') as infile:
        data = json.load(infile)

    def remove_capacity_999(obj):
        if isinstance(obj, dict):
            if obj.get("class_capacity") == "999" or obj.get("class_capacity") == 999:
                return None
            new_obj = {}
            for key, value in obj.items():
                result = remove_capacity_999(value)
                if result is not None:
                    new_obj[key] = result
            return new_obj
        elif isinstance(obj, list):
            return [remove_capacity_999(item) for item in obj if remove_capacity_999(item) is not None]
        else:
            return obj
    cleaned_data = remove_capacity_999(data)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(cleaned_data, outfile, indent=4, ensure_ascii=False)
def remove_online_instruction_mode():
    with open(output_file, 'r', encoding='utf-8') as infile:
        data = json.load(infile)
    def remove_online_mode(obj):
        if isinstance(obj, dict):
            if obj.get("instruction_mode") == 'Online':
                return None
            new_obj = {}
            for key, value in obj.items():
                result = remove_online_mode(value)
                if result is not None:
                    new_obj[key] = result
            return new_obj
        elif isinstance(obj, list):
            return [remove_online_mode(item) for item in obj if remove_online_mode(item) is not None]
        else:
            return obj
    cleaned_data = remove_online_mode(data)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(cleaned_data, outfile, indent=4, ensure_ascii=False)
def remove_tba_instructors():
    with open(output_file, 'r', encoding='utf-8') as infile:
        data = json.load(infile)
    def clean_instructors(obj):
        if isinstance(obj, dict):
            if "meetings" in obj:
                for meeting in obj["meetings"]:
                    if "instructors" in meeting:
                        meeting["instructors"] = [
                            instructor for instructor in meeting["instructors"]
                            if instructor.get("name") != "To Be Announced"
                        ]
            for value in obj.values():
                clean_instructors(value)
        elif isinstance(obj, list):
            for item in obj:
                clean_instructors(item)
    clean_instructors(data)
    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)
def remove_dash_instructors():
    with open(output_file, 'r', encoding='utf-8') as infile:
        data = json.load(infile)

    def clean_instructors(obj):
        if isinstance(obj, dict):
            if "meetings" in obj:
                for meeting in obj["meetings"]:
                    if "instructors" in meeting:
                        meeting["instructors"] = [
                            instructor for instructor in meeting["instructors"]
                            if instructor.get("name") != "-"
                        ]
            for value in obj.values():
                clean_instructors(value)
        elif isinstance(obj, list):
            for item in obj:
                clean_instructors(item)

    clean_instructors(data)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)
def clean_empty_instructors_tba_meets_and_empty_times():
    with open(output_file, 'r', encoding='utf-8') as infile:
        data = json.load(infile)
    def clean_data(obj):
        if isinstance(obj, dict):
            if "instructors" in obj and isinstance(obj["instructors"], list) and not obj["instructors"]:
                return None
            if obj.get("meets") == "TBA":
                return None
            if "meeting_time_start" in obj and obj["meeting_time_start"] == "":
                return None
            if "meeting_time_end" in obj and obj["meeting_time_end"] == "":
                return None
            new_obj = {}
            for key, value in obj.items():
                result = clean_data(value)
                if result is not None:
                    new_obj[key] = result
            return new_obj
        elif isinstance(obj, list):
            return [clean_data(item) for item in obj if clean_data(item) is not None]
        else:
            return obj
    cleaned_data = clean_data(data)
    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(cleaned_data, outfile, indent=4, ensure_ascii=False)
def clean_classroom_names():
    with open(classroom_json, 'r', encoding='utf-8') as infile:
        data = json.load(infile)
    def remove_invalid_classrooms(obj):
        if isinstance(obj, dict):
            if "Name" in obj and '/' in obj["Name"]:
                return None
            new_obj = {}
            for key, value in obj.items():
                result = remove_invalid_classrooms(value)
                if result is not None:
                    new_obj[key] = result
            return new_obj
        elif isinstance(obj, list):
            return [remove_invalid_classrooms(item) for item in obj if remove_invalid_classrooms(item) is not None]
        else:
            return obj
    cleaned_data = remove_invalid_classrooms(data)
    with open(classroom_json, 'w', encoding='utf-8') as outfile:
        json.dump(cleaned_data, outfile, indent=4, ensure_ascii=False)
def clean_classroom_names_hyphen():
    with open(classroom_json, 'r', encoding='utf-8') as infile:
        data = json.load(infile)
    def process_classroom_names(obj):
        if isinstance(obj, dict):
            if "Name" in obj:
                cleaned_name = obj["Name"].replace('-', ' ')
                cleaned_name = re.sub(r'\(.*$', '', cleaned_name).strip()
                obj["Name"] = cleaned_name
            for key, value in obj.items():
                process_classroom_names(value)
        elif isinstance(obj, list):
            for item in obj:
                process_classroom_names(item)
    process_classroom_names(data)
    with open(classroom_json, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)
def clean_none_and_no_room_classrooms():
    with open(output_file, 'r', encoding='utf-8') as infile:
        data = json.load(infile)
    cleaned_data = []
    for course in data:
        section_info = course.get("section_info", {})
        meetings = section_info.get("meetings", [])
        if any(meeting.get("room") in [None, "NO ROOM"] for meeting in meetings):
            continue
        else:
            cleaned_data.append(course)
    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(cleaned_data, outfile, indent=4, ensure_ascii=False)
def clean_empty_meetings():
    with open(output_file, 'r', encoding='utf-8') as infile:
        data = json.load(infile)
    cleaned_data = []
    for course in data:
        section_info = course.get("section_info", {})
        meetings = section_info.get("meetings", [])
        if meetings:
            cleaned_data.append(course)
    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(cleaned_data, outfile, indent=4, ensure_ascii=False)
def remove_building_codes(input_file, output_file, remove_bldg_cd):
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for item in data:
        if 'section_info' in item and 'meetings' in item['section_info']:
            item['section_info']['meetings'] = [
                meeting for meeting in item['section_info']['meetings']
                if meeting.get('bldg_cd') not in remove_bldg_cd
            ]
        if 'similar_classes' in item:
            for similar_class in item['similar_classes']:
                if 'meeting_patterns' in similar_class:
                    similar_class['meeting_patterns'] = [
                        pattern for pattern in similar_class['meeting_patterns']
                        if pattern.get('bldg_cd') not in remove_bldg_cd
                    ]

    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
def also_remove_building_codes(remove_bldg_cd):
    with open(classroom_json, 'r') as file:
        classrooms = json.load(file)
    cleaned_classrooms = [
        classroom for classroom in classrooms
        if not any(classroom.get('Name', '').startswith(prefix) for prefix in remove_bldg_cd)
    ]
    with open(classroom_json, 'w') as file:
        json.dump(cleaned_classrooms, file, indent=4)
def clean_schedule(professor_schedule):
    cleaned_schedule = {}
    for key, schedule in professor_schedule.items():
        merged_dict = {}
        for item in schedule:
            start_end = (item[0], item[1])
            if start_end in merged_dict:
                merged_dict[start_end] += item[2]
            else:
                merged_dict[start_end] = item[2]
        cleaned_schedule[key] = [(start, end, count) for (start, end), count in merged_dict.items()]

    return cleaned_schedule
def check_tags():
    with open(classroom_json, 'r') as file:
        classrooms = json.load(file)

    cleaned_classrooms = [
        classroom for classroom in classrooms
        if not ("Details" in classroom and
                "Classroom Tag" in classroom["Details"] and
                "Medical Campus" in classroom["Details"]["Classroom Tag"])
    ]

    with open(classroom_json, 'w') as file:
        json.dump(cleaned_classrooms, file, indent=4)
def clean_tags():
    with open(classroom_json, 'r') as file:
        classrooms = json.load(file)

    cleaned_classrooms = [
        classroom for classroom in classrooms
        if not ("Details" in classroom and
                "Classroom Tag" in classroom["Details"] and
                any("Fenway Campus" in tag for tag in classroom["Details"]["Classroom Tag"]))
    ]

    with open(classroom_json, 'w') as file:
        json.dump(cleaned_classrooms, file, indent=4)
def extract_capacity_from_additional_info():
    # Open the JSON file for reading and load its content into the 'data' variable
    with open(classroom_json, 'r', encoding='utf-8') as infile:
        data = json.load(infile)

    # Initialize an empty list to store the capacities found
    capacities = []

    # Define a helper function to find capacities within the JSON structure
    def find_capacity(obj):
        # Check if the current object is a dictionary
        if isinstance(obj, dict):
            # If 'AdditionalInfo' and 'Capacity' are keys in the object, attempt to extract the capacity
            if "AdditionalInfo" in obj and "Capacity" in obj["AdditionalInfo"]:
                try:
                    # Convert the capacity to an integer and add it to the capacities list
                    capacities.append(int(obj["AdditionalInfo"]["Capacity"]))
                except ValueError:
                    # If conversion to integer fails, ignore this capacity
                    pass

            # Recursively search for capacities in each value of the dictionary
            for value in obj.values():
                find_capacity(value)
        # If the current object is a list, iterate over its items and apply the function on each
        elif isinstance(obj, list):
            for item in obj:
                find_capacity(item)

    # Start the capacity finding process on the main data structure loaded from JSON
    find_capacity(data)

    # Return the list of capacities extracted from the JSON data
    return capacities
def extract_name_capacity_dict():
    # This function reads a JSON file containing classroom data and extracts a dictionary mapping classroom names to their capacities.

    with open(classroom_json, 'r', encoding='utf-8') as infile:
        # Open the JSON file and load its content into a Python dictionary.
        data = json.load(infile)

    # Initialize a dictionary to store name-capacity pairs.
    name_capacity_dict = {}

    # Define a recursive function to traverse through JSON objects and find name-capacity pairs.
    def find_name_capacity(obj):
        if isinstance(obj, dict):
            # If the object is a dictionary, check for the presence of "Name" and "Capacity" in the "AdditionalInfo" field.
            if "Name" in obj and "AdditionalInfo" in obj and "Capacity" in obj["AdditionalInfo"]:
                try:
                    name_capacity_dict[obj["Name"]] = int(obj["AdditionalInfo"]["Capacity"])
                except ValueError:
                    # If the conversion to an integer fails, ignore this entry.
                    pass
            # Recursively process all values in the dictionary.
            for value in obj.values():
                find_name_capacity(value)
        elif isinstance(obj, list):
            # If the object is a list, iterate over each item and apply the function recursively.
            for item in obj:
                find_name_capacity(item)

    # Start the recursive process to populate the name_capacity_dict with data from the JSON.
    find_name_capacity(data)

    # Return the dictionary containing classroom names and their corresponding capacities.
    return name_capacity_dict
def extract_professor_mapping():
    # Open the JSON file specified by output_file and load its contents into a Python dictionary.
    with open(output_file, 'r', encoding='utf-8') as infile:
        data = json.load(infile)

    # Initialize a dictionary to store the mapping of professor names to unique IDs.
    professor_mapping = {}
    # A counter to assign a unique ID to each professor.
    professor_id_counter = 0

    # Define a recursive function to find instructors within the data.
    # The use of nonlocal indicates that professor_id_counter is used from the parent function's scope.
    def find_instructors(obj):
        nonlocal professor_id_counter
        if isinstance(obj, dict):
            # If the object is a dictionary, look for "meetings".
            if "meetings" in obj:
                # If "meetings" exists, iterate over each meeting.
                for meeting in obj["meetings"]:
                    # Check if the meeting has "instructors".
                    if "instructors" in meeting:
                        # For each instructor, retrieve their "name".
                        for instructor in meeting["instructors"]:
                            name = instructor.get("name")
                            # If the name is valid and not already in the mapping,
                            # assign a new unique ID and update the counter.
                            if name and name not in professor_mapping:
                                professor_mapping[name] = professor_id_counter
                                professor_id_counter += 1
            # Recursively process all values in the dictionary, traversing deeper.
            for value in obj.values():
                find_instructors(value)
        elif isinstance(obj, list):
            # If the object is a list, apply the function recursively to each item.
            for item in obj:
                find_instructors(item)

    # Call the recursive function on the main data object loaded from JSON.
    find_instructors(data)

    # Return the dictionary which contains the mapping of professor names to unique IDs.
    return professor_mapping
def build_professor_schedule():
    # Open the JSON file that contains the cleaned data and load it into a variable
    with open(output_file, 'r', encoding='utf-8') as infile:
        data = json.load(infile)

    # Initialize an empty dictionary to store the schedule of each professor
    professor_schedule = {}

    # Map days of the week to corresponding indices
    day_mapping = {
        "Mo": 0, "Tu": 1, "We": 2, "Th": 3, "Fr": 4, "Sa": 5, "Su": 6
    }

    # Helper function to convert a time string into a time slot index
    def parse_time(time_str, day):
        # Parse the time string into a datetime object
        time_obj = datetime.strptime(time_str, "%I:%M%p")
        # Convert hours and minutes to total minutes
        minutes = time_obj.hour * 60 + time_obj.minute
        # Calculate a unique time slot index considering both time and day
        return (minutes // 5) + day * (24 * 60 // 5)

    # Recursive function to find meetings in JSON data and build the schedule
    def find_meetings(obj):
        if isinstance(obj, dict):
            # Check if the object contains meeting information necessary for building the schedule
            if "meetings" in obj and "class_availability" in obj:
                # Retrieve and convert the class capacity to integer
                capacity = obj["class_availability"].get("class_capacity")
                if capacity is not None:
                    capacity = int(capacity)

                # Iterate over each meeting to extract details
                for meeting in obj["meetings"]:
                    if "instructors" in meeting and "days" in meeting and "meeting_time_start" in meeting and "meeting_time_end" in meeting:
                        # Convert the days string to a list of corresponding indices using day_mapping
                        days_str = meeting["days"]
                        days = [day_mapping[days_str[i:i+2]] for i in range(0, len(days_str), 2) if days_str[i:i+2] in day_mapping]

                        # Iterate over each instructor and update their schedule
                        for instructor in meeting["instructors"]:
                            professor_name = instructor.get("name")
                            professor_id = professor_mapping.get(professor_name)

                            if professor_id is not None:
                                # Ensure there's a list for storing the professor's meetings
                                if professor_id not in professor_schedule:
                                    professor_schedule[professor_id] = []

                                # Add the meeting details to the professor's schedule for each day
                                for day in days:
                                    start_time = parse_time(meeting["meeting_time_start"], day)
                                    end_time = parse_time(meeting["meeting_time_end"], day)
                                    professor_schedule[professor_id].append((start_time, end_time, capacity))

            # Recursively process all values in the dictionary
            for value in obj.values():
                find_meetings(value)
        elif isinstance(obj, list):
            # Recursively apply the function to each item in a list
            for item in obj:
                find_meetings(item)

    # Begin the process of finding meetings
    find_meetings(data)

    # Return the completed schedule for each professor
    return professor_schedule
def build_monday_professor_schedule():
    # Load data from the specified JSON file. The purpose of this step is to read the structured class data
    # to extract relevant meeting information.
    with open(output_file, 'r', encoding='utf-8') as infile:
        data = json.load(infile)

    # Initialize an empty dictionary to store professors' schedules.
    # Keys will be unique professor IDs and values will be lists of their scheduled meetings.
    professor_schedule = {}

    # Mapping of day abbreviations to indices, helping translate string representations of days into numeric indices.
    day_mapping = {
        "Mo": 0, "Tu": 1, "We": 2, "Th": 3, "Fr": 4, "Sa": 5, "Su": 6
    }

    # Function to convert a time string into the number of 5-minute units from the start of the day.
    # It helps in creating a uniform representation of time for easy comparison and scheduling.
    def parse_time(time_str, day):
        time_obj = datetime.strptime(time_str, "%I:%M%p")
        minutes = time_obj.hour * 60 + time_obj.minute
        return minutes // 5

    # Recursive function to traverse the JSON data structure and find meetings scheduled on Monday.
    # The focus is on extracting meeting times and associating them with instructors, updating their schedules.
    def find_monday_meetings(obj):
        if isinstance(obj, dict):
            # Check if the current dict contains meeting and capacity information.
            if "meetings" in obj and "class_availability" in obj:
                capacity = obj["class_availability"].get("class_capacity")
                if capacity is not None:
                    capacity = int(capacity)

                for meeting in obj["meetings"]:
                    # Look for meetings with defined days, start time, end time, and instructors.
                    if (
                        "instructors" in meeting
                        and "days" in meeting
                        and "meeting_time_start" in meeting
                        and "meeting_time_end" in meeting
                    ):
                        # Determine which days the meeting occurs, converting them to indices using day_mapping.
                        days_str = meeting["days"]
                        days = [
                            day_mapping[days_str[i:i+2]]
                            for i in range(0, len(days_str), 2)
                            if days_str[i:i+2] in day_mapping
                        ]

                        # If the meeting takes place on Monday (index 0), process the meeting details.
                        if 0 in days:
                            for instructor in meeting["instructors"]:
                                professor_name = instructor.get("name")
                                professor_id = professor_mapping.get(professor_name)

                                if professor_id is not None:
                                    # Initialize the schedule list for the professor if it does not exist.
                                    if professor_id not in professor_schedule:
                                        professor_schedule[professor_id] = []

                                    # Parse the start and end time of the meeting and add them to the schedule.
                                    start_time = parse_time(meeting["meeting_time_start"], 0)
                                    end_time = parse_time(meeting["meeting_time_end"], 0)
                                    professor_schedule[professor_id].append((start_time, end_time, capacity))

            # Continue traversing through other elements of the JSON structure.
            for value in obj.values():
                find_monday_meetings(value)
        elif isinstance(obj, list):
            # Apply the search function to each item if the current object is a list.
            for item in obj:
                find_monday_meetings(item)

    # Start the recursive search for Monday meetings in the loaded data.
    find_monday_meetings(data)

    # Return the fully constructed dictionary of Monday schedules for each professor.
    return professor_schedule
def create_classroom_mapping():
    # Load JSON data from the specified file into the 'data' variable
    with open(classroom_json, 'r', encoding='utf-8') as infile:
        data = json.load(infile)

    # Dictionary to hold the mapping of classroom names to unique identifiers
    classroom_mapping = {}

    # Counter to generate unique identifiers for each classroom
    classroom_id_counter = 0

    # Recursive function to traverse the JSON structure to find classrooms
    def find_classrooms(obj):
        nonlocal classroom_id_counter  # Allow the nested function to modify this variable
        if isinstance(obj, dict):  # Check if the object is a dictionary
            if "Name" in obj:  # If the classroom name is found in the object
                classroom_name = obj["Name"]

                # If the classroom name is not already in the mapping, add it
                if classroom_name not in classroom_mapping:
                    classroom_mapping[classroom_name] = classroom_id_counter
                    classroom_id_counter += 1  # Increment the counter for the next unique ID

            # Iterate over dictionary values for further processing
            for value in obj.values():
                find_classrooms(value)  # Recursive call for nested dictionaries
        elif isinstance(obj, list):  # Check if the object is a list
            # Iterate over list items to look for classrooms
            for item in obj:
                find_classrooms(item)  # Recursive call for list items

    find_classrooms(data)  # Initial call to the recursive function with loaded data

    # Return the final mapping of classroom names to IDs
    return classroom_mapping
def allocate_professor_courses(professor_mapping, classroom_mapping, output_file):
    # Determine the number of unique professors and rooms
    N = len(professor_mapping)
    M = len(classroom_mapping)

    # Calculate the total number of 5-minute intervals in a week
    T = 7 * 24 * 60 // 5

    # Initialize a 3D array for professor-room-time allocations
    professor_courses = np.zeros((N, M, T), dtype=int)

    # Helper function to convert time to 5-minute intervals
    def parse_time_to_5_min_units(time_str):
        time_obj = datetime.strptime(time_str, "%I:%M%p")
        return (time_obj.hour * 60 + time_obj.minute) // 5

    # Load JSON data
    with open(output_file, 'r', encoding='utf-8') as infile:
        data = json.load(infile)

        for course in data:
            section_info = course.get("section_info", {})
            meetings = section_info.get("meetings", [])

            for obj in meetings:
                room_field = obj.get("room", "")
                room_parts = room_field.split()
                room_name = room_parts[-2] + " " + room_parts[-1] if len(room_parts) >= 2 else None

                if room_name in [None, "NO ROOM"]:
                    continue

                instructors = obj.get("instructors", [])
                for instructor in instructors:
                    professor_name = instructor.get("name")
                    professor_id = professor_mapping.get(professor_name)
                    room_id = classroom_mapping.get(room_name)

                    if professor_id is None or room_id is None:
                        continue

                    days_str = obj.get("days", "")
                    start_time = parse_time_to_5_min_units(obj["meeting_time_start"])
                    end_time = parse_time_to_5_min_units(obj["meeting_time_end"])

                    day_mapping = {"Mo": 0, "Tu": 1, "We": 2, "Th": 3, "Fr": 4, "Sa": 5, "Su": 6}
                    for day_abbr in [days_str[i:i + 2] for i in range(0, len(days_str), 2)]:
                        day = day_mapping.get(day_abbr)
                        if day is not None:
                            start_k = start_time + day * (24 * 60 // 5)
                            end_k = end_time + day * (24 * 60 // 5)
                            for k in range(start_k, end_k):
                                professor_courses[professor_id][room_id][k] = 1

    return professor_courses
def allocate_monday_professor_courses(professor_mapping, classroom_mapping, output_file):
    # Determine the number of professors and rooms
    N = len(professor_mapping)
    M = len(classroom_mapping)

    # Define the number of 5-minute intervals for Monday
    T_monday = 24 * 60 // 5

    # Initialize the 3D array for Monday allocations
    professor_courses_monday = np.zeros((N, M, T_monday), dtype=int)

    # Helper function to parse time to 5-minute intervals
    def parse_time_to_5_min_units(time_str):
        time_obj = datetime.strptime(time_str, "%I:%M%p")
        return (time_obj.hour * 60 + time_obj.minute) // 5

    # Load JSON data
    with open(output_file, 'r', encoding='utf-8') as infile:
        data = json.load(infile)

        for course in data:
            section_info = course.get("section_info", {})
            meetings = section_info.get("meetings", [])

            for obj in meetings:
                room_field = obj.get("room", "")
                room_parts = room_field.split()
                room_name = room_parts[-2] + " " + room_parts[-1] if len(room_parts) >= 2 else None

                if room_name in [None, "NO ROOM"]:
                    continue

                instructors = obj.get("instructors", [])
                for instructor in instructors:
                    professor_name = instructor.get("name")
                    professor_id = professor_mapping.get(professor_name)
                    room_id = classroom_mapping.get(room_name)

                    if professor_id is None or room_id is None:
                        continue

                    days_str = obj.get("days", "")
                    if "Mo" not in days_str:  # Only process records that include Monday
                        continue

                    start_time = parse_time_to_5_min_units(obj["meeting_time_start"])
                    end_time = parse_time_to_5_min_units(obj["meeting_time_end"])

                    day_mapping = {"Mo": 0, "Tu": 1, "We": 2, "Th": 3, "Fr": 4, "Sa": 5, "Su": 6}
                    for day_abbr in [days_str[i:i+2] for i in range(0, len(days_str), 2)]:
                        day = day_mapping.get(day_abbr)
                        if day == 0:  # Process only Monday
                            for k in range(start_time, end_time):
                                professor_courses_monday[professor_id][room_id][k] = 1

    return professor_courses_monday
def create_walking_cost_matrix(classroom_mapping, b2b_distance_file):
    # Step 1: Read the 'b2b_walking_distance.csv' file into a pandas DataFrame.
    b2b_distance = pd.read_csv(b2b_distance_file)

    # Step 2: Create a dictionary of building names mapped to their respective indices from classroom_mapping.
    buildings = {name.split()[0]: idx for name, idx in classroom_mapping.items()}

    # Step 3: Define the number of classrooms using the size of classroom_mapping.
    num_classrooms = len(classroom_mapping)

    # Initialize the walking_cost matrix with 'inf', denoting initially unknown walking distances.
    walking_cost = np.full((num_classrooms, num_classrooms), np.inf)

    # Iterate over each possible classroom pairing to set the initial walking costs.
    for i in range(num_classrooms):
        for j in range(num_classrooms):
            # Set the walking cost to 0 for the same room (no walking required).
            if i == j:
                walking_cost[i][j] = 0
            # Assign a generic cost of 10 for moving within the same building.
            elif list(classroom_mapping.keys())[i].split()[0] == list(classroom_mapping.keys())[j].split()[0]:
                walking_cost[i][j] = 10

    # Step 4: Iterate over each row in the 'b2b_distance' DataFrame to update the walking_cost matrix.
    for _, row in b2b_distance.iterrows():
        building_a, building_b, distance = row['abbreviationA'], row['abbreviationB'], row['distance']
        # Update the matrix for pairs of classrooms between each pair of buildings.
        for classroom_a, idx_a in classroom_mapping.items():
            for classroom_b, idx_b in classroom_mapping.items():
                if classroom_a.split()[0] == building_a and classroom_b.split()[0] == building_b:
                    # Set the walking distance for the respective indices in the walking_cost matrix.
                    walking_cost[idx_a][idx_b] = distance
                    walking_cost[idx_b][idx_a] = distance

    # Step 5: Identify positions where walking_cost remains 'inf' (meaning unreachable).
    inf_positions = np.where(walking_cost == np.inf)
    if inf_positions[0].size > 0:
        for i, j in zip(inf_positions[0], inf_positions[1]):
            print(f"Inf found at walking_cost[{i}][{j}]")

    return walking_cost

keys_to_remove = ["additionalLinks", "bookstore", "cfg", "catalog_descr", "materials", "enrollment_information", "reserve_caps", "catalog_descr", "messages", "notes"]
clean_large_json(input_file, output_file, keys_to_remove)
remove_class_capacity_999()
remove_online_instruction_mode()
remove_tba_instructors()
remove_dash_instructors()
clean_empty_instructors_tba_meets_and_empty_times()
clean_classroom_names()
clean_classroom_names_hyphen()
clean_none_and_no_room_classrooms()
clean_empty_meetings()
remove_bldg_cd = ["ALB", "CTC", "INS", "SPH", "XBG", "MED", "FAB", "FCB", "FCC", "HAW", "GDS", "FPH", "EVN"]
remove_building_codes(output_file, output_file, remove_bldg_cd)
also_remove_building_codes(remove_bldg_cd)
check_tags()
capacities = extract_capacity_from_additional_info()
name_capacity_dict = extract_name_capacity_dict()
professor_mapping = extract_professor_mapping()
professor_schedule = build_professor_schedule()
professor_schedule = clean_schedule(professor_schedule)
monday_professor_schedule = build_monday_professor_schedule()
monday_professor_schedule = clean_schedule(monday_professor_schedule)
classroom_mapping = create_classroom_mapping()
professor_courses = allocate_professor_courses(professor_mapping, classroom_mapping, output_file)
professor_courses_monday = allocate_monday_professor_courses(professor_mapping, classroom_mapping, output_file)
walking_cost = create_walking_cost_matrix(classroom_mapping, b2b_distance)
data_to_export = {
    "monday_professor_schedule": monday_professor_schedule,
    "professor_mapping": professor_mapping,
    "classroom_mapping": classroom_mapping,
    "professor_courses_monday ": professor_courses_monday ,
    "capacities": capacities,
    "walking_cost": walking_cost
}

with open("data_export.pkl", "wb") as file:
    pickle.dump(data_to_export, file)


