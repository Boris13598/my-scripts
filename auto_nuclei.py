'''Simple httpx and nuclei automation tool'''
import subprocess
import sys
from datetime import datetime

def main(subdomains):
	timestamp: str = datetime.now().strftime("%Y%m%d_%H%M%S") #Timestamps for files
	live_file: str = f"livehosts_{timestamp}.txt"
	nuclei_file: str = f"nuclei_results_{timestamp}.txt"

	#Check if subdomains file is here
	try:
		with open(subdomains, 'r') as f:
			subd: list[str] = [line.strip() for line in f if line.strip()]
	except FileNotFoundError:
		print(f"[-] Error: {subdomains} not found!")
		sys.exit(1)
	print(f'[+] Loaded {len(subd)} subdomains')

	print(f'[*] Running httpx to find live hosts...')
	try:
		subprocess.run(
			['httpx', '-l', subdomains, '-o', live_file, '-silent'])
	except FileNotFoundError:
		print(f'[-] Error: httpx is not installed or not on PATH')
		sys.exit(1)


	try:
		with open(live_file, 'r') as l:
			livehosts: list[str] = [line.strip() for line in l if line.strip()]
		print(f"[+] Found {len(livehosts)} live hosts")
	except FileNotFoundError:
		print(f'[-] No live hosts found!')


	print(f'[*] Running nuclei...')
	try:
		subprocess.run(
			['nuclei', '-l', live_file,
			'-o', nuclei_file])
	except FileNotFoundError:
		print(f'[-] Error: nuclei not installed or not in PATH')
		sys.exit(1)

	print(f'[+] Done! You can check results in {nuclei_file}')

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print(f'Usage: python auto_nuclei.py <your_subdomains_file.txt>')
		sys.exit(1)
	main(sys.argv[1])
