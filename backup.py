from pprint import pprint
import logging
from vk import VkUser


logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w")
logging.debug("A DEBUG Message")
logging.info("An INFO")
logging.warning("A WARNING")
logging.error("An ERROR")
logging.critical("A message of CRITICAL severity")

if __name__ == '__main__':
	
	print('Введите в поле свой id или 0, если вы хотите ввести своё screen_name ')
	id = int(input('Введите id пользователя: '))
	screen_name = str(input('Введите screen_name пользователя: '))
	count = int(input('Введите желаемое количество фотографий: '))	
	access_token = ''
	vk_client = VkUser(access_token, '5.131')
	if id == 0:		
		user_id = vk_client.user_id(screen_name)
		print(user_id)
		pprint(vk_client.get_photo(user_id, count))
	else:
		user_id = id
		pprint(vk_client.get_photo(user_id, count))