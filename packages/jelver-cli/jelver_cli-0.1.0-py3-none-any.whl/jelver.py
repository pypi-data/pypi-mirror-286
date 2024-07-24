#!/usr/bin/env python3

"""Usage: 
  jelver test --api-key=<api-key> [<web> <username> <password>] 
  jelver cases ls --api-key=<api-key>
  jelver cases add <case_ids> --api-key=<api-key> 
  jelver cases rm <case_ids> --api-key=<api-key>
  jelver (-h | --help)

Description:
    Most of the commands to run the end-to-end tests from your application. 

Commands:
  test                 Run the all the tests recorded from your application
  cases ls             List all the cases that are recorded from your application
  cases add            Include the cases that you want to test
  cases rm             Exclude the cases that you don't want to test

Arguments:  
  case_ids             The case ids that you want to include
                       or exclude, they must be separated by a comma (ex: 1,2,344)   
  web                  The URL of the website to be tested 
  username             The username to be used to login
  password             The password to be used to login

Options:
  -h --help
  --api-key=<api-key>  The API key to authenticate the user 


"""

import sys
from docopt import docopt
from remote_tests import RemoteTests
from cases_management import CasesManagement
from utils.jelver_exceptions import JelverAPIException

def main():
    """
    Main function that runs a command based on the arguments

    Arguments:
    :args: None 

    Return: None
    """
    args = docopt(__doc__, version='0.1.0')

    if args['--api-key'] is None:
        raise JelverAPIException("You must provide an API key to authenticate the user")

    if args['test']:
        RemoteTests(
            url=args['<web>'],
            username=args['<username>'],
            password=args['<password>'],
            api_key=args["--api-key"]
        ).run()
    elif args['cases']:
        if args['ls']:
            CasesManagement(args["--api-key"]).list()
        elif args['add']:    
            CasesManagement(args["--api-key"]).add(args['<case_ids>']) 
        elif args['rm']:    
            CasesManagement(args["--api-key"]).remove(args['<case_ids>'])
    else:
        sys.argv.append('-h')
        docopt(__doc__, version=1)



if __name__ == '__main__':
    main()
