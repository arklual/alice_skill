import json

def load_scene(scene_id):
    with open(f'scenes/{scene_id}.json') as f:
        scene = json.load(f)
        if scene['tts'] == '':
            scene['tts'] = scene['text']
        return scene