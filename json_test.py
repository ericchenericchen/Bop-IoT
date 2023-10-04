import json

# json library: https://docs.python.org/3.5/library/json.html

person = {
    'name': 'Tommy Trojan',
    'email': 'tommy@usc.edu',
    'phone': '213-740-2311',
    'nicknames': [
        'Tommy T',
        'Spirit of Troy',
    ],
}

print(type(person))
print(person)

person_json = json.dumps(person)
print(person_json)

# TODO: What type is person_json?
# person_json is a json formatted string; json.dumps() always returns strings
print(type(person_json))

# TODO: Pretty printing
pretty_person_json = json.dumps(person, sort_keys=False, indent=4)
print(pretty_person_json)
#If we do sort_keys=True the order of the json keys are sorted alphabetically, and if we don't it maintains its original position.