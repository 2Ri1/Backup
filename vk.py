import requests
import configparser
from ya_disk import YaUploader
from create_json import create_json
from datetime import datetime


class VkUser:
	
	url = 'https://api.vk.com/method/'
	
	def __init__(self, token, version):
		self.params = {
			'access_token': token,
			'v': version
        }
		
	def user_id(self, screen_name):
		url = self.url + 'users.get'
		params = {
			'user_ids' : screen_name,
			'fields' : 'id',
			'name_case' : 'nom'
		}

		req = requests.get(url, params={**self.params, **params}).json()
		for key, value in req.items():	
			for elem in value:
				for key_2, value_2 in elem.items():
					if key_2 == "id":
						user_ids = value_2
					
		return user_ids
		
	def get_photo(self, user_id, count):
		get_photo_url = self.url + 'photos.get'
		get_photo_params = {
				            'owner_id': user_id,							
							'extended' : 1,	
							'album_id' : 'profile',
							'count' : count
		}
			
		req = requests.get(get_photo_url, params={**self.params, **get_photo_params}).json()

		for key, value in req.items():			
			for key_1, value_1 in value.items():
				photo_info_list = []	
				like_count = []
				if key_1 == 'items':
					for val in value_1:
						for key_2, value_2 in val.items():
							if key_2 == 'date':
								date_photo = value_2
								dt_object = datetime.fromtimestamp(date_photo)
							if key_2 == 'sizes':
								list_with_sizes = []
								photo_info = {}
								for val_2 in value_2:	
									for key_3, value_3 in val_2.items():
										if key_3 == 'height':
											list_with_sizes.append(value_3)
									for key_3, value_3 in val_2.items():
										if key_3 == 'height' and value_3 == max(list_with_sizes):
											photo_info.update(val_2)
						for key_4, value_4 in val.items():
							if key_4 == 'likes':
								for key_5, value_5 in value_4.items():
									if key_5 == 'count':												
										for key_6, value_6 in photo_info.items():
											if key_6 == 'url':
												data = value_6
											elif key_6 == 'height':
												height = str(value_6)
											elif key_6 == 'width':
												width = str(value_6)
										size = height + '*' + width
										count = set()
										name = str(value_5) + '.jpg '
										like_count.append(value_5)
										dup = [x for x in like_count if x in count or (count.add(x) or False)]
								for number in dup:
									like_count.remove(number)
									name += str(dt_object)
	
								photo_information = {"file_name": name, "size": size}
								photo_info_list.append(photo_information)	
								params_upload = {'path': name, 'url': data}
								config = configparser.ConfigParser()   	
								config.read("token.ini")
								uploader = YaUploader(config["Yandex"]["token"])
								result = uploader.upload_photo_to_disk(params_upload,data, name)

				create_json(photo_info_list)
				disk_file_path = 'list_of_photos.json'
				filename = 'list_of_photos.json'
				config = configparser.ConfigParser()   	
				config.read("token.ini")
				uploader = YaUploader(config["Yandex"]["token"])
				res = uploader.upload_file_to_disk(disk_file_path, filename)
				file_upload_path = 'photo'
				res_2 = uploader.create_file(file_upload_path)
			
		return 'Success'
