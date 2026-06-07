#!/usr/bin/env python3

'''Simple httpx and nuclei automation tool'''
import subprocess
import sys
from datetime import datetime
import argparse

def main(subdomains, severity, threads, concurrency):
	timestamp: str = datetime.now().strftime("%m%d_%H%M%S") #Timestamps for files
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

	#Run httpx
	print(f'[*] Running httpx with {threads} threads to find live hosts...')
	try:
		result = subprocess.run(
			['httpx', '-l', subdomains, '-o', live_file, '-silent', '-threads', threads],
			 capture_output=True)
		if result.returncode != 0:
			print(f'[-] Warning: httpx exited with the code {result.returncode}')
			print(f'[-] Error: {result.stderr.decode()}')
	except FileNotFoundError:
		print(f'[-] Error: httpx is not installed or not on PATH')
		sys.exit(1)


	try:
		with open(live_file, 'r') as l:
			livehosts: list[str] = [line.strip() for line in l if line.strip()]
		print(f"[+] Found {len(livehosts)} live hosts")
	except FileNotFoundError:
		print(f'[-] No live hosts found!')
		sys.exit(1)

	#Run nuclei
	print(f'[*] Running nuclei with {severity} severity...')
	try:
		cmd = ['nuclei', '-l', live_file,
			'-o', nuclei_file]
		if severity:
			cmd.extend(['-severity', severity])
		if concurrency:
			cmd.extend(['-c', str(concurrency)])
		result = subprocess.run(
			cmd, capture_output=True,
			text=True)
		if result.returncode != 0:
			print(f'[-] Warning: nuclei exited with code {result.returncode}')
	except FileNotFoundError:
		print(f'[-] Error: nuclei not installed or not in PATH')
		sys.exit(1)

	print(f'[+] Done! You can check results in {nuclei_file}')

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="My scanning tool")
	parser.add_argument('file', help="Subdomains file")
	parser.add_argument('-s', '--severity', 
				choices=['info', 'medium', 'low', 'high', 'critical'],
				help="Filter by severity (info, low, medium, high, critical)")
	parser.add_argument('-t', '--threads', type=str, default='100', help="Number of threads for httpx")
	parser.add_argument('-c', '--concurrency', type=int, default=50, help="Nuclei control concurrency")

	args = parser.parse_args()
	main(args.file, args.severity, args.threads, args.concurrency)
