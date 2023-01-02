# trickmyinstall
Python Script for setting up my custom Pop! OS, Fedora, and Manjaro configurations.

Install:  git clone git@github.com:linuxg33k76/trickmyinstall.git 

Note!
- Install pyyaml and tqdm packages.  *pip3 install pyyaml tqdm*

OR

https://github.com/linuxg33k76/trickmyinstall.git

data/*.yaml contains the setup files for adding commands or updating packages.
- Edit these files to install your favorite packages or editing your favorite files.
- Lines in YAML files will be executed in order
- Does require sudo privileges to use (will prompt)
- REQUIRES Python3 packages: pyyaml & tqdm <-- IMPORTANT!!!

Usage:  trickmyinstall.py --help (for list of commands)

