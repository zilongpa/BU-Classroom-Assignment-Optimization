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

def data_cleaning_course(input_file, output_file, keys_to_remove, remove_bldg_cd=[]):
    with open(input_file, 'r', encoding='utf-8') as infile:
        data = json.load(infile)

    def traverse_data(obj, func):
        if isinstance(obj, dict):
            return func(obj)
        elif isinstance(obj, list):
            new_list = []
            for item in obj:
                result = traverse_data(item, func)
                if result is not None:
                    new_list.append(result)
            return new_list
        else:
            return obj

    def remove_keys_func(obj):
        if isinstance(obj, dict):
            for k in keys_to_remove:
                obj.pop(k, None)
            new_obj = {}
            for k, v in obj.items():
                res = traverse_data(v, remove_keys_func)
                if res is not None:
                    new_obj[k] = res
            return new_obj
        else:
            return obj

    def remove_capacity_999_func(obj):
        if isinstance(obj, dict):
            if obj.get("class_capacity") in [999, "999"]:
                return None
            new_obj = {}
            for k, v in obj.items():
                res = traverse_data(v, remove_capacity_999_func)
                if res is not None:
                    new_obj[k] = res
            return new_obj
        return obj

    def remove_online_mode_func(obj):
        if isinstance(obj, dict):
            if obj.get("instruction_mode") == "Online":
                return None
            new_obj = {}
            for k, v in obj.items():
                res = traverse_data(v, remove_online_mode_func)
                if res is not None:
                    new_obj[k] = res
            return new_obj
        return obj

    def remove_unwanted_instructors_func(obj):
        if isinstance(obj, dict):
            if "meetings" in obj:
                for meeting in obj["meetings"]:
                    if "instructors" in meeting:
                        meeting["instructors"] = [
                            inst for inst in meeting["instructors"]
                            if inst.get("name") not in ["To Be Announced", "-"]
                        ]
            new_obj = {}
            for k, v in obj.items():
                res = traverse_data(v, remove_unwanted_instructors_func)
                if res is not None:
                    new_obj[k] = res
            return new_obj
        return obj

    def clean_invalid_entries_func(obj):
        if isinstance(obj, dict):
            if ("instructors" in obj and isinstance(obj["instructors"], list) and not obj["instructors"]) \
               or obj.get("meets") == "TBA" \
               or (obj.get("meeting_time_start") == "") \
               or (obj.get("meeting_time_end") == ""):
                return None
            new_obj = {}
            for k, v in obj.items():
                res = traverse_data(v, clean_invalid_entries_func)
                if res is not None:
                    new_obj[k] = res
            return new_obj
        return obj

    def remove_no_room_classes(data_list):
        cleaned = []
        for course in data_list:
            section_info = course.get("section_info", {})
            meetings = section_info.get("meetings", [])
            if any(m.get('room') in [None, "NO ROOM"] for m in meetings):
                continue
            cleaned.append(course)
        return cleaned

    def remove_empty_meetings(data_list):
        cleaned = []
        for course in data_list:
            section_info = course.get("section_info", {})
            meetings = section_info.get("meetings", [])
            if meetings:
                cleaned.append(course)
        return cleaned

    def remove_bldg_cd_func(data_list):
        for item in data_list:
            if 'section_info' in item and 'meetings' in item['section_info']:
                item['section_info']['meetings'] = [
                    m for m in item['section_info']['meetings']
                    if m.get('bldg_cd') not in remove_bldg_cd
                ]
            if 'similar_classes' in item:
                for sc in item['similar_classes']:
                    if 'meeting_patterns' in sc:
                        sc['meeting_patterns'] = [
                            p for p in sc['meeting_patterns']
                            if p.get('bldg_cd') not in remove_bldg_cd
                        ]
        return data_list

    data = traverse_data(data, remove_keys_func)
    data = traverse_data(data, remove_capacity_999_func)
    data = traverse_data(data, remove_online_mode_func)
    data = traverse_data(data, remove_unwanted_instructors_func)
    data = traverse_data(data, clean_invalid_entries_func)

    if isinstance(data, list):
        data = remove_no_room_classes(data)
        data = remove_empty_meetings(data)
        data = remove_bldg_cd_func(data)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)



def data_cleaning_classroom(remove_bldg_cd):
    import json
    import re

    with open(classroom_json, 'r', encoding='utf-8') as infile:
        data = json.load(infile)

    def clean_data(obj):
        if isinstance(obj, dict):
            # Remove invalid classrooms with '/' in the Name
            if "Name" in obj and '/' in obj["Name"]:
                return None
            # Clean classroom names by replacing '-' with ' ' and removing text in parentheses
            if "Name" in obj:
                cleaned_name = obj["Name"].replace('-', ' ')
                cleaned_name = re.sub(r'\(.*$', '', cleaned_name).strip()
                obj["Name"] = cleaned_name
            # Remove classrooms starting with specific building codes
            if any(obj.get('Name', '').startswith(prefix) for prefix in remove_bldg_cd):
                return None
            # Remove classrooms with specific tags
            if ("Details" in obj and "Classroom Tag" in obj["Details"]):
                tags = obj["Details"]["Classroom Tag"]
                if "Medical Campus" in tags or any("Fenway Campus" in tag for tag in tags):
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

    # Specify building codes to remove
    remove_bldg_cd = remove_bldg_cd  # Replace with actual building codes as needed

    cleaned_data = clean_data(data)

    with open(classroom_json, 'w', encoding='utf-8') as outfile:
        json.dump(cleaned_data, outfile, indent=4, ensure_ascii=False)
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
def extract_from_classroom():
    with open(classroom_json, 'r', encoding='utf-8') as infile:
        data = json.load(infile)
    capacities = []
    name_capacity_dict = {}
    classroom_mapping = {}
    classroom_id_counter = 0
    def process_classroom_data(obj):
        nonlocal classroom_id_counter
        if isinstance(obj, dict):
            if "AdditionalInfo" in obj and "Capacity" in obj["AdditionalInfo"]:
                try:
                    capacities.append(int(obj["AdditionalInfo"]["Capacity"]))
                except ValueError:
                    pass

            if "Name" in obj and "AdditionalInfo" in obj and "Capacity" in obj["AdditionalInfo"]:
                try:
                    name_capacity_dict[obj["Name"]] = int(obj["AdditionalInfo"]["Capacity"])
                except ValueError:
                    pass

            if "Name" in obj:
                classroom_name = obj["Name"]
                if classroom_name not in classroom_mapping:
                    classroom_mapping[classroom_name] = classroom_id_counter
                    classroom_id_counter += 1

            for value in obj.values():
                process_classroom_data(value)

        elif isinstance(obj, list):
            for item in obj:
                process_classroom_data(item)

    process_classroom_data(data)

    return capacities, name_capacity_dict, classroom_mapping

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
def build_professor_schedule_for_day(day_index, professor_mapping):
    with open(output_file, 'r', encoding='utf-8') as infile:
        data = json.load(infile)

    professor_schedule = {}
    day_mapping = {
        "Mo": 0, "Tu": 1, "We": 2, "Th": 3, "Fr": 4, "Sa": 5, "Su": 6
    }

    def parse_time(time_str):
        time_obj = datetime.strptime(time_str, "%I:%M%p")
        minutes = time_obj.hour * 60 + time_obj.minute
        return minutes // 5

    def find_meetings_for_day(obj):
        if isinstance(obj, dict):
            if "meetings" in obj and "class_availability" in obj:
                capacity = obj["class_availability"].get("class_capacity")
                if capacity is not None:
                    capacity = int(capacity)

                for meeting in obj["meetings"]:
                    if (
                        "instructors" in meeting
                        and "days" in meeting
                        and "meeting_time_start" in meeting
                        and "meeting_time_end" in meeting
                    ):
                        days_str = meeting["days"]
                        days = [
                            day_mapping[days_str[i:i+2]]
                            for i in range(0, len(days_str), 2)
                            if days_str[i:i+2] in day_mapping
                        ]

                        if day_index in days:
                            for instructor in meeting["instructors"]:
                                professor_name = instructor.get("name")
                                professor_id = professor_mapping.get(professor_name)

                                if professor_id is not None:
                                    if professor_id not in professor_schedule:
                                        professor_schedule[professor_id] = []

                                    start_time = parse_time(meeting["meeting_time_start"])
                                    end_time = parse_time(meeting["meeting_time_end"])
                                    professor_schedule[professor_id].append((start_time, end_time, capacity))

            for value in obj.values():
                find_meetings_for_day(value)
        elif isinstance(obj, list):
            for item in obj:
                find_meetings_for_day(item)

    find_meetings_for_day(data)
    return professor_schedule
def allocate_professor_courses_for_day(professor_mapping, classroom_mapping, output_file):
    N = len(professor_mapping)
    M = len(classroom_mapping)
    T_day = 24 * 60 // 5

    professor_courses_monday = np.zeros((N, M, T_day), dtype=int)
    professor_courses_tuesday = np.zeros((N, M, T_day), dtype=int)
    professor_courses_wednesday = np.zeros((N, M, T_day), dtype=int)
    professor_courses_thursday = np.zeros((N, M, T_day), dtype=int)
    professor_courses_friday = np.zeros((N, M, T_day), dtype=int)

    def parse_time_to_5_min_units(time_str):
        time_obj = datetime.strptime(time_str, "%I:%M%p")
        minutes = time_obj.hour * 60 + time_obj.minute
        return minutes // 5

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
                    if professor_id is not None and room_id is not None:
                        days_str = obj.get("days", "")
                        start_time = parse_time_to_5_min_units(obj["meeting_time_start"])
                        end_time = parse_time_to_5_min_units(obj["meeting_time_end"])
                        for day_abbr in [days_str[i:i + 2] for i in range(0, len(days_str), 2)]:
                            if day_abbr == "Mo":
                                for k in range(start_time, end_time):
                                    professor_courses_monday[professor_id][room_id][k] = 1
                            elif day_abbr == "Tu":
                                for k in range(start_time, end_time):
                                    professor_courses_tuesday[professor_id][room_id][k] = 1
                            elif day_abbr == "We":
                                for k in range(start_time, end_time):
                                    professor_courses_wednesday[professor_id][room_id][k] = 1
                            elif day_abbr == "Th":
                                for k in range(start_time, end_time):
                                    professor_courses_thursday[professor_id][room_id][k] = 1
                            elif day_abbr == "Fr":
                                for k in range(start_time, end_time):
                                    professor_courses_friday[professor_id][room_id][k] = 1

    return professor_courses_monday, professor_courses_tuesday, professor_courses_wednesday, professor_courses_thursday, professor_courses_friday

def create_walking_cost_matrix(classroom_mapping, b2b_distance_file):
    # Step 1: Read the 'b2b_walking_distance.csv' file into a pandas DataFrame.
    b2b_distance = pd.read_csv(b2b_distance_file)

    # Step 3: Define the number of classrooms using the size of the classroom mapping.
    num_classrooms = len(classroom_mapping)

    # Initialize the walking_cost matrix with 'inf', denoting initially unknown walking distances.
    walking_cost = np.full((num_classrooms, num_classrooms), np.inf)

    # Step 4: Iterate over each row in the 'b2b_distance' DataFrame to update the walking_cost matrix.
    for _, row in b2b_distance.iterrows():
        building_a, building_b, distance = row['abbreviationA'], row['abbreviationB'], row['distance']
        # Update the matrix for pairs of classrooms, between each pair of buildings.
        for classroom_a, idx_a in classroom_mapping.items():
            for classroom_b, idx_b in classroom_mapping.items():
                if classroom_a.split()[0] == building_a and classroom_b.split()[0] == building_b:
                    # Set the walking distance for the respective indices in the walking_cost matrix.
                    walking_cost[idx_a][idx_b] = distance
                    walking_cost[idx_b][idx_a] = distance

    # Iterate over each possible classroom pairing to set the initial walking costs.
    for i in range(num_classrooms):
        for j in range(num_classrooms):
            # Set the walking cost to 0 for the same room (i.e., no walking required).
            if i == j:
                walking_cost[i][j] = 0
            # Assign a generic cost of 10 for moving within the same building.
            elif list(classroom_mapping.keys())[i].split()[0] == list(classroom_mapping.keys())[j].split()[0]:
                walking_cost[i][j] = 10

    # Step 5: Identify and print positions where walking_cost remains 'inf' (meaning unreachable). If none, confirm.
    inf_positions = np.where(walking_cost == np.inf)
    if inf_positions[0].size > 0:
        for i, j in zip(inf_positions[0], inf_positions[1]):
            print(f"Inf found at walking_cost[{i}][{j}]")

    return walking_cost

def export_schedule_to_pkl(day_name, professor_schedule, professor_courses, file_name):
    data_to_export = {
        f"{day_name.lower()}_professor_schedule": professor_schedule,
        "professor_mapping": professor_mapping,
        "classroom_mapping": classroom_mapping,
        f"professor_courses_{day_name.lower()}": professor_courses,
        "capacities": capacities,
        "walking_cost": walking_cost
    }
    with open(file_name, "wb") as file:
        pickle.dump(data_to_export, file)

def process_solution(file_path):
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
    solution = data[0]
    total_walking_cost = 0.0
    for prof_id, classrooms in solution.items():
        if len(classrooms) <= 1:
            continue
        for i in range(len(classrooms) - 1):
            from_room = classrooms[i]
            to_room = classrooms[i + 1]
            cost = walking_cost[from_room][to_room]
            total_walking_cost += cost

    print(f"Solution walking cost：{total_walking_cost}")
    id_to_professor = {v: k for k, v in professor_mapping.items()}
    id_to_classroom = {v: k for k, v in classroom_mapping.items()}

    formatted_solution = {}

    for prof_id, room_ids in solution.items():
        prof_name = id_to_professor.get(prof_id, f"Unknown Professor {prof_id}")
        formatted_solution[prof_name] = [
            id_to_classroom.get(room_id, f"Unknown Room {room_id}") for room_id in room_ids
        ]

    for prof_name, rooms in formatted_solution.items():
        print(f"{prof_name}: {', '.join(rooms)}")

def print_weekly_walking_cost(professor_courses_monday,
                              professor_courses_tuesday,
                              professor_courses_wednesday,
                              professor_courses_thursday,
                              professor_courses_friday,
                              walking_cost):
    days_data = {
        "Monday": professor_courses_monday,
        "Tuesday": professor_courses_tuesday,
        "Wednesday": professor_courses_wednesday,
        "Thursday": professor_courses_thursday,
        "Friday": professor_courses_friday
    }

    for day_name, professor_courses in days_data.items():
        total_walking_cost = 0.0

        num_professors = len(professor_courses)
        num_classrooms = len(professor_courses[0])
        num_time_slots = len(professor_courses[0][0])

        for prof_index in range(num_professors):
            prev_classroom = None
            for time_slot in range(num_time_slots):
                current_classroom = None
                for classroom_index in range(num_classrooms):
                    if professor_courses[prof_index][classroom_index][time_slot] == 1:
                        current_classroom = classroom_index
                        break
                if current_classroom is not None:
                    if prev_classroom is not None:
                        cost = walking_cost[prev_classroom][current_classroom]
                        total_walking_cost += cost
                    prev_classroom = current_classroom
        print(f"{day_name} cost: {total_walking_cost}")


#################################################################################################################################################################


keys_to_remove = ["additionalLinks", "bookstore", "cfg", "catalog_descr", "materials", "enrollment_information", "reserve_caps", "catalog_descr", "messages", "notes"]
remove_bldg_cd = ["ALB", "CTC", "INS", "SPH", "XBG", "MED", "FAB", "FCB", "FCC", "HAW", "GDS", "FPH", "EVN"]

data_cleaning_course(input_file=input_file, output_file=output_file, keys_to_remove=keys_to_remove, remove_bldg_cd=remove_bldg_cd)
data_cleaning_classroom(remove_bldg_cd)
capacities, name_capacity_dict, classroom_mapping = extract_from_classroom()
professor_mapping = extract_professor_mapping()
professor_courses_monday, professor_courses_tuesday, professor_courses_wednesday, professor_courses_thursday, professor_courses_friday = allocate_professor_courses_for_day(professor_mapping, classroom_mapping, output_file)
monday_professor_schedule = clean_schedule(build_professor_schedule_for_day(0, professor_mapping))
tuesday_professor_schedule = clean_schedule(build_professor_schedule_for_day(1, professor_mapping))
wednesday_professor_schedule = clean_schedule(build_professor_schedule_for_day(2, professor_mapping))
thursday_professor_schedule = clean_schedule(build_professor_schedule_for_day(3, professor_mapping))
friday_professor_schedule = clean_schedule(build_professor_schedule_for_day(4, professor_mapping))
walking_cost = create_walking_cost_matrix(classroom_mapping, b2b_distance)

export_schedule_to_pkl("Monday", monday_professor_schedule, professor_courses_monday, "monday.pkl")
export_schedule_to_pkl("Tuesday", tuesday_professor_schedule, professor_courses_tuesday, "tuesday.pkl")
export_schedule_to_pkl("Wednesday", wednesday_professor_schedule, professor_courses_wednesday, "wednesday.pkl")
export_schedule_to_pkl("Thursday", thursday_professor_schedule, professor_courses_thursday, "thursday.pkl")
export_schedule_to_pkl("Friday", friday_professor_schedule, professor_courses_friday, "friday.pkl")


process_solution('../data/best_solution.pkl')

print_weekly_walking_cost(professor_courses_monday, professor_courses_tuesday, professor_courses_wednesday, professor_courses_thursday, professor_courses_friday, walking_cost)


