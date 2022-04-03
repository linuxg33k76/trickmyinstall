#! /usr/bin/env python3

'''
Pop! OS Python Setup Script
Author:  Ben C. Calvert
Date:  18 September 2021

Description:  This program configures Linux environment per YAML config found in data/.

Distros Supported:  Pop!_OS, Ubuntu, Fedora, Manjaro

'''

from logging import raiseExceptions
import os
import re
import getpass
import yaml
from classes import ArgsClass as AC
from classes import LinuxSystemInfo as LSI

# Declare Program Functions

def check_for_root():

    '''
    Check for root user

    return: bool
    '''

    user = os.popen('whoami','r').read().strip('\n')

    print(f'\n*** User: {user} is executing this script.***\n')

    if user == 'root':
        return True
    else:
        return False


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
    Create a backup directory

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


def read_config_file(file):

    '''
    Read data from config file - in YAML format

    file: string (complete path to file)

    return: array of strings
    '''

    with open(file, 'r') as rf:
        return yaml.safe_load(rf)


def process_commands(commands_array):
    '''
    Process commands in array

    commands_array: array of strings

    return: none
    '''

    for command in commands_array:
            os.system(command)    

def get_remote_backup_info():
    '''
    Collect System and User Input

    return: dictionary
    '''
    regex = r'uid=(\d{1,4})\D{1,}gid=(\d{1,4})'
    regex_gid = r'\Dgid=(\d{1,4})'
    current_user = os.popen('whoami','r').read().strip('\n')
    id_info = os.popen('id','r').read().strip('\n')
    uid = re.match(regex, id_info).group(1)
    gid = re.match(regex, id_info).group(2)

    # Collect User inputs

    invalid = True
    while invalid:
        host_ip = input('Remote Samba Server IP Address: ')
        host_name = input('Remote Samba Server name: ')
        host_share = input ('Remote Samba Share name: ')
        user_cred = input('Remote Samba Share Username: ')
        password_check_invalid = True
        while password_check_invalid:
            pass_cred1 = getpass.getpass('Remote Samba Share Password: ')
            pass_cred2 = getpass.getpass('Please confirm password: ')
            if pass_cred1 == pass_cred2:
                pass_cred = pass_cred1
                password_check_invalid = False
            else:
                print('Passwords Do NOT match!  Please try again.')
        domain_cred = input('Remote Samba Share Domain: ')
        print(f'Samba Host IP: {host_ip}\nSamba Host Name: {host_name}\nSamba share: {host_share}\nSamba user: {user_cred}\nSamba pass: {pass_cred}\nSamba domain: {domain_cred}\n')
        response = input("Does the information look correct? (Y/n)")
        print(response)
        if 'Y' in response or 'y' in response:
            invalid = False
    
    results = {
        'host_ip': host_ip,
        'host_name': host_name,
        'host_share': host_share,
        'user_cred': user_cred,
        'pass_cred': pass_cred,
        'domain_cred': domain_cred,
        'current_user': current_user,
        'uid': uid,
        'gid': gid
    }
    return results

# Main Program

def main():

    '''
    Main Program function
    '''

    # Declare Constants and Variables

    HOME_DIR = os.getenv("HOME")
    os_info = LSI.LinuxSystemInfo().system
    user_test = check_for_root()

    # User check - if root exit script and print error message

    if user_test is True:
        print("\n***Script Aborting...  Please execute with a privileged user other than root user.***\n")
        quit()

    # Identify Terminal Size

    c = os.popen('stty size', 'r').read().split()[1]

    if int(c) > 120:
        columns = 120
    else:
        columns = int(c)

    # Process CLI arguments

    if args.test is True:
        print(args)
        quit()

    if args.directory == 'default':
        download_dir = os.getenv('HOME') + '/Downloads/'
    else:
        download_dir = args.directory

    # Create Backup Directory

    print('\n' + '*'*columns + '\n\tCreating Backup Directory for config files...\n' + '*'*columns + '\n')

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

    # Used os_info to decide which YAML file to use

    if "ubuntu" in os_info or "pop" in os_info:

        # Ubuntu/Pop OS setup parameters
        yaml_config = read_config_file('data/popos.yaml')
    
    elif 'fedora' in os_info:

        # Fedora setup parameters
        yaml_config = read_config_file('data/fedora.yaml')
    
    elif 'manjaro' in os_info:

        # Manjaro setup parameters
        yaml_config = read_config_file('data/manjaro.yaml')
        
    else:
        print('OS type not found!  Exiting the system.')
        quit()

    # Configure Variables based on config files

    update_commands_array = yaml_config['Update']
    install_commamds_array = yaml_config['Packages']
    macwifi_commands_array = yaml_config['MacDevice']
    vim_commands_array = yaml_config['VimSetup']
    environment_commands = yaml_config['Environment']
    
    # Run install and setup commands

    skip_items = ' '.join(args.skip)

    if "update" in skip_items.lower():
        print('\n' + '*'*columns + '\n\tSkipping Update Process\n' + '*'*columns + '\n')
    else:
        print('\n' + '*'*columns + '\n\tUpdating System...\n' + '*'*columns + '\n')

        process_commands(update_commands_array)

    if "install" in skip_items.lower():
        print('\n' + '*'*columns + '\n\tSkipping Package Install Process\n' + '*'*columns + '\n')
    else:
        print('\n' + '*'*columns + '\n\tInstalling Additional Packages...\n' + '*'*columns + '\n')

        process_commands(install_commamds_array)

    # Install 3rd Party Packages

    if "3rdparty" in skip_items.lower():
        print('\n' + '*'*columns + '\n\tSkipping 3rd Party Package Install Process\n' + '*'*columns + '\n')
    else:
        print('\n' + '*'*columns + '\n\tInstalling Additional 3rd Party Packages...\n' + '*'*columns + '\n')

        # Python Foo:  get diretory list and filter for *.deb using Regular Expressions!
        
        if "pop" in os_info:
            third_party_apps = [val for val in os.listdir(download_dir) if re.search(r'.deb', val)]
        elif "fedora" in os_info:
            third_party_apps = [val for val in os.listdir(download_dir) if re.search(r'.rpm', val)]
        else:
            third_party_apps = ['None']

        # Print 3rdParty Apps to install

        print(f'The following 3rdParty Apps will be installed:\n\t{", ".join(third_party_apps)}')

        # Install the app(s)

        if "pop" in os_info:

            for app in third_party_apps:
                os.system(f'sudo apt install {download_dir}{app}')
    
        elif "fedora" in os_info:
        
            for app in third_party_apps:
                os.system(f'sudo dnf install {download_dir}{app}')
    
        else:
            pass

    # Check for new versions

    print('\nUpdating system after 3rdParty App Install...\n')

    process_commands(update_commands_array)
   
    # Set Default CLI editor...I like Vim!

    print('\n' + '*'*columns + '\n\tSetting the default editor (I like VIM)...\n' + '*'*columns + '\n')
    
    process_commands(vim_commands_array)

    # Setting up Environment (See YAML files for details on commands)

    if args.macwifi is True:
        print('\n' + '*'*columns + '\n\tInstalling Mac Wi-Fi Drivers...\n' + '*'*columns + '\n')
        process_commands(macwifi_commands_array)

    print('\n' + '*'*columns + '\n\tRunning Configuration Scripts...\n' + '*'*columns + '\n')

    process_commands(environment_commands)
    
    # Setup Remote Samba File Store

    print('\n' + '*'*columns + '\n\tSetup Samba Share\n' + '*'*columns + '\n')

    user_response = input('\nSetup Remote Samba Share with /mnt/remote_cifs? (Y/n)')

    if "Y" in user_response or "y" in user_response:
        '''
        Setup remote samba share
        '''
        # Get cifs share information
        rb_data = get_remote_backup_info()

        # Alert User process is starting

        print('\n' + '*'*columns + '\n\tSetting Up Remote Samba Share...\n' + '*'*columns + '\n')

        # Create /etc/host entry
        os.system(('grep "{0}" /etc/hosts || echo "{0}  {1}" | sudo tee -a /etc/hosts')\
            .format(rb_data['host_ip'], rb_data['host_name']))

        # Write Credentials to user's home directory
        samba_file = HOME_DIR + '/.sambacreds'
        os.system(('echo "username={0}\npassword={1}\ndomain={2}" > {3}')\
            .format(rb_data['user_cred'], rb_data['pass_cred'],rb_data['domain_cred'], samba_file))
        
        # Backup Samba Directory
        os.system(f'cp {HOME_DIR}/.sambacreds {backup_directory}')

        # Create /mnt mount point
        REMOTE_MNT = '/mnt/remote_cifs'
        user = rb_data['current_user']
        os.system(f'test -d {REMOTE_MNT} || sudo mkdir {REMOTE_MNT}')
        os.system(f'sudo chmod -R 770 {REMOTE_MNT}')
        os.system(f'sudo chown -R {user}:{user} {REMOTE_MNT}')

        # Write cifs entry to /etc/fstab
        os.system('grep "# Samba Mount created by TrickMyInstall Script" /etc/fstab || echo "# Samba Mount created by TrickMyInstall Script" | sudo tee -a /etc/fstab')
        os.system(('grep "//{0}/{1}" /etc/fstab || echo "//{0}/{1}  /mnt/remote_cifs  cifs  credentials={2},uid={3},gid={4}  0       0 " | sudo tee -a /etc/fstab')\
            .format(rb_data['host_name'], rb_data['host_share'], samba_file, rb_data['uid'], rb_data['gid']))
    
        # Mount cifs share

        os.system('sudo systemctl daemon-reload')
        os.system('sudo mount -a')
    else:
        print('\n' + '*'*columns + '\n\tSkipping Remote Samba Share...\n' + '*'*columns + '\n')


    # Store a list of installed packages in HOME/backup (overwrite if file exists ">"; NOT append ">>")

    print(f'\n Creating a list of installed packages in {backup_directory}...')

    if "pop" in os_info:
        os.system(f'dpkg --get-selections > {backup_directory}Installed_Ubuntu_Packages_$(date +%m_%d_%Y).log')
    elif "fedora" in os_info:
        os.system(f'sudo rpm -qa > {backup_directory}Installed_Fedora_Packages_$(date  +%m_%d_%Y).log')
    elif 'manjaro' in os_info:
        os.system(f'sudo pacman -Qe > {backup_directory}Installed_Manjaro_Packages_$(date +%m_%d_%Y).log')
    else:
        pass

    # Backup Dconf (Gnome) settings
    
    print(f'\n Creating a Gnome Settings (dconf) in {backup_directory}...')
    os.system(f'dconfz dump / > {backup_directory}dconf_user_settings_$(date +%m_%d_%Y).bkup')

    # Test to see if reboot is needed

    if test_for_file_exists('/var/run/reboot-required'):
        print('\n' + '*'*columns + '\n\tPlease reboot to complete installation\n' + '*'*columns + '\n')
    else:
        print('\n' + '*'*columns + '\n\tInstallation Complete!\n' + '*'*columns + '\n')

if __name__ == '__main__':

    # Call CLI Parser and get command line arguments

    args = AC.CLIParser().get_args()

    # Start program
    main()