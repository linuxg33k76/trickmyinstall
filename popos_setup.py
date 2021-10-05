#! /usr/bin/env python3

'''
Pop! OS Python Setup Script
Author:  Ben C. Calvert
Date:  18 September 2021

Description:  This program configures Pop! OS Linus based on configuration parameters found in the ../Data directory JSON files.

'''

import os
import sys
import httplib2
from classes import ArgsClass as AC

'''
ToDo:

1.  Collect arguments
2.  Read JSON files (or recipe files)
3.  Perform upgrade of the system
4.  Install Pop! OS Packages
5.  Install 3rd Party Packages based on URL and wget commands
    - unreliable as finding the correct URL is difficult.  Will check Download Directory.
6.  Configure System setting files - .vimrc, .bash_aliases, default editor, etc.

'''

def validate_dir(dir_path):
    if os.path.isdir(dir_path):
        return True
    else:
        print(f'Skipping 3rd Party package install.  {dir_path} does not exist.')
        return False
    

def test_for_file(file):
    if os.path.isfile(file):
        print(f'{file} exists!')
        return True
    else:
        return False



def main():
    '''Main Program function'''

    # Declare Constants and Variables

    HOME_DIR = os.getenv("HOME")

    ALIAS_FILE = HOME_DIR + '/.bash_aliases'
    BASHRC_FILE = HOME_DIR + '/.bashrc'
    VIMRC_FILE = HOME_DIR + '/.vimrc'
    FAKE_FILE = HOME_DIR + '/.fake_file'

    if args.directory == 'default':
        download_dir = os.getenv('HOME') + '/Downloads/'
    else:
        # Validate format
        download_dir = args.directory
    dir_exists = validate_dir(download_dir)

    if dir_exists is False:
        args.skip = '3rdParty'
    

    update_command = 'sudo apt update && sudo apt upgrade'
    full_upgrade_command = 'sudo apt update && sudo apt full-upgrade'
    favorite_packages = 'sudo apt install -y snapd code vim neofetch gnome-tweaks libavcodec-extra steam deja-dup thunderbird zenmap sysfsutils'
    codec_packages = 'sudo apt install -y gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly libavcodec-extra gstreamer1.0-libav'
    sshfs_support = 'sudo apt install -y exfat-fuse exfat-utils sshfs'
    python3_extras = 'sudo apt install -y python3-pip python3-venv'
    cleanup_packages = 'sudo apt update && sudo apt autoremove'
    set_default_editor = 'sudo update-alternatives --config editor'

    commands = [update_command, full_upgrade_command,favorite_packages, codec_packages, sshfs_support, python3_extras, cleanup_packages, set_default_editor]

    # Configuration Scripts

    update_dot_bash_profile = 'echo \nneofetch\necho'
    create_dot_vimrc = 'syntax on \nset numbers \ncolorscheme ron \n'
    bash_aliases = "alias update='sudo apt update && sudo apt upgrade' \nalias upgrade='sudo apt update && sudo apt full-upgrade' \nalias cleanup='sudo apt update && sudo apt autoremove' \n"
    bluetooth_ERTM_disable = 'module/bluetooth/parameters/disable_ertm=1'
    
    
    # Turn off Bluetooth ERTM - append to the end of /etc/sysfs.conf
    '''
	echo 
	echo "Enabling Bluetooth Xbox One Controller Support."
	echo
	grep "disable_ertm=1" /etc/sysfs.conf
	if [ $? -ne 0 ]; then
		echo "/etc/sysfs.conf edits not found.  Editing now..."
		echo
		sudo chmod o+w /etc/sysfs.conf # enable writing to /etc/sysfs.conf
		sudo echo "module/bluetooth/parameters/disable_ertm=1" >> /etc/sysfs.conf
		sudo chmod o-w /etc/sysfs.conf # dsiable writing to /etc/sysfs.conf
		echo
		echo "Be sure to reboot to complete disabling of Bluetooth ERTM (Enhanced Re-Transmission Mode)."
	else
		echo "Bluetooth ERTM already disabled."
		echo
	fi
	echo
    '''

    shell = os.getenv('SHELL')
    kernel = os.system('uname -svr')
    

    # Run install and setup commands

    for command in commands:
        os.system(command)
    

    bashrc_result = test_for_file(BASHRC_FILE)
    bash_aliases_result = test_for_file(ALIAS_FILE)
    vimrc_result = test_for_file(VIMRC_FILE)
    fake_file_result = test_for_file(FAKE_FILE)

    print(bashrc_result, bash_aliases_result, vimrc_result, fake_file_result)

    '''
    To Do:

        Read files
        Check for entries
        Write lines
        Save files

    '''

    print(update_dot_bash_profile)
    print(create_dot_vimrc)
    print(bash_aliases)
    print(bluetooth_ERTM_disable)
    

if __name__ == '__main__':

    # Call CLI Parser and get command line arguments
    args = AC.CLIParser().get_args()
    print(args)
 

    # Start program
    main()