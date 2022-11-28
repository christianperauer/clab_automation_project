from Exscript.util.interact import read_login
from Exscript.protocols import SSH2


account = read_login()
conn = SSH2()                       
conn.connect('172.20.20.2')     
conn.login(account)  


while True:
    command = raw_input('cli: ')
    if command == 'q': break
    conn.execute(command)
    print(conn.response)



conn.send('quit\r')               
conn.close() 