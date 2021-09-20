#! /usr/bin/env python3

'''
Pop! OS Python Setup Script
Author:  Ben C. Calvert
Date:  18 September 2021

Description:  This program configures Pop! OS Linus based on configuration parameters found in the ../Data directory JSON files.

'''

import os
import httplib2
from classes import ArgsClass as AC

'''
ToDo:

1.  Collect arguments
2.  Read JSON files (or recipe files)
3.  Perform upgrade of the system
4.  Install Pop! OS Packages
5.  Install 3rd Party Packages based on URL and wget commands
6.  Configure System setting files - .vimrc, .bash_aliases, default editor, etc.

'''

def validate_dir(dir_path):
    if os.path.isdir(dir_path) == False:
            user_input = input(f'{dir_path} is not a valid path. Do you want to create (Y/N) ')
            if user_input.upper() == 'Y':
                os.mkdir(dir_path)
            else:
                print(f'{dir_path} has not been created.  Aborting.')
                quit()


def main():
    '''Main Program function'''

    # Declare Constants and Variables

    if args.directory == 'default':
        download_dir = os.getenv('HOME') + '/Downloads/popospy_downloads'
    else:
        # Validate format
        download_dir = args.directory
    validate_dir(download_dir)
        




if __name__ == '__main__':

    # Call CLI Parser and get command line arguments
    args = AC.CLIParser().get_args()
    print(args)
 

    # Start program
    main()