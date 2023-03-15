from scenes import scenes

def main(event, context):
    user_id = None
    scene = 0
    if 'request' in event and \
            'original_utterance' in event['request'] \
            and len(event['request']['original_utterance']) > 0:
        req_text = event['request']['original_utterance']
        state = event.get('state')
        if state:
            #user_id = int(state.get('user').get('value')) if state.get('user') is not None else None
            scene = int(state.get('session').get('value')) if state.get('session') is not None else None
        answer = process_request(scene, req_text)
    else:
        answer = process_request(scene)
    (text, tts, session_state, end_session) = answer
    return build_response(event, text, tts, end_session, user_id, session_state)

def process_request(scene, text=None):
    scene = scenes.load_scene(scene)
    scene_text = scene['text']
    tts = scene['tts']
    next_scenes = scene['next_scenes']
    is_end = scene['end']

    if text is None :
        return (scene_text, tts, next_scenes['other'], is_end)
    next_scene = next_scenes.get(text.lower())
    if next_scene is None:
        return (scene_text, tts, next_scenes['other'], is_end)
    return (scene_text, tts, next_scene, is_end)


def build_response(event, text, tts = None, end_session = False, user_id = None, session_state = 0):
    if tts is None:
        tts = text

    if end_session:
        end_session = 'true'
    else:
        end_session = 'false'

    data = {
        'version': event['version'],
        'session': event['session'],
        'response': {
            'text': text,
            'tts': tts,
            'end_session': end_session,
        },
        "session_state": {
            "value": session_state,
        },
    }
    if user_id:
        data['user_state_update'] = {
            "value": user_id,
        }
    return data

