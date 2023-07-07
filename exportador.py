import json, os
from jinja2 import Environment, FileSystemLoader

def render_template():
    # Load the JSON file
    with open('results.json') as json_file:
        videos = json.load(json_file)

    # Load the Jinja2 environment and template
    env = Environment(loader=FileSystemLoader(r'C:\Users\lords\Downloads\testingartweb'))
    template = env.get_template('template.html')

    # Render the template with the videos
    output = template.render(videos=videos)

    # Write the result to a new HTML file
    with open(r'C:\Users\lords\Downloads\testingartweb\index.html', 'w', encoding="utf-8") as f:
        f.write(output)

    # Git add, commit, push
    os.system(r'cd C:\Users\lords\Downloads\testingartweb')
    os.system('git add .')
    os.system('git commit -m "Update"')
    os.system('git push')


def export_results(video_path, emotion_percentages, poema, audio_path):
    data = {
        "video_path": f"https://espejomagico-708d7.web.app/{video_path}",
        "emotion_percentages": emotion_percentages,
        "poema": poema,
        "audio_path": f"https://espejomagico-708d7.web.app/{audio_path}"
    }
    try:
        with open('results.json', 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        existing_data = []
    existing_data.append(data)
    with open('results.json', 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, indent=4)
