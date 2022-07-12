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
from classes import TMIClass as TMIC
from classes import ArgsClass as AC
from classes import SystemInfo as SI


# Main Program

def main():

    '''
    Main Program function
    '''

    # Declare Constants and Variables

    HOME_DIR = os.getenv("HOME")
    UNAME = os.popen('uname', 'r').read().strip()

    if 'Darwin' in UNAME:
        os_info = SI.MacOSSystemInfo().system
    else:
        os_info = SI.LinuxSystemInfo().system
    
    user_test = tmi.check_for_root()

    # User check - if root exit script and print error message

    if user_test is True:
        print('\n***Script Aborting...  Please execute with a privileged user other than root user.***\n')
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

    backup_dir_exists = tmi.create_backup_dir(backup_directory)

    # Fail if the backup directory creation fails

    if not backup_dir_exists:
        print('Backup Directory creation failed.  Exiting script.')
        quit()

    # Used os_info to decide which YAML file to use

    if 'ubuntu' in os_info or 'pop' in os_info:

        # Ubuntu/Pop OS setup parameters
        yaml_config = tmi.read_config_file('data/popos.yaml')
    
    elif 'fedora' in os_info:

        # Fedora setup parameters
        yaml_config = tmi.read_config_file('data/fedora.yaml')
    
    elif 'manjaro' in os_info:

        # Manjaro setup parameters
        yaml_config = tmi.read_config_file('data/manjaro.yaml')
        
    else:
        print('OS type not found!  Exiting the system.')
        tmi.process_commands(["uname -srv", "neofetch"])
        quit()

    # Configure Variables based on config files

    update_commands_array = yaml_config['Update']
    install_commamds_array = yaml_config['Packages']
    macwifi_commands_array = yaml_config['MacDevice']
    vim_commands_array = yaml_config['VimSetup']
    environment_commands = yaml_config['Environment']
    
    # Run install and setup commands

    skip_items = ' '.join(args.skip)

    if 'update' in skip_items.lower():
        print('\n' + '*'*columns + '\n\tSkipping Update Process\n' + '*'*columns + '\n')
    else:
        print('\n' + '*'*columns + '\n\tUpdating System...\n' + '*'*columns + '\n')

        tmi.process_commands(update_commands_array)

    if 'install' in skip_items.lower():
        print('\n' + '*'*columns + '\n\tSkipping Package Install Process\n' + '*'*columns + '\n')
    else:
        print('\n' + '*'*columns + '\n\tInstalling Additional Packages...\n' + '*'*columns + '\n')

        tmi.process_commands(install_commamds_array)

    # Install 3rd Party Packages

    if '3rdparty' in skip_items.lower():
        print('\n' + '*'*columns + '\n\tSkipping 3rd Party Package Install Process\n' + '*'*columns + '\n')
    else:
        print('\n' + '*'*columns + '\n\tInstalling Additional 3rd Party Packages...\n' + '*'*columns + '\n')

        # Python Foo:  get diretory list and filter for *.deb using Regular Expressions!
        
        if 'pop' in os_info:
            third_party_apps = [val for val in os.listdir(download_dir) if re.search(r'.deb', val)]
        elif 'fedora' in os_info:
            third_party_apps = [val for val in os.listdir(download_dir) if re.search(r'.rpm', val)]
        else:
            third_party_apps = ['None']

        # Print 3rdParty Apps to install

        print(f'The following 3rdParty Apps will be installed:\n\t{", ".join(third_party_apps)}')

        # Install the app(s)

        if 'pop' in os_info:

            for app in third_party_apps:
                os.system(f'sudo apt install {download_dir}{app}')
    
        elif 'fedora' in os_info:
        
            for app in third_party_apps:
                os.system(f'sudo dnf install {download_dir}{app}')
    
        else:
            pass

    # Check for new versions

    print('\nUpdating system after 3rdParty App Install...\n')

    tmi.process_commands(update_commands_array)
   
    # Set Default CLI editor...I like Vim!

    print('\n' + '*'*columns + '\n\tSetting the default editor (I like VIM)...\n' + '*'*columns + '\n')
    
    tmi.process_commands(vim_commands_array)

    # Setting up Environment (See YAML files for details on commands)

    if args.macwifi is True:
        print('\n' + '*'*columns + '\n\tInstalling Mac Wi-Fi Drivers...\n' + '*'*columns + '\n')
        tmi.process_commands(macwifi_commands_array)

    print('\n' + '*'*columns + '\n\tRunning Configuration Scripts...\n' + '*'*columns + '\n')

    tmi.process_commands(environment_commands)
    
    # Setup Remote Samba File Store

    print('\n' + '*'*columns + '\n\tSetup Samba Share\n' + '*'*columns + '\n')

    user_response = input('\nSetup Remote Samba Share with /mnt/remote_cifs? (Y/n)')

    if 'Y' in user_response or 'y' in user_response:
        '''
        Setup remote samba share
        '''
        # Get cifs share information
        rb_data = tmi.get_remote_backup_info()

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

    if 'pop' in os_info:
        os.system(f'dpkg --get-selections > {backup_directory}Installed_Ubuntu_Packages_$(date +%m_%d_%Y).log')
    elif 'fedora' in os_info:
        os.system(f'sudo rpm -qa > {backup_directory}Installed_Fedora_Packages_$(date  +%m_%d_%Y).log')
    elif 'manjaro' in os_info:
        os.system(f'sudo pacman -Qe > {backup_directory}Installed_Manjaro_Packages_$(date +%m_%d_%Y).log')
    else:
        pass

    # Backup Dconf (Gnome) settings
    
    print(f'\n Creating a Gnome Settings (dconf) in {backup_directory}...')
    os.system(f'dconf dump / > {backup_directory}dconf_user_settings_$(date +%m_%d_%Y).bkup')

    # Test to see if reboot is needed

    if 'pop' in os_info or 'ubuntu' in os_info:
        if tmi.test_for_file_exists('/var/run/reboot-required'):
            print('\n' + '*'*columns + '\n\tPlease reboot to complete installation\n' + '*'*columns + '\n')
    elif 'fedora' in os_info:
        os.system('sudo needs-restarting -r')
    else:
        print('\n' + '*'*columns + '\n\tInstallation Complete!\n' + '*'*columns + '\n')

if __name__ == '__main__':

    # Call CLI Parser and get command line arguments

    args = AC.CLIParser().get_args()
    tmi = TMIC.TrickMyInstall()

    # Start program
    main()