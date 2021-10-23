#! /usr/bin/env python3

'''
Pop! OS Python Setup Script
Author:  Ben C. Calvert
Date:  18 September 2021

Description:  This program configures Pop! OS Linux per user requirements.

'''

import os
import re
import json
from classes import ArgsClass as AC

# Declare Program Functions

def validate_dir(dir_path):

    '''
    Check for 3rd Party Downloads
    '''

    if os.path.isdir(dir_path):
        return True
    else:
        print(f'{dir_path} does not exist.')
        return False


def create_backup_dir(backup_dir):

    '''
    Create a backup directory under user's HOME
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
    '''
    
    if os.path.isfile(file):
        return True
    else:
        return False


def create_file(file):
    
    '''
    Create a file - incase config file is missing.
    '''

    os.system('touch ' + file)

    if not os.path.isfile(file):
        print(f'File: {file} could not be created.')
    else:
        print(f'Created: {file} successfully!!')


def backup_file(file):

    '''
    Test for file and if doesn't exist, create it then preform backup
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


def process_commands(commands_array):
    '''
    Process commands in array
    '''

    for command in commands_array:
            os.system(command)    


def read_json_file(file):
    '''
    Process commands in config file and return json object
    '''
    with open(file, 'rb') as json_file:
        json_data = json_file.read()
    return json.loads(json_data)


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
        download_dir = args.directory

    # Validate Download Directory

    dir_exists = validate_dir(download_dir)

    if dir_exists is False:
        args.skip = '3rdParty'

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

    if "update" in args.skip:
        print('\n' + '*'*100 + '\n\tSkipping Update Process\n' + '*'*100 + '\n')
    else:
        print('\n' + '*'*100 + '\n\tUpdating System...\n' + '*'*100 + '\n')

        process_commands(update_commands_array)

    if "install" in args.skip:
        print('\n' + '*'*100 + '\n\tSkipping Package Install Process\n' + '*'*100 + '\n')
    else:
        print('\n' + '*'*100 + '\n\tInstalling Additional Packages...\n' + '*'*100 + '\n')

        process_commands(install_commamds_array)

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
            entry_exists = False
            if config_file == BASHRC_FILE:
                lines = read_config_file(config_file)
                for line in lines:
                    if re.search('neofetch', line):
                        entry_exists = True
                        print(f'Config file entry exists in: {config_file}. No edit required.')
                if entry_exists is False:
                    write_config_file(config_file, script_syntax)
            elif config_file == ALIAS_FILE:
                lines = read_config_file(config_file)
                for line in lines:
                    if re.search('alias update=', line):
                        entry_exists = True
                        print(f'Config file entry exists in: {config_file}. No edit required.')
                if entry_exists is False:
                    write_config_file(config_file, script_syntax)
            elif config_file == VIMRC_FILE:
                lines = read_config_file(config_file)
                for line in lines:
                    if re.search('colorscheme', line):
                        entry_exists = True
                        print(f'Config file entry exists in: {config_file}. No edit required.')
                if entry_exists is False:
                    write_config_file(config_file, script_syntax)
            elif config_file == ETC_SYSFS_CONF_FILE:
                lines = read_config_file(config_file)
                for line in lines:
                    if re.search('module/bluetooth/parameters/disable_ertm=1', line):
                        entry_exists = True
                        print(f'Config file entry exists in: {config_file}. No edit required.')
                if entry_exists is False:
                    os.system(f'sudo chmod o+w {config_file}')
                    write_config_file(config_file, script_syntax)
                    os.system(f'sudo chmod o-w {config_file}')
            else:
                pass
    
    if test_for_file_exists('/var/run/reboot-required'):
        print('\n' + '*'*100 + '\n\tPlease reboot to complete installation\n' + '*'*100 + '\n')
    
    else:
        print('\n' + '*'*100 + '\n\tInstallation Complete!\n' + '*'*100 + '\n')

if __name__ == '__main__':

    # Call CLI Parser and get command line arguments

    args = AC.CLIParser().get_args()
 
    # Start program
    main()