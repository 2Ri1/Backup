import json

def create_json(dobavit):
	with open('list_of_photos.json', 'w') as f:
		f.write(json.dumps(dobavit))