# Software Fair Guide

A display of all the projects in Stanford's CS 210 and 194! Check out the link [here](https://cs210.github.io/SoftwareGuide/)!

## To Run

### Frontend

First, install all necessary dependencies:
```bash
npm run install
```

Next, run the development server:
```bash
npm run dev
```

### Backend Scripts

First, make a copy of the Google Form found [here](https://docs.google.com/forms/d/e/1FAIpQLScfF8IDrwYKKic6A2kVAI_DdzyTwEtYoIVHfNsN-zVDyOiH9A/viewform) for the corresponding year. Then, after you have all of the responses, download the `.csv` file and name it `input.csv`. Finally, feel free to edit `categories.csv` -- to include and/or remove categories for projects -- as well as edit `layout.csv`.

Finally, once you're all ready, run the main script to generate the necessary data:
```bash
python3 software_guide_generator.py
```

## Contribution

The CI/CD pipeline is configured to push automatically to GitHub pages upon push.

## Old Notes

### How to change teaminfo
Note that all of the team information can be found team_info.csv inside of the update_software_guide folder.
Here you can change the table each team is assigned to and any other relevant info. To assign two teams to
the same table you can simply append .a or .b to that teams table number. The fill color for each team will be automatically 
set to the AI category color if it is an AI-relevant project; otherwise, it will default to the first category color.

### How to add categories
If you would like to add categories, edit the categories.csv file within the update_software_guide folder. Add
a name and associated tailwind UI color.

