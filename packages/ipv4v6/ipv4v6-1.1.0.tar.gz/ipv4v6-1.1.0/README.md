# Thank you for supporting!
* Function *get_ip()* is used to get your ipv4 address including host and port.
	```
	from ipv4v6 import get_ip
	print(get_ip()) #It'll print something like 117.143.170.80:2653
	```
* Function *get_ipv4()* is used to get your ipv4 address including only host.
	```
	from ipv4v6 import get_ipv4
	print(get_ipv4()) #It'll print something like 117.143.170.80
	```

  **(Tips : If you just want to get ipv4 address, *get_ip()* is a better choice because it's faster than *get_ipv4*)**
 * Function *get_ipv6()* is used to get your ipv6 address including only host.
	 ```
	 from ipv4v6 import get_ipv6
	 print(get_ipv6())
	 #It'll print something like 2409:8a1e:6e81:4280:6456:3051:4f3f:1965
	 ```
 * Function *ip_tuple()* returns a tuple which contains the host and the port of your ipv4 address.
   **(Tips : It can be given to *socket.connect()* as parameter)**
   ```
   from socket import *
   from ipv4v6 import ip_tuple
   sock=socket(AF_INET,SOCK_STREAM)
   sock.connect(ip_tuple())
   ```
* Function *get_ipv4_location()* and *get_ipv6_location* returns the location of your ip address. 
   ```
   from ipv4v6 import get_ipv4_location
   print(get_ipv4_location()) #It'll print the location
   ```