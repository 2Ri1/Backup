from pprint import pprint
import requests
import json
import logging

logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w")
logging.debug("A DEBUG Message")
logging.info("An INFO")
logging.warning("A WARNING")
logging.error("An ERROR")
logging.critical("A message of CRITICAL severity")

class YaUploader:
	def __init__(self, token: str):
		self.token = token
	def get_headers(self):
		return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

	def upload_photo_to_disk(self, params_upload):
		yandex_upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload/'
		headers = self.get_headers()
		response = requests.post(url=yandex_upload_url, params=params_upload, headers=headers)
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

class VkUser:
	url = 'https://api.vk.com/method/'
	
	def __init__(self, token, version):
		self.params = {
			'access_token': token,
			'v': version    
        }
	def get_photo(self):
		get_photo_url = self.url + 'photos.get'
		get_photo_params = {'user_ids': '169033595',
							'extended' : 1,	
							'album_id' : 'profile'
							}
		req = requests.get(get_photo_url, params={**self.params, **get_photo_params}).json()
		for key, value in req.items():			
			for key_1, value_1 in value.items():
				d = []
				if key_1 == 'items':
					for val in value_1:
						for key_2, value_2 in val.items():
							if key_2 == 'sizes':
								g = []
								j = {}
								for val_2 in value_2:							
									for key_3, value_3 in val_2.items():	
										if key_3 == 'height':
											g.append(value_3)
									for key_3, value_3 in val_2.items():
										if key_3 == 'height' and value_3 == max(g):
											j.update(val_2)
						for key_4, value_4 in val.items():
							if key_4 == 'likes':
								for key_5, value_5 in value_4.items():
									if key_5 == 'count':
										value_5 = str(value_5)
										path = (value_5 +'.jpg')
										for key_6, value_6 in j.items():
											if key_6 == 'url':
												data = value_6
											elif key_6 == 'height':
												height = str(value_6)
											elif key_6 == 'width':
												width = str(value_6)
										size = height + '*' + width
										photo_information = {"file_name": path, "size": size}
										d.append(photo_information)										
										params_upload = {'path': path, 'url': data}
										if __name__ == '__main__':
											token = ''
											uploader = YaUploader(token)
											result = uploader.upload_photo_to_disk(params_upload)
											
				with open('list_of_photos.json', 'w') as f:
					f.write(json.dumps(d))
				disk_file_path = 'list_of_photos.json'
				filename = 'list_of_photos.json'
				token = ''								
				uploader = YaUploader(token)
				res = uploader.upload_file_to_disk(disk_file_path, 'list_of_photos.json')

		return 'Success'

access_token = ''

vk_client = VkUser(access_token, '5.131')
pprint(vk_client.get_photo())