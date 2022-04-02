#!/usr/bin/env python3



import argparse


class CLIParser(argparse.ArgumentParser):

    '''
    --------------------------------------------------------------------------------
    Description:  Collect cli arguments and present help commands - an extension
    of argparse.ArgumentParser() class.
    Parameter(s):  None
    Return: None.
    --------------------------------------------------------------------------------
    '''

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('-s', '--skip', type=str, help='Skip specific task: install,update,3rdParty', default='', nargs='+')
        # self.parser.add_argument('-e', '--exclude', type=str, help='Exclude Specified Packages from package file', default='', nargs='+')
        self.parser.add_argument('-m', '--macwifi', help='Install Mac WiFi drivers.', action='store_true')
        self.parser.add_argument('-b', '--directory', type=str, help='User Specified Download Directory.', default='default')
        self.parser.add_argument('-d', '--backup_directory', type=str, help='User Specified Backup Directory.', default='default')
        self.parser.add_argument('-r', '--remote_backup_flag', help='Setup Remote Backup Location in /etc/fstab', action='store_true')
        self.parser.add_argument('-v', '--verbose', help='Display log file output', action='store_true')
        self.parser.add_argument('--test', help='Turn on test output', action='store_true')
        self.args = self.parser.parse_args()

    def get_args(self):

        '''
        --------------------------------------------------------------------------------
        Description:  Return cli arguments.
        Parameter(s):  self : instance of CLIParser() class
        Return: self.args : object
        --------------------------------------------------------------------------------
        '''

        return self.args
