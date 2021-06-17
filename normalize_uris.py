import requests
import json
#example     dbr : Stuttgart

def normalize_uris(in_data):
    if ':' in in_data:
        in_list = in_data.split(':', 1)
        in_pre = in_list[0]
        if in_pre == 'http' or in_pre == 'https':
            return in_data
        else:
            url = 'http://prefix.cc/' + in_pre + '.file.json'
            r = requests.get(url)
            prefix = json.loads(r.text)[in_pre]
            return prefix + in_list[1]
    else:
        return 'Exception: Input not legal'


if __name__ == "__main__":
    print('This is a script which can normalise a URI') 
    print('Please enter your input:')
    in_data = input()
    print(normalize_uris(in_data))
