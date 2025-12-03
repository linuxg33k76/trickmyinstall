#! /usr/bin/env python3

'''
Linux OS Python Setup Script
Author:  Ben C. Calvert
Date:  18 September 2021

Description:  This program configures Linux environment per YAML config found in data/.

Distros Supported:  Pop!_OS, Ubuntu, Fedora, Manjaro, CachyOS, Nobara, MacOS, WSL (Ubuntu)

Updated: 24 August 2025

'''

from logging import raiseExceptions
import logging
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

    # Declare Constants

    HOME_DIR = os.getenv("HOME")
    UNAME = os.popen('uname -s', 'r').read().strip()

    # Configure Logging
    logging.basicConfig(filename=f'{HOME_DIR}/trickmyinstall.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info('Starting TrickMyInstall Script')

    logging.info(f'OS: {UNAME}')
    logging.info(f'Home Directory: {HOME_DIR}')


    if 'DARWIN' in UNAME.upper():

        os_info = SI.MacOSSystemInfo().system
        logging.info(f'OS Info: {os_info}')

    elif "MICROSOFT" in UNAME.upper():

        os_info = "WSL"
        logging.info(f'OS Info: {os_info}')

    else:

        os_info = SI.LinuxSystemInfo().system   
        logging.info(f'OS Info: {os_info}')
    
    os_desktop = SI.LinuxSystemInfo().desktop
    logging.info(f'OS Desktop: {os_desktop}')
    
    user_test = tmi.check_for_root()

    # User check - if root exit script and print error message

    if user_test is True:
        print('\n***Script Aborting...  Please execute with a privileged user other than root user.***\n')
        logging.error('Script executed as root. Aborting.')
        quit()

    # Identify Terminal Size

    terminal_width = tmi.get_terminal_width()

    if terminal_width > 120:
        columns = 120
    else:
        columns = terminal_width

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
    logging.info('Creating Backup Directory for config files...')

    if args.backup_directory == 'default':
        backup_directory = HOME_DIR + '/backup/'    
    else:
        backup_directory = args.backup_directory
    logging.info(f'Backup Directory: {backup_directory}')

    # Validate Backup Directory

    backup_dir_exists = tmi.create_backup_dir(backup_directory)

    # Fail if the backup directory creation fails

    if not backup_dir_exists:
        print('Backup Directory creation failed.  Exiting script.')
        logging.error('Backup Directory creation failed. Exiting script.')
        quit()

    # Used os_info to decide which YAML file to use

    # Test for user specified YAML config file - Default value is 'none'

    if args.yamlfile != 'none':

        # Read user specified file
        yaml_config = tmi.read_config_file(args.yamlfile)
        logging.info(f'YAML Config File: {args.yamlfile}')

    else:

        # If no user argument provided, then use defaults based on OS

        if 'ubuntu' in os_info or 'pop' in os_info:

            # Ubuntu/Pop OS setup parameters
            yaml_config = tmi.read_config_file('data/popos.yaml')
            logging.info(f'YAML Config File: {args.yamlfile}')
        
        elif 'fedora' in os_info:

            # Fedora setup parameters
            if 'KDE' in os_desktop:
                yaml_config = tmi.read_config_file('data/fedora_kde.yaml')
                logging.info(f'YAML Config File: {args.yamlfile}')
            else:
                yaml_config = tmi.read_config_file('data/fedora.yaml')
                logging.info(f'YAML Config File: {args.yamlfile}')
        
        elif 'manjaro' in os_info:

            # Manjaro setup parameters
            yaml_config = tmi.read_config_file('data/manjaro.yaml')
            logging.info(f'YAML Config File: {args.yamlfile}')

        elif 'cachyos' in os_info:
            
            # CachyOS setup parameters
            yaml_config = tmi.read_config_file('data/cachyos.yaml')
            logging.info(f'YAML Config File: {args.yamlfile}')

        elif 'nobara' in os_info:

            # Nobara setup parameters
            yaml_config = tmi.read_config_file('data/nobara.yaml')
            logging.info(f'YAML Config File: {args.yamlfile}')
        
        elif 'bazzite' in os_info:

            # Bazzite setup parameters
            yaml_config = tmi.read_config_file('data/bazzite.yaml')
            logging.info(f'YAML Config File: {args.yamlfile}')
        
        elif 'Darwin' in os_info:

            # Manjaro setup parameters
            yaml_config = tmi.read_config_file('data/macos.yaml')
            logging.info(f'YAML Config File: {args.yamlfile}')

        elif 'WSL' in os_info:

            # WSL (Ubuntu) setup parameters
            yaml_config = tmi.read_config_file('data/wsl.yaml')
            logging.info(f'YAML Config File: {args.yamlfile}')

        elif 'arch' in os_info:

            # Arch Linux setup parameters
            yaml_config = tmi.read_config_file('data/arch.yaml')
            logging.info(f'YAML Config File: {args.yamlfile}')
            
        else:
            print(os_info)
            print('OS type not found!  Exiting the system.')
            logging.error(f'OS type not found: {os_info}. Exiting.')
            tmi.process_commands(["uname -srv", "neofetch"])
            quit()

    # Configure Variables based on config files

    update_commands_array = yaml_config['Update']
    install_commamds_array = yaml_config['Packages']
    backup_commands_array = yaml_config['Backup']
    vim_commands_array = yaml_config['VimSetup']
    environment_commands = yaml_config['Environment']
    
    # Run install and setup commands

    if 'all' in args.skip:
        skip_items = 'install,update,3rdparty'  
    else:
        skip_items = ' '.join(args.skip)
    logging.info(f'Skip Items: {skip_items}')

    # Update System

    if 'update' in skip_items.lower():
        print('\n' + '*'*columns + '\n\tSkipping Update Process\n' + '*'*columns + '\n')
    else:
        print('\n' + '*'*columns + '\n\tUpdating System...\n' + '*'*columns + '\n')
        logging.info('Updating System...')

        tmi.process_commands(update_commands_array)
        logging.info('Update Process Completed.')

    # Install Packages

    if 'install' in skip_items.lower():
        print('\n' + '*'*columns + '\n\tSkipping Package Install Process\n' + '*'*columns + '\n')
    else:
        print('\n' + '*'*columns + '\n\tInstalling Additional Packages...\n' + '*'*columns + '\n')
        logging.info('Installing Additional Packages...')

        tmi.process_commands(install_commamds_array)
        logging.info('Package Install Process Completed.')

    # Install 3rd Party Packages

    if '3rdparty' in skip_items.lower():
        print('\n' + '*'*columns + '\n\tSkipping 3rd Party Package Install Process\n' + '*'*columns + '\n')
    else:
        print('\n' + '*'*columns + '\n\tInstalling Additional 3rd Party Packages...\n' + '*'*columns + '\n')
        logging.info('Installing Additional 3rd Party Packages...')

        # Python Foo:  get diretory list and filter for *.deb using Regular Expressions!
        
        if 'pop' in os_info:
            third_party_apps = [val for val in os.listdir(download_dir) if re.search(r'.deb', val)]
        elif 'fedora' in os_info:
            third_party_apps = [val for val in os.listdir(download_dir) if re.search(r'.rpm', val)]
        elif 'manjaro' in os_info:
            third_party_apps = [val for val in os.listdir(download_dir) if re.search(r'.xz', val)]
        else:
            third_party_apps = ['None']
        logging.info(f'3rd Party Apps: {third_party_apps}')

        # Print 3rdParty Apps to install

        print(f'The following 3rdParty Apps will be installed:\n\t{", ".join(third_party_apps)}')

        # Install the app(s)

        if 'pop' in os_info:

            for app in third_party_apps:
                os.system(f'sudo apt install {download_dir}{app}')
    
        elif 'fedora' in os_info:
        
            for app in third_party_apps:
                os.system(f'sudo dnf install {download_dir}{app}')
    
        elif 'manjaro' in os_info:

            for app in third_party_apps:
                os.system(f'sudo pacman -U {download_dir}{app}')

        else:
            pass
        logging.info('3rd Party App Install Process Completed.')

    # Check for new versions

    if 'update' in skip_items.lower():
        print('\n' + '*'*columns + '\n\tSkipping Update Process\n' + '*'*columns + '\n')
    else:
        print('\nUpdating system after 3rdParty App Install...\n')
        logging.info('Updating system after 3rdParty App Install...')
        
        tmi.process_commands(update_commands_array)
        logging.info('Update Process Completed.')
   
    # Set Default CLI editor...I like Vim!

    print('\n' + '*'*columns + '\n\tSetting the default editor (I like VIM)...\n' + '*'*columns + '\n')
    logging.info('Setting the default editor...')
    
    tmi.process_commands(vim_commands_array)
    logging.info('Vim Setup Process Completed.')

    # Backup Config Files & Setting up Environment (See YAML files for details on commands)

    print('\n' + '*'*columns + '\n\tBacking up configuration files prior to edits...\n' + '*'*columns + '\n')
    logging.info('Backing up configuration files...')

    tmi.process_commands(backup_commands_array)
    logging.info('Backup Process Completed.')

    print('\n' + '*'*columns + '\n\tRunning Configuration Scripts...\n' + '*'*columns + '\n')
    logging.info('Running Configuration Scripts...')

    tmi.process_commands(environment_commands)
    logging.info('Environment Setup Process Completed.')
    
    # Setup Fingerprint Reader

    if args.fingerprint is True:
        print('\n' + '*'*columns + '\n\tSetting Up Fingerprint Reader...\n' + '*'*columns + '\n')
        logging.info('Setting Up Fingerprint Reader...')
        os.system('./data/scripts/fingerprint.sh')
        logging.info('Fingerprint Setup Process Completed.')

    # Setup Remote Samba File Store

    if 'Darwin' in os_info or 'WSL' in os_info:
        pass
    else:

        print('\n' + '*'*columns + '\n\tSetup Samba Share\n' + '*'*columns + '\n')
        logging.info('Setting up Samba Share...')

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
            os.system(('grep "//{0}/{1}" /etc/fstab || echo "//{0}/{1}  /mnt/remote_cifs  cifs  credentials={2},uid={3},gid={4},file_mode=0755,dir_mode=0755  0  0 " | sudo tee -a /etc/fstab')\
                .format(rb_data['host_name'], rb_data['host_share'], samba_file, rb_data['uid'], rb_data['gid']))
        
            # Mount cifs share
            os.system('sudo systemctl daemon-reload')
            os.system('sudo mount -a')
            logging.info('Samba Share Setup Process Completed.')

        else:

            print('\nSamba Share setup aborted.')
            logging.info('Samba Share setup aborted.')


    # Performing File System Activities

    print('\n' + '*'*columns + '\n\tPerforming Files System Activites\n' + '*'*columns + '\n')
    logging.info('Performing File System Activities...')

    # Store a list of installed packages in HOME/backup (overwrite if file exists ">"; NOT append ">>")

    print(f'\nCreating a list of installed packages in {backup_directory}...')

    if 'pop' in os_info:
        os.system(f'dpkg --get-selections > {backup_directory}Installed_Ubuntu_Packages_$(date +%m_%d_%Y).log')
    elif 'fedora' in os_info:
        os.system(f'sudo rpm -qa > {backup_directory}Installed_Fedora_Packages_$(date  +%m_%d_%Y).log')
    elif 'manjaro' in os_info:
        os.system(f'sudo pacman -Qe > {backup_directory}Installed_Manjaro_Packages_$(date +%m_%d_%Y).log')
    elif 'arch' in os_info:
        os.system(f'sudo pacman -Qe > {backup_directory}Installed_Arch_Packages_$(date +%m_%d_%Y).log')
    else:
        print('No package list created - OS not supported!')
    logging.info('Package List Created.')

    # Backup Dconf (Gnome) settings
    
    if 'Darwin' in os_info or 'WSL' in os_info:
        pass
    else:
        print(f'\nCreating a Gnome Settings (dconf) in {backup_directory}...')
        logging.info(f'Creating a Gnome Settings (dconf) in {backup_directory}.')
        os.system(f'dconf dump / > {backup_directory}dconf_user_settings_$(date +%m_%d_%Y).bkup')   
        logging.info(f'Gnome Settings (dconf) Created in {backup_directory}.')
 
    # Copy Wallpapers to the user's Pictures directory

    if 'Darwin' in os_info or 'WSL' in os_info:
        pass
    else:
        print('\nCopying Wallpapers to Pictures directory...')
        logging.info('Copying Wallpapers to Pictures directory...')
        os.system('cd /home/${USER}/code && test -d wallpapers || git clone https://github.com/linuxg33k76/wallpapers')
        os.system(f'test -d {HOME_DIR}/Pictures/wallpapers || mkdir -p {HOME_DIR}/Pictures/wallpapers')
        os.system(f'rsync -av --exclude=".git" ~/code/wallpapers/ {HOME_DIR}/Pictures/wallpapers/')
        logging.info(f'Wallpapers Copied to: {HOME_DIR}/Pictures/wallpapers.')

    # Setup Git Environment

    print('\n' + '*'*columns + '\n\tSetup Global git Config\n' + '*'*columns + '\n')
    logging.info('Setting up Global git Config...')

    user_response = input('\nSetup global git configuration file? (Y/n)')

    if 'Y' in user_response or 'y' in user_response:

        print('\nSetting Up git configuration...\n')
        logging.info('Setting Up git configuration...')
        git_name, git_email = tmi.get_git_global_name_email()
        os.system(f'git config --global user.name \"{git_name}\"')
        os.system(f'git config --global user.email \"{git_email}\"')
        logging.info(f'Global git config set up using: {git_name} and {git_email}')

    else:

        print('\ngit global config setup aborted.')
        logging.info('Global git config setup aborted.')

    # Set Hostname
    print('\n' + '*'*columns + '\n\tPlease Set Hostname\n' + '*'*columns + '\n')
    logging.info('Setting Hostname...')
    
    print('\nCurrent Hostname: ' + os.popen('hostname', 'r').read().strip())
    hostname = input('\nHostname of system? (Press [Enter] to leave as is): ')
    if hostname != '':
        os.system(f'sudo hostnamectl set-hostname {hostname}')
        logging.info(f'Hostname set to: {hostname}')
    else:
        print('Hostname NOT changed.')
        logging.info('Hostname NOT changed.')
    
    # Generate SSH Keys if necessary

    print('\n' + '*'*columns + '\n\tGenerate SSH Keys\n' + '*'*columns + '\n')
    logging.info('Checking for SSH Keys and Generating if necessary...')
    os.system('./data/scripts/sshkeygen.sh')
    logging.info('SSH Key Generation/Location Completed.')
    
    # Test to see if reboot is needed and final messages

    if 'pop' in os_info or 'ubuntu' in os_info:
        if tmi.test_for_file_exists('/var/run/reboot-required'):
            print('\n' + '*'*columns + '\n\tPlease reboot to complete installation\n' + '*'*columns + '\n')
            logging.info('Please reboot to complete installation.')
    elif 'fedora' in os_info:
        os.system('sudo needs-restarting -r')
        logging.info('Please reboot to complete installation.')
    elif 'WSL' in os_info:
        print('\n\t***NOTE *** See this link to install Powerline Fonts in WSL: https://logfetch.com/wsl2-install-powerline/ \n')
        logging.info('Please reboot to complete installation.')
    else:
        print('\n' + '*'*columns + '\n\tInstallation Complete!\n' + '*'*columns + '\n')
        logging.info('Installation Complete!')

if __name__ == '__main__':

    # Call CLI Parser and get command line arguments

    args = AC.CLIParser().get_args()
    tmi = TMIC.TrickMyInstall()

    # Test for root user
    if os.getuid() == 0:
        print(f'I am (g)Root!')

    # Start program
    main()