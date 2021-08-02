import requests
import json

response = requests.get(
        'https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&site=stackoverflow'
            )

#print(response) # status only 400 if success

# json dumps is used to force double quotes on output
#formattedJson = json.dumps(response.json())
#print(formattedJson) # spits out entire json data
#print(response.json()['items']) # filter to only show ['items']

# f = open("response.json","w+")
# f.write(formattedJson)
# f.close()

for question in response.json()['items']:
    if question['is_answered'] == 0:
        print(question['title'])
        print(question['link'])
    else:
        print("skipped")
    print()
