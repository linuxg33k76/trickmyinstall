#! /usr/bin/env python3

'''
Pop! OS Python Setup Script
Author:  Ben C. Calvert
Date:  18 September 2021

Description:  This program configures Pop! OS Linus based on configuration parameters found in the ../Data directory JSON files.

'''

import os
import re
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
    '''
    Check for 3rd Party Downloads
    '''
    if os.path.isdir(dir_path):
        return True
    else:
        print(f'Skipping 3rd Party package install.  {dir_path} does not exist.')
        return False
    

def test_for_file(file):
    '''
    Test for file and if doesn't exist, create it
    '''
    if not os.path.isfile(file):
        os.system('touch ' + file)
    if os.path.isfile(file):
        print(f'This file exists: {file}')
        # Make a backup file
        os.system(f'cp {file} {file}.bkup')
        return True
    else:
        print(f'Could not create: {file}')
        return False
   

def write_config_file(file, lines):
    '''
    Write data to config file
    '''
    with open(file, 'a') as of:
        of.write(lines)
        print(f'Wrote to file: {file}')
    return


def read_config_file(file):
    '''
    Read data from config file
    '''
    with open(file, 'r') as rf:
        return rf.readlines()


def main():
    '''
    Main Program function
    '''

    # Declare Constants and Variables

    HOME_DIR = os.getenv("HOME")

    ALIAS_FILE = HOME_DIR + '/.bash_aliases'
    BASHRC_FILE = HOME_DIR + '/.bashrc'
    VIMRC_FILE = HOME_DIR + '/.vimrc'
    ETC_SYSFS_CONF_FILE = '/etc/sysfs.conf'

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
    favorite_packages = 'sudo apt install -y snapd code vim neofetch gnome-tweaks gnome-boxes libavcodec-extra steam deja-dup thunderbird zenmap sysfsutils'
    codec_packages = 'sudo apt install -y gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly libavcodec-extra gstreamer1.0-libav'
    sshfs_support = 'sudo apt install -y exfat-fuse exfat-utils sshfs'
    python3_extras = 'sudo apt install -y python3-pip python3-venv'
    cleanup_packages = 'sudo apt update && sudo apt autoremove'
    set_default_editor = 'sudo update-alternatives --config editor'

    commands = [update_command, full_upgrade_command,favorite_packages, codec_packages, sshfs_support, python3_extras, cleanup_packages, set_default_editor]

    # Configuration Scripts

    syntax_dot_bash_rc = '\nneofetch\n'
    syntax_dot_vimrc = '\nsyntax on\nset number\ncolorscheme ron\n'
    syntax_bash_aliases = "alias update='sudo apt update && sudo apt upgrade'\nalias upgrade='sudo apt update && sudo apt full-upgrade'\nalias cleanup='sudo apt update && sudo apt autoremove'\n"
    syntax_bluetooth_ERTM_disable = 'module/bluetooth/parameters/disable_ertm=1\n'
        
    # Turn off Bluetooth ERTM - append to the end of /etc/sysfs.conf

    shell = os.getenv('SHELL')
    kernel = os.system('uname -svr')
    

    # Run install and setup commands

    for command in commands:
        os.system(command)
    

    config_files = [BASHRC_FILE, ALIAS_FILE, VIMRC_FILE, ETC_SYSFS_CONF_FILE]
    config_data = {BASHRC_FILE: syntax_dot_bash_rc, ALIAS_FILE: syntax_bash_aliases, VIMRC_FILE: syntax_dot_vimrc, ETC_SYSFS_CONF_FILE: syntax_bluetooth_ERTM_disable}

    for config_file in config_files:
        tf = test_for_file(config_file)
        if tf is True:
            entry_exists = False
            if config_file == BASHRC_FILE:
                lines = read_config_file(config_file)
                for line in lines:
                    if re.search('neofetch', line):
                        entry_exists = True
                if entry_exists is False:
                    write_config_file(config_file, config_data[config_file])
            elif config_file == ALIAS_FILE:
                lines = read_config_file(config_file)
                for line in lines:
                    if re.search('alias update=', line):
                        entry_exists = True
                if entry_exists is False:
                    write_config_file(config_file, config_data[config_file])
            elif config_file == VIMRC_FILE:
                lines = read_config_file(config_file)
                for line in lines:
                    if re.search('colorscheme', line):
                        entry_exists = True
                if entry_exists is False:
                    write_config_file(config_file, config_data[config_file])
            elif config_file == ETC_SYSFS_CONF_FILE:
                lines = read_config_file(config_file)
                for line in lines:
                    if re.search('module/bluetooth/parameters/disable_ertm=1', line):
                        entry_exists = True
                if entry_exists is False:
                    os.system(f'sudo chmod o+w {config_file}')
                    write_config_file(config_file, config_data[config_file])
                    os.system(f'sudo chmod o-w {config_file}')
            else:
                pass


if __name__ == '__main__':

    # Call CLI Parser and get command line arguments
    args = AC.CLIParser().get_args()
    print(args)
 

    # Start program
    main()