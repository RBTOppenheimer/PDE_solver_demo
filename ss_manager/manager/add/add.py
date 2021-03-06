import os
import sys
import json
import socket
sys.path.append("../")
from util.table import table
from util.proxy import proxy

configFile = open("config.json")
config = json.load(configFile)
data_path = "../../database/database.txt"
new_file = config["file"]
l_addr = config["local_ip"]
l_port = config["local_port"]


# Database modification
add_list = []
database = table()
database.get_ctx_fromfile(data_path)
print("original database: ")
database.export()
source = table()
source.get_ctx_fromfile(new_file)
print("new data: ")
source.export()
d_uuid_list = database.get_uuid_list()
s_uuid_list = source.get_uuid_list()
ld = len(d_uuid_list)
ls = len(s_uuid_list)
for i in range(ls):
	if s_uuid_list[i] in d_uuid_list:
		continue
	else:
		database.ctx.append(source.ctx[i])
		database.num += 1
		add_list.append(source.ctx[i])
database.write_tofile(data_path)
#print("Add new data to database, get: ")
#database.export()

# Remote server modification
print("---------------")

for x in add_list:
	remote_addr = x.serverIP
	remote_port = x.serverPort
	passwd = x.passwd
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind((l_addr, l_port))
	sock.connect((remote_addr, 6001))
	sock.send(b"ping")
	print(sock.recv(1506))
	cmd = 'add: {\"server_port\": '+str(remote_port)+', \"password\": \"'+passwd+'\"}'
	print(cmd)
	content = bytes(cmd, encoding="utf8")
	print(content)
	sock.send(content)
	sock.send(content)
	sock.send(content)
	sock.send(content)
	print(sock.recv(1506))




