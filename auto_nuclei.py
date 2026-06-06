'''Simple httpx and nuclei automation tool'''
import subprocess
import sys

def main(subdomains):
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
			['httpx', '-l', subdomains, '-o', 'livehosts.txt', '-silent'])
	except FileNotFoundError:
		print(f'[-] Error: httpx is not installed or not on PATH')
		sys.exit(1)


	try:
		with open('livehosts.txt', 'r') as l:
			livehosts: list[str] = [line.strip() for line in l if line.strip()]
		print(f"[+] Found {len(livehosts)} live hosts")
	except FileNotFoundError:
		print(f'[-] No live hosts found!')
	print(f'[*] Running nuclei...')
	try:
		subprocess.run(
			['nuclei', '-l', 'livehosts.txt',
			'-o', 'nuclei_results.txt'])
	except FileNotFoundError:
		print(f'[-] Error: nuclei not installed or not in PATH')
		sys.exit(1)

	print(f'[+] Done! You can check results in nuclei_results.txt')

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print(f'Usage: python auto_nuclei.py <your_subdomains_file.txt>')
		sys.exit(1)
	main(sys.argv[1]) # a small change
