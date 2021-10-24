#! /usr/bin/env python3

'''
Pop! OS Python Setup Script
Author:  Ben C. Calvert
Date:  18 September 2021

Description:  This program configures Pop! OS Linux per user requirements found in data/.

'''

import os
import re
import json
from classes import ArgsClass as AC

# Declare Program Functions

def validate_dir(dir_path):

    '''
    Check for 3rd Party Downloads

    dir_path: string 

    return: bool
    '''

    if os.path.isdir(dir_path):
        return True
    else:
        print(f'{dir_path} does not exist.')
        return False


def create_backup_dir(backup_dir):

    '''
    Create a backup directory under user's HOME

    backup_dir: string

    return: bool
    '''

    if os.path.isdir(backup_dir) is True:
        print(f'Backup directory: {backup_dir} exists!')
        return True
    else:
        print(f'Createing backup directory: {backup_dir}')
        os.system(f'mkdir {backup_dir}')
        if os.path.isdir(backup_dir) is True:
            return True
        else:
            return False


def test_for_file_exists(file):
    
    '''
    Test for file existance.

    file: string (complete path to file)

    return: bool
    '''
    
    if os.path.isfile(file):
        return True
    else:
        return False


def create_file(file):
    
    '''
    Create a file - incase config file is missing.

    file: string (complete path to file)

    return: none
    '''

    os.system('touch ' + file)

    if not os.path.isfile(file):
        print(f'File: {file} could not be created.')
    else:
        print(f'Created: {file} successfully!!')


def backup_file(file):

    '''
    Test for file and if doesn't exist, create it then preform backup

    file: string (complete path to file)

    return: bool
    '''

    # get just the filename for copy purposes by splitting, reversing [::-1], and grabbing first element [0]
    
    filename = file.split("/")[::-1][0]

    if not os.path.isfile(file):
        os.system('touch ' + file)
        os.system(f"echo '#! Create by Pop_OS Py Script' >> {file}")
        return True

    elif os.path.isfile(file):
        print(f'Backing up: {file}')

        # Make a backup file
    
        os.system(f'cp {file} ~/backup/{filename}.bkup')
        return True
    else:
        print(f'Could not create: {file}')
        return False
   

def write_config_file(file, lines):

    '''
    Write data to config file based on values in lines

    file: string (complete path to file)
    lines: array of strings

    return: none
    '''

    with open(file, 'a') as of:
        of.write(lines)
    return


def read_config_file(file):

    '''
    Read data from config file

    file: string (complete path to file)

    return: array of strings
    '''

    with open(file, 'r') as rf:
        return rf.readlines()


def read_json_file(file):
    '''
    Process commands in config file and return json object

    file: string (complete path to file)

    return: Python Object
    '''

    with open(file, 'rb') as json_file:
        json_data = json_file.read()
    return json.loads(json_data)


def process_config_file(config_file, search_term, script_syntax):
    '''
    Process config file script entries based on search term and 
    make a decision to write script_syntax or not to write the syntax.

    config_file: string (complete path to file)
    search_term: string
    script_syntax: string

    return: none
    '''

    entry_exists = False

    # Read config file lines
    lines = read_config_file(config_file)

    # Search each line for the specified search term
    print(f'Checking {config_file} for: \n{script_syntax}')
    for line in lines:
        if re.search(search_term, line):
            entry_exists = True
            output_config_file_msg(config_file, 1)

    # If serach terms do not appear, write script syntax

    if entry_exists is False and config_file != '/etc/sysfs.conf':
        print(f'No entry in {config_file}')
        write_config_file(config_file, script_syntax)
        output_config_file_msg(config_file, 2)

    # Check for special case file /etc/sysfs.conf - Xbox controller support for gaming
    elif entry_exists is False and config_file == '/etc/sysfs.conf':
        os.system(f'sudo chmod o+w {config_file}')
        write_config_file(config_file, script_syntax)
        output_config_file_msg(config_file, 2)
        os.system(f'sudo chmod o-w {config_file}')
    else:
        pass

    return


def process_commands(commands_array):
    '''
    Process commands in array

    commands_array: array of strings

    return: none
    '''

    for command in commands_array:
            os.system(command)    


def output_config_file_msg(config_file, msg):
    '''
    Method to print a config file message based on msg value - code simplification

    config_file: string (complete path to file)
    msg: integer (values 1 or 2 accepted)

    return: none
    '''

    if msg == 1:
        print(f'Config file entry exists in: {config_file}  No edit required.\n')
    elif msg == 2:
        print(f'New lines added to {config_file}.\n')
    else:
        print(f'Invalid message type:  {msg}.\n')
    return

# Main Program

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

    if args.test is True:
        print(args)
        quit()

    if args.directory == 'default':
        download_dir = os.getenv('HOME') + '/Downloads/'
    else:
        download_dir = args.directory

    # Validate Download Directory

    # dir_exists = validate_dir(download_dir)

    # if dir_exists is False:
    #     args.skip = '3rdParty'

    # Create Backup Directory

    print('\n' + '*'*100 + '\n\tCreating Backup Directory for config files...\n' + '*'*100 + '\n')

    if args.backup_directory == 'default':
        backup_directory = HOME_DIR + '/backup/'
    else:
        backup_directory = args.backup_directory

    # Validate Backup Directory

    backup_dir_exists = create_backup_dir(backup_directory)

    # Fail if the backup directory creation fails

    if not backup_dir_exists:
        print('Backup Directory creation failed.  Exiting script.')
        quit()

    # Command Variables - Can be user defined.  New variable can be added to update_command array.

    pkg_commands = read_json_file('data/pkgcommands.json')

    # Read Python Object attributes and store in variables
    update_command = pkg_commands.get('update_command')
    full_upgrade_command = pkg_commands.get('full_upgrade_command')
    favorite_packages = pkg_commands.get('favorite_packages')
    codec_packages = pkg_commands.get('codec_packages')
    sshfs_support = pkg_commands.get('sshfs_support')
    python3_extras = pkg_commands.get('python3_extras')
    programming_extras = pkg_commands.get('programming_extras')
    cleanup_packages = pkg_commands.get('cleanup_packages')
    flatpak_packages = pkg_commands.get('flatpak_packages')
    snap_packages = pkg_commands.get('snap_packages')
    set_default_editor = pkg_commands.get('set_default_editor')


    # Create Array of upgrade commands to parse through

    update_commands_array = [update_command, full_upgrade_command]

    # Create Array of install commands to parse through

    install_commamds_array = [  favorite_packages, 
                                codec_packages, 
                                sshfs_support, 
                                python3_extras, 
                                programming_extras, 
                                cleanup_packages, 
                                flatpak_packages, 
                                snap_packages
                            ]

    # Configuration Script Data

    syntax_commands = read_json_file('data/syntaxcommands.json')

    # Read Python Object attributes and store in variables
    syntax_dot_bash_rc = syntax_commands.get('syntax_dot_bash_rc')
    syntax_bash_aliases = syntax_commands.get('syntax_bash_aliases')
    syntax_dot_vimrc = syntax_commands.get('syntax_dot_vimrc')
    syntax_bluetooth_ERTM_disable = syntax_commands.get('syntax_bluetooth_ERTM_disable')
    
    # Create Array of script variables to parse through

    script_syntax_array = [ syntax_dot_bash_rc, 
                            syntax_bash_aliases, 
                            syntax_dot_vimrc, 
                            syntax_bluetooth_ERTM_disable
                          ]

    print('\n' + '*'*100 + '\n\tGetting Kernel and other System information...\n' + '*'*100 + '\n')

    shell = os.getenv('SHELL')
    kernel = os.system('uname -svr')
    

    # Run install and setup commands

    skip_items = ' '.join(args.skip)

    if "update" in skip_items.lower():
        print('\n' + '*'*100 + '\n\tSkipping Update Process\n' + '*'*100 + '\n')
    else:
        print('\n' + '*'*100 + '\n\tUpdating System...\n' + '*'*100 + '\n')

        process_commands(update_commands_array)

    if "install" in skip_items.lower():
        print('\n' + '*'*100 + '\n\tSkipping Package Install Process\n' + '*'*100 + '\n')
    else:
        print('\n' + '*'*100 + '\n\tInstalling Additional Packages...\n' + '*'*100 + '\n')

        process_commands(install_commamds_array)

    # Install 3rd Party Packages

    if "3rdparty" in skip_items.lower():
        print('\n' + '*'*100 + '\n\tSkipping 3rd Party Package Install Process\n' + '*'*100 + '\n')
    else:
        print('\n' + '*'*100 + '\n\tInstalling Additional 3rd Party Packages...\n' + '*'*100 + '\n')

        # Python Foo:  get diretory list and filter for *.deb using Regular Expressions!
        third_party_apps = [val for val in os.listdir(download_dir) if re.search(r'.deb', val)]

        # Print 3rdParty Apps to install
        print(f'The following 3rdParty Apps will be installed:\n\t{", ".join(third_party_apps)}')

        # Install the app
        for app in third_party_apps:
            os.system(f'sudo apt install {download_dir}{app}')

        # Check for new versions
        print('\nUpdating system after 3rdParty App updates...\n')
        os.system('sudo apt update && sudo apt upgrade')
   
    # Set Default CLI editor...I like Vim!
    
    print('\n' + '*'*100 + '\n\tSetting the default editor (I like VIM)...\n' + '*'*100 + '\n')

    os.system(set_default_editor)
    
    # Add lines to configuration files

    print('\n' + '*'*100 + '\n\tConfiguring the Config files...\n' + '*'*100 + '\n')

    # Create Config File Array to parse through.  Create Dictionary of config files : config script data.

    config_files_array = [BASHRC_FILE, ALIAS_FILE, VIMRC_FILE, ETC_SYSFS_CONF_FILE]
    
    # Check for length of arrays to be equal - program check!

    if len(config_files_array) != len(script_syntax_array):
        print('Please check script files.  Length mismatch!')
        quit()


    # Write Config Files

    for config_file, script_syntax in zip(config_files_array, script_syntax_array):
        bf = backup_file(config_file)
        if bf is True:
            # entry_exists = False
            if config_file == BASHRC_FILE:
                process_config_file(config_file, 'neofetch', script_syntax)

            elif config_file == ALIAS_FILE:
                process_config_file(config_file, 'alias update=', script_syntax)

            elif config_file == VIMRC_FILE:
                process_config_file(config_file, 'colorscheme', script_syntax)

            elif config_file == ETC_SYSFS_CONF_FILE:
                process_config_file(config_file, 'module/bluetooth/parameters/disable_ertm=1', script_syntax)

            else:
                pass
    
    # Post Installation Work
    print('\n' + '*'*100 + '\n\tPost Installation Cleanup...\n' + '*'*100 + '\n')

    # System Package Cleanup

    print('\nRemoving Unused Packages...\n')
    os.system('sudo apt autoremove')
    
    # Store a list of installed packages in HOME/backup (overwrite if file exists ">"; NOT append ">>")

    print(f'\n Creating a list of installed packages in {backup_directory}...')
    os.system(f'dpkg --get-selections > {backup_directory}Installed_Packages_$(date +%m_%d_%Y).log')

    # Test to see if reboot is needed

    if test_for_file_exists('/var/run/reboot-required'):
        print('\n' + '*'*100 + '\n\tPlease reboot to complete installation\n' + '*'*100 + '\n')
    else:
        print('\n' + '*'*100 + '\n\tInstallation Complete!\n' + '*'*100 + '\n')

if __name__ == '__main__':

    # Call CLI Parser and get command line arguments

    args = AC.CLIParser().get_args()
 
    # Start program
    main()