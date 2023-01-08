from pprint import pprint
import requests
import json

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
				if key_1 == 'items':
					# print(key_1)
					# print(value_1)
					for val in value_1:
						# print(f'\n{val}\n')
						for key_2, value_2 in val.items():
							if key_2 == 'sizes':
								# print(vii)
								g = []
								j = {}
								for val_2 in value_2:							
									# print(f'\n{val_2}\n')
									for key_3, value_3 in val_2.items():	
										if key_3 == 'height':
											g.append(value_3)
									for key_3, value_3 in val_2.items():
										if key_3 == 'height' and value_3 == max(g):
											j.update(val_2)
								# print(f'\n{j}\n')
						d = []
						for key_4, value_4 in val.items():
							if key_4 == 'likes':
								for key_5, value_5 in value_4.items():
									if key_5 == 'count':
										for key_6, value_6 in j.items():
											if key_6 == 'url':
												d.append(value_6)
										print(f'\n{d}\n')
										to_json = {value_5: d}
										with open('img.txt', 'w') as f:
											json.dump(d, f)
										# with open('img.json') as f:
										# 	print(f.read())
		return d

access_token = ''

vk_client = VkUser(access_token, '5.131')
pprint(vk_client.get_photo())

class YaUploader:
	def __init__(self, token: str):
		self.token = token
	def get_headers(self):
		return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

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
	# def upload(self, file_path: str):
        # """Метод загружает файлы по списку file_list на яндекс диск"""
        # Тут ваша логика
        # Функция может ничего не возвращать


if __name__ == '__main__':
	# Получить путь к загружаемому файлу и токен от пользователя
	disk_file_path = 'img.txt'
	filename = 'img.txt'
	token = ''
	uploader = YaUploader(token)
	result = uploader.upload_file_to_disk(disk_file_path, 'img.txt')

