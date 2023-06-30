import json

def export_results(video_path, emotion_percentages, poema, audio_path):
    data = {
        "video_path": video_path,
        "emotion_percentages": emotion_percentages,
        "poema": poema,
        "audio_path": audio_path
    }
    with open('results.json', 'w') as f:
        json.dump(data, f, indent=4)