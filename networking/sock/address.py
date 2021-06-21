from requests import get

def __initserverhost():
	ip = get('https://api.ipify.org').text
	return ip
