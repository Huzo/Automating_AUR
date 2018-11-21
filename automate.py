from lxml import html
import urllib.request
import subprocess

packagename = 'dropbox'
response = urllib.request.urlopen("https://aur.archlinux.org/packages/" + packagename + '/').read()
source = html.fromstring(response)
all_links = source.xpath('//ul[@id="pkgdepslist"]/li/a/@href')
official_links = [link for link in all_links if link.startswith('https://www.archlinux.org/packages/?q=')]
aur_links = ['https://aur.archlinux.org' + link for link in all_links if not link.startswith('https')]

official_dependencies = [i.replace('https://www.archlinux.org/packages/?q=', '') for i in official_links]
aur_dependencies = [i.replace('https://aur.archlinux.org/packages/', '') for i in aur_links]

installed_dependencies = {'official': [], "aur": []}
not_installed_dependencies = {'official': [], "aur": []}

print("\nChecking dependencies of " + packagename + '...\n')

for i in range(len(official_dependencies)):
    if(subprocess.call('pacman ' + '-Qi ' + official_dependencies[i] ,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0):
    	installed_dependencies['official'].append(official_dependencies[i])
    else:
    	not_installed_dependencies['official'].append(official_dependencies[i])

for i in range(len(aur_dependencies)):
    if(subprocess.call('pacman ' + '-Qi ' + aur_dependencies[i] ,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0):
    	installed_dependencies['aur'].append(aur_dependencies[i])
    else:
    	not_installed_dependencies['aur'].append(aur_dependencies[i])
print("*************")
for i in range(len(installed_dependencies['official'])):
	print("Dependency " + installed_dependencies['official'][i] + " is already installed")
for i in range(len(installed_dependencies['aur'])):
	print("Dependency " + installed_dependencies['aur'][i] + " is already installed")
print("*************")
for i in range(len(not_installed_dependencies['official'])):
	print("Dependency " + not_installed_dependencies['official'][i] + " is not installed")
for i in range(len(not_installed_dependencies['aur'])):
	print("Dependency " + not_installed_dependencies['aur'][i] + " is not installed")

def aur_git_install(package_name, is_dep = False):
	git_link = "https://aur.archlinux.org/" + package_name + ".git"
	
	subprocess.call('git clone ' + git_link, shell=True)
	subprocess.call('cd ' + package_name, shell=True)
	subprocess.call('ls',shell=True)
	if(is_dep):
		subprocess.call('makepkg PKGBUILD -i --asdeps',shell=True, cwd= package_name)
	else:
		subprocess.call('makepkg package_name/PKGBUILD -i',shell=True, cwd= package_name)
	subprocess.call('rm -rf ' + package_name, shell=True)

# official
for i in range(len(not_installed_dependencies['official'])):
	package_name = not_installed_dependencies['aur'][i]
	subprocess.call('yes | sudo pacman -S ' + package_name, shell=True)

# aur 
for i in range(len(not_installed_dependencies['aur'])):
	aur_git_install(not_installed_dependencies['aur'][i], is_dep = True)

# final install
aur_git_install(packagename)
