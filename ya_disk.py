import requests
from pprint import pprint


class YaUploader:
	
	def __init__(self, token: str):
		self.token = token
	def get_headers(self):
		return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

	def create_file(self, file_upload_path):
		url = 'https://cloud-api.yandex.net/v1/disk/resources'
		headers = self.get_headers()
		requests.put(url=f'{url}?path={file_upload_path}', headers=headers)
				
	def upload_photo_to_disk(self, params_upload, data, name):
		uploud_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload/'
		headers = self.get_headers()
		v = name
		path = 'photo'
		params = {
                    "path": f'/{path}/{v}',
                    "url": data,
                    "overwrite": "true",
                }
		response = requests.post(url=uploud_url, params=params, headers=headers)
		return response.json()
		
	def get_files_list(self):
		files_url = 'https://cloud-api.yandex.net/v1/disk/resources/files'
		headers = self.get_headers()
		response = requests.get(files_url, headers=headers)
		return response.json()
		
	def _get_upload_link(self, disk_file_path):
		upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
		headers = self.get_headers()
		params = {"path": disk_file_path, "overwrite": "true"}
		response = requests.get(upload_url, headers=headers, params=params)
		pprint(response.json())
		return response.json()

	def upload_file_to_disk(self, disk_file_path, filename):
		href = self._get_upload_link(disk_file_path=disk_file_path).get("href", "")
		response = requests.put(href, data=open(filename, 'rb'))
		response.raise_for_status()
		if response.status_code == 201:
			print("Success")