from data.Node import Node
from data.Node_Source import Node_Source

import json

with open('data/data.json', 'r') as file:
    data = json.load(file)

print(data)

for node in data["nodes"]:
    print(node)



# json_data = json.dumps(data)
