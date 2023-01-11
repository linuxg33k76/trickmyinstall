#!/usr/bin/env python3

import os
import re
import getpass
import yaml

class TrickMyInstall():

    def __init__(self):
        pass


    def check_for_root(self):

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


    def validate_dir(self, dir_path):

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


    def create_backup_dir(self, backup_dir):

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


    def test_for_file_exists(self, file):
        
        '''
        Test for file existance.

        file: string (complete path to file)

        return: bool
        '''
        
        if os.path.isfile(file):
            return True
        else:
            return False


    def create_file(self, file):
        
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


    def read_config_file(self, file):

        '''
        Read data from config file - in YAML format

        file: string (complete path to file)

        return: array of strings
        '''

        with open(file, 'r') as rf:
            return yaml.safe_load(rf)


    def process_commands(self, commands_array):
        '''
        Process commands in array

        commands_array: array of strings

        return: none
        '''
        
        for command in commands_array:
                os.system(command)


    def get_remote_backup_info(self):
        '''
        Collect System and User Input

        return: dictionary
        '''

        regex_uid = r'uid=(\d{1,4})'
        regex_gid = r'gid=(\d{1,4})'
        current_user = os.popen('whoami','r').read().strip('\n')
        id_info = os.popen('id','r').read().strip('\n')
        uid = re.findall(regex_uid, id_info)[0]
        gid = re.findall(regex_gid, id_info)[0]
   
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
            
            print(f'\n\tSamba Host IP: {host_ip}\n\tSamba Host Name: {host_name}\n\tSamba share: {host_share}\n\tSamba user: {user_cred}\n\tSamba pass: {pass_cred}\n\tSamba domain: {domain_cred}\n')
            
            response = input('Does the information look correct? (Y/n)')

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


    def get_git_global_name_email(self):
        '''
        Collect Git Global User Name and Email Input

        return: tuple
        '''

        # Collect User inputs

        invalid = True
        while invalid:
            print('Please provide your user name and email for git\'s global config file.\n')
            git_name = input('User\'s Name for git: ')
            git_email = input ('Email Address for git: ')
            
            print(f'\n\tGit User Name: {git_name}\n\tGit Email Address: {git_email}')
            
            response = input('\nDoes the information above look correct? (Y/n)')
 
            if 'Y' in response or 'y' in response:
                invalid = False
        
        results = (git_name, git_email)

        return results