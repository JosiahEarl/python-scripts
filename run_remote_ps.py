#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#*********************************************************************
#
#   NAME:
#       run_remote_ps.py
#
#   AUTHOR:
#       Josiah Earl
#
#   DESCRIPTION:
#       Example script of how to run a remote powershell script
#       from a linux box
#
#
#*********************************************************************
'''

# ---------------------------------------------------------------------
#                               IMPORTS
# ---------------------------------------------------------------------
try:
    import winrm
    import logging
    import os
    import sys
except Exception as exc:
    raise Exception('Error occurred while importing modules. Error message: {err}'.format(err=exc.message))


# ---------------------------------------------------------------------
#                               CONSTANTS AND LOGGING
# ---------------------------------------------------------------------
# True = log all messages to disk and False = log only exception messages to disk
DEBUG = True

try:
    # Log file
    log_file = '/root/run_remote_ps_log.log'

    # Local file debugging output
    FORMAT = '%(asctime)s %(levelname)s %(lineno)s \t%(message)s'
    logging.basicConfig(filename=log_file, format=FORMAT, level=(logging.INFO))

    # Set script variables
    USERNAME = '<username here>'
    PASSWORD = '<password here>'
    IP_ADDRESS = '<ip address here>'
    PS_SCRIPT = '<path to PS script on remote machine>'
except Exception as exc:
    raise Exception('Error occurred while creating constants and logger. '
                    'Error message: {err}'.format(err=exc.message))

if DEBUG:
    logging.info('Set constants and created logger...')


# ---------------------------------------------------------------------
#                               PROCEDURES
# ---------------------------------------------------------------------

# *********************************************************************
#
# Procedure Name:
#   create_winrm_session
#
# Description:
#   Procedure that creates a winrm session
#
# *********************************************************************
def create_winrm_session(ip_address, username, password):
    try:
        if DEBUG:
            logging.info('Creating WinRM session...')

        # Create winrm session
        winrmsession = winrm.Session('{}'.format(ip_address), auth=('{}'.format(username), '{}'.format(password)))

        if DEBUG:
            logging.info('Created WinRM session..')

        return winrmsession
    except Exception as exc:
        logging.info('Encountered error when trying to create winrm session. Error: {}'.format(exc.message))
        raise Exception(
            'Encountered error when trying to create winrm session. Error: {}'.format(exc.message)
        )

# *********************************************************************
#
# Procedure Name:
#   exec_ps_script
#
# Description:
#   Procedure that executes a remote PS script using a winrm session
#
# *********************************************************************
def exec_ps_script(winrmsession, ps_script):
    try:
        if DEBUG:
            logging.info('Executing PS script...')

        # Run remote PS script through the winrm session
        result = winrmsession.run_cmd('powershell.exe -command {ps_script}'.format(ps_script=ps_script))

        if len(result.std_err) > 0:
            raise Exception('{}'.format(result.std_err))

        if DEBUG:
            logging.info("Result: {result}\n\nErrors: {errors}...".format(result=result.std_out, errors=result.std_err))

        return winrmsession
    except Exception as exc:
        logging.info('Encountered error when trying to create winrm session. Error: {}'.format(exc.message))
        raise Exception(
            'Encountered error when trying to create winrm session. Error: {}'.format(exc.message)
        )


# *********************************************************************
#
# Procedure Name:
#   main
#
# Description:
#   Entrypoint procedure that runs all other procedures
#
# *********************************************************************
def main():
    try:
        if DEBUG:
            logging.info('Starting procedures...')

        # Create WinRM session
        winrmsession = create_winrm_session(IP_ADDRESS, USERNAME, PASSWORD)

        # Run PS script
        exec_ps_script(winrmsession, PS_SCRIPT)

        if DEBUG:
            logging.info('Done!')
    except Exception as exc:
        print('Error encountered: {}'.format(exc.message))
        sys.exit(1)


# Entrypoint of script
if __name__ == "__main__":
    main()