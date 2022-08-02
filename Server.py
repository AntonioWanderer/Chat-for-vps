import socket

UDP_MAX_SIZE = 65535

hist = open("Msg_history.txt", 'w')
hist.close()

def listen(host: str = '146.19.247.186', port: int = 3000):
	hist = open("Msg_history.txt", 'a')
	pseudonims = {}
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind((host, port))
	print(f'Listening at {host}:{port}')
	members = []
	while True:
		msg, addr = s.recvfrom(UDP_MAX_SIZE)
		
		if addr not in members:
			members.append(addr)
			
		if not msg:
			continue
		client_id = addr[1]
		
		if msg.decode('ascii') == '__join':
			print(f'Client {client_id} joined chat')
			hist = open("Msg_history.txt", 'a')
			hist.write(f'Client {client_id} joined chat')
			hist.close()
			continue
		
		msg = f'client{client_id}: {msg.decode("ascii")}'
		hist = open("Msg_history.txt", 'a')
		hist.write(msg+"\n")
		hist.close()
		for member in members:
			if member == addr:
				continue
			s.sendto(msg.encode('ascii'), member)
			
listen()
