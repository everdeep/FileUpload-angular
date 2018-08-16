import json


arr = [{'word': 'potato', 'type': 'noun'}, {'word': 'tomato','type': 'noun'}]

with open ('dict.dat', 'w') as f:
    print(json.dumps(arr))
    # json.dump(dict, f)
