import json

def export_results(video_path, emotion_percentages, poema, audio_path):
    data = {
        "video_path": video_path,
        "emotion_percentages": emotion_percentages,
        "poema": poema,
        "audio_path": audio_path
    }
    with open('results.json', 'a', encoding='utf-8') as f:
        f.write(json.dumps(data, indent=4))
        f.write('\n')
