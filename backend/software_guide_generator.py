import csv
import json
import ast

# Global params for configuring output
DEFAULT_FILL_COLOR = "#ffffff"
CLICK_FILL_COLOR = "#000000"

# Convert the raw Google Form CSV into the updated CSV.
def convert_csv(input_path, output_path):
    with open(input_path, mode='r', encoding='utf-8') as infile:
        reader = list(csv.DictReader(infile))
        
        # First pass: count 194 teams
        num_194_teams = sum(1 for row in reader if '194' in row['Which course number for your team (you)'])
        table_counter_194 = 1
        table_counter_210 = 23  # Right after the last 194 table
        is_shared_table = False  # Flag to track if we're in a shared table

        with open(output_path, mode='w', newline='', encoding='utf-8') as outfile:
            fieldnames = ['team', 'table_num', 'members', 'description', 'categories', 'has_ai']
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                course = row['Which course number for your team (you)']
                team = row['Team Name'].strip()
                members = row['Names of individuals on the team'].strip().replace(';', ',')
                description = row['Please provide a brief description of your project as you wish it to appear in the Software Fair Program Guide'].strip()
                categories = row['Please check any genres to which you believe your project belongs'].strip()
                has_ai = row['Is your project AI-related?'].strip()

                if '194' in course:
                    if 12 <= table_counter_194 <= 19:
                        if not is_shared_table:
                            table_num = f"{table_counter_194}.a"
                            is_shared_table = True
                        else:
                            table_num = f"{table_counter_194}.b"
                            is_shared_table = False
                            table_counter_194 += 1
                    else:
                        table_num = str(table_counter_194)
                        table_counter_194 += 1
                else:  # assume 210
                    table_num = str(table_counter_210)
                    table_counter_210 += 1

                writer.writerow({
                    'team': team,
                    'table_num': table_num,
                    'members': members,
                    'description': description,
                    'categories': categories,
                    'has_ai': has_ai
                })

# Function to safely convert string to list
def convert_str_to_list(str_list):
    try:
        return ast.literal_eval(str_list)
    except (ValueError, SyntaxError):
        return []
    
def split_coords(coords):
    if len(coords) != 8:
        print(len(coords))
        raise ValueError("Expected 8 coordinates representing a rectangle.")

    # Extract coordinates
    x1, y1 = coords[0], coords[1]
    x2, y2 = coords[2], coords[3]
    x3, y3 = coords[4], coords[5]
    x4, y4 = coords[6], coords[7]

    midpoint_x_bot = (x1 + x2) // 2
    midpoint_y_bot = (y1 + y2) // 2
    midpoint_x_top = (x3 + x4) // 2
    midpoint_y_top = (y3 + y4) // 2

    # First half rectangle (left)
    first_half = [x1, y1, midpoint_x_bot, midpoint_y_bot, midpoint_x_top, midpoint_y_top, x4, y4]

    # Second half rectangle (right)
    second_half = [midpoint_x_bot, midpoint_y_bot, x2, y2, x3, y3, midpoint_x_top, midpoint_y_top]

    return first_half, second_half

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
            first_half, second_half = split_coords(coords)
            table_coords[table_num] = {
                "full": convert_str_to_list(row['coords']),
                "half-a": first_half,
                "half-b": second_half
            }

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

    with open(team_file_path, mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            table_num_label = row["table_num"]
            table_space = "full"

            if "a" in table_num_label:
                table_space = "half-a"
            if "b" in table_num_label:
                table_space = "half-b"

            table_num = int(table_num_label.split(".")[0])

            # Code that sets preference for revealing projects with AI
            ai_related = row['has_ai']
            main_category = row["categories"].split(", ")[0]
            if (ai_related == "Yes"):
                main_category = "AI"
                row["categories"]+=", AI"

            if main_category not in category_data:
                raise LookupError(f"Main Category: {main_category} not found in Category Data: ")

            # If table coords exist we generate data
            if table_num in table_coords:
                pre_fill_color = category_data.get(main_category, {}).get('hex_color', DEFAULT_FILL_COLOR)
                section_num = category_data.get(main_category, {}).get('section_number', 0)
                image_map_areas.append(json_area(section_num, row["table_num"], row['team'], table_coords[table_num][table_space], pre_fill_color))
                team_info_ls.append(generate_team_info(row, section_num))
            else:
                raise LookupError(f"Error: Table number {table_num} not specified in layout")

    # Write the JSON output
    with open("../src/app/components/areas.json", 'w') as file:
        json.dump(image_map_areas, file, indent=4)

    with open("../src/app/components/teams.json", 'w') as file:
        json.dump(team_info_ls, file, indent=4)

def json_area(section_num, table_num_label, team_name, coords, pre_fill_color):
    """
        Generates json area object that is used by the react image mapper 
    """
    return {
        'name': str(section_num) + "-" + team_name + "-" + table_num_label,
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
        "teamNum": team_data['table_num'],
        "description": team_data['description'],
        "categories": team_data['categories'].split(", "),
        "teamMembers": team_data['members'],
        "sectionNum": section_num
    }

    return team_info

if __name__ == "__main__":
    convert_csv("data/input.csv", "data/team_info.csv")
    generate_category_map_from_csv("data/categories.csv")
    process_teams_and_generate_json("data/team_info.csv", "data/layout.csv", "data/categories.csv")