import csv
import json
import ast

# Global params for configuring output
DEFAULT_FILL_COLOR = "#ffffff"
CLICK_FILL_COLOR = "#000000"

# Function to safely convert string to list
def convert_str_to_list(str_list):
    try:
        return ast.literal_eval(str_list)
    except (ValueError, SyntaxError):
        return []

def csvlayout_to_dict(csv_file_path):
    """
    Reads a CSV file with table coords and returns them as a dictionary
    """
    table_coords = {}
    with open(csv_file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            table_num = int(row['table_num'])
            coords = convert_str_to_list(row['coords'])
            table_coords[table_num] = coords

    return table_coords

def generate_category_map_from_csv(csv_path):
    """
        Generates the categoryMap.js component by using the values listed in the .csv file
    """
    with open(csv_path, mode="r") as csvfile:
        reader = csv.DictReader(csvfile)
        section_counter = 0
        category_data = {}
        for row in reader:
            category_data[row["category"]] = {
            "color": row["color"],
            "hex_color": row["hex_color"],
            "section_number": section_counter
            }
            section_counter += 1

        js_content = "const categoryMap = {\n"
        for category, info in category_data.items():
            js_content += f"  \"{category}\": {{\n"
            js_content += f"    \"section\": \"{info['section_number']}\",\n"
            js_content += f"    \"color\": \"bg-{info['color']}\"\n"
            js_content += f"  }},\n"
        js_content = js_content.rstrip(",\n") + "\n};\n\nexport default categoryMap;"


    with open("../src/app/components/categoryMap.js", mode="w") as file:
        file.write(js_content) 

def generate_category_dict_from_csv(csv_path):
    """
        Same code as generate_category_map_from_csv however values are loaded into a python dict
    """
    section_counter = 0;
    with open(csv_path, mode="r") as csvfile:
        reader = csv.DictReader(csvfile)
        category_data = {}
        for row in reader:
            category_data[row["category"]] = {
            "color": row["color"],
            "hex_color": row["hex_color"],
            "section_number": section_counter
            }
            section_counter += 1

    return category_data

def process_teams_and_generate_json(team_file_path, layout_file_path, categories_file_path):

    # Load table coordinates
    table_coords = csvlayout_to_dict(layout_file_path)
    
    # Load category data
    category_data = generate_category_dict_from_csv(categories_file_path)
    
    # Prepare to accumulate team info for the text file and area data for JSON
    team_info_ls = []
    image_map_areas = []

    with open(team_file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            main_category = row["main_category"]
            table_num = int(row["table_num"])

            if main_category not in category_data:
                raise LookupError(f"Main Category: {main_category} not found in Category Data: ")

            # If table coords exist we generate data
            if table_num in table_coords:
                pre_fill_color = category_data.get(main_category, {}).get('hex_color', DEFAULT_FILL_COLOR)
                section_num = category_data.get(main_category, {}).get('section_number', 0)
                image_map_areas.append(json_area(section_num, table_num, table_coords[table_num], pre_fill_color))
                team_info_ls.append(generate_team_info(row, section_num))
            else:
                raise LookupError(f"Error: Table number {table_num} not specified in layout")

    # Write the JSON output
    with open("../src/app/components/areas.json", 'w') as file:
        json.dump(image_map_areas, file, indent=4)

    with open("../src/app/components/teams.json", 'w') as file:
        json.dump(team_info_ls, file, indent=4)

def json_area(section_num, table_num, coords, pre_fill_color):
    """
        Generates json area object that is used by the react image mapper 
    """
    return {
        'name': str(section_num) + "-" + str(table_num),
        "shape": "poly",
        "coords": coords, 
        'preFillColor': pre_fill_color,
        'fillColor': CLICK_FILL_COLOR
    }

def generate_team_info(team_data, section_num):
    """
        This creates the info for each team which is populated into the TeamInfo component
    """

    team_info = {
        "teamName": team_data['team'],
        "teamNum": int(team_data['table_num']),
        "description": team_data['description'],
        "categories": team_data['categories'].split(", "),
        "mainCategory": team_data["main_category"],
        "teamMembers": team_data['members'],
        "sectionNum": section_num
    }

    return team_info

generate_category_map_from_csv("categories.csv")
process_teams_and_generate_json("team_info.csv", "layout.csv", "categories.csv")