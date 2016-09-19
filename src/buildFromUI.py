#!/usr/bin/env python
# encoding: utf-8
'''
tools.buildFromUI -- use pyuic4 to convert UI files from QT to python files

tools.buildFromUI is a description

It defines classes_and_methods

@author:     Ricc

@copyright:  2016 RBE All rights reserved.

@license:    GPL license

@contact:    user_email
@deffield    updated: Updated
'''

import sys
import os
import glob

# import argparse
import subprocess
import yaml

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

__all__ = []
__version__ = '0.2a'
__date__ = '2016-08-13'
__updated__ = '2016-08-14'

DEBUG = 1
TESTRUN = 0
PROFILE = 0

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg
    
def main(argv=None):

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    display_info(program_name)
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by user_name on %s.
  Copyright 2016 organization_name. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-c", "--config", dest="config", required=True, help="recurse into subfolders [default: %(default)s]")
        parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %(default)s]")
        parser.add_argument('-V', '--version', action='version', version=program_version_message)

        # Process arguments
        args = parser.parse_args()

        verbose = args.verbose
        config_name = args.config

        if verbose > 0:
            print("Verbose mode on")

#         if os.path.exists(config_file):
#             raise CLIError("Configuration file: [" + config_file + "] file not found!")

        # MAIN BODY #
        options = load_config(config_name);
        process_ui_files(options)

    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception, e:
        if DEBUG or TESTRUN:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2


def load_config(config_name):
    
    with open(".buildFromUI.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    
    cfg = cfg[config_name]
    option = {}
    option['indir'] = cfg['src'] + cfg['in']
    option['outdir'] = cfg['src'] + cfg['out']
    option['srcdir'] = cfg['src']
    option['exe'] = False
    if ( cfg.has_key('exe') ):
        if ( cfg['exe'] ):
            option['exe'] = True
            
        
    return option
    
def process_ui_files(config):       
    process_files = glob.glob(config['indir'] + "/*.ui")
    
    print "Source:      " + config['indir']
    print "Destination: " + config['outdir'] + "\n"
    
    for myFile in process_files:
        path_fname = list(os.path.split(os.path.abspath(myFile)))
        print "Converting\n\tfile: " + path_fname[1]
        
        outfname = os.path.splitext(path_fname[1])[0]
        print "\t  to: " + outfname 
        
        outfname = config['outdir'] + outfname + ".py"
        cmd = build_cmd(myFile, outfname, config['exe'])
        return_code = subprocess.call(cmd, shell=True)
        
        if (return_code == 0):        
            print "pyuic4 conversion: success"
        else:
            print "pyuic4 conversion: failed code " + return_code 
     
        print ""
     
     
def build_cmd(in_file, out_file, exe):
    cmd = "pyuic4 "
    if (exe):
        cmd = cmd + "-x "
    
    cmd = cmd + in_file + " -o " +  out_file
     
    return cmd
         
def display_info(program_name):
         
    print program_name + " written by Ricc Ballard"
    print "version: " + __version__ + " created on: " + __date__
    print "Last updated on: " + __updated__ + "\n" 
     
     
     
     
if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-v")
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'tools.buildFromUI_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())
    
       
    
    
    