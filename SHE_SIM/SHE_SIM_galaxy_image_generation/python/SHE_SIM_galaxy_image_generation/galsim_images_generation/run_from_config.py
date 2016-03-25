#!/usr/bin/env python

"""gen_galsim_images.py
   Created by Bryan Gillis, March 2014
   Last edited by brg, 11 Aug 2015

   Contact: brg@roe.ac.uk

   Requirements: GalSim toolkit (and its requirements).
   GalSim can be downloaded from https://github.com/GalSim-developers/GalSim, and see
   https://github.com/GalSim-developers/GalSim/wiki/Installation-Instructions for its
   installation requirements.

   This is a script to generate a set of seeded random images using the GalSim toolkit,
   suitable for Euclid benchmarking tests of shear-measurement algorithms.
   This script should be invoked with a command that points it to an appropriate
   configuration script, for instance through:

   $ python gen_galsim_images.py my_config.cfg

   See the sample configuration files included with this script for the proper format.
   It is recommended that you start with an appropriate configuration script and modify
   it to suit your purposes.

   If a configuration file is not passed to this script, it will use the set of default
   configuration values assigned in the load_default_configurations(...) function below.

   NOTE 1: If you got this script or the configuration file from someone else, check the
   output directory and change it if necessary. It can use absolute paths, and the
   folders will be created if necessary, which may result in creating a file structure
   you don't want.

   NOTE 2: If you see odd bugs in running this, it's possibly due to a parallelization bug.
   This script assumes that all of the process it calls are not parallelized, and if they
   are, it can lead to clashes between threads. You can try fixing this by setting the
   following environmental variables before run (which one is actually needed depends on
   the specifics of your installation):
       export MKL_NUM_THREADS=1
       export NUMEXPR_NUM_THREADS=1
       export OPENBLAS_NUM_THREADS=1
    If this doesn't work, please let me know at brg@roe.ac.uk, and I'll try to figure out
    what's going on.
"""

profile = True

import pickle
import subprocess

from galsim_images_generation import magic_values as mv
from galsim_images_generation.generate_images import generate_images
import pyfftw


if profile:
    import cProfile



def run_from_config_file(config_file_name):

    if config_file_name == "":
        from galsim_images_generation.config.config_default import load_default_configurations
        survey, options = load_default_configurations()

    else:

        # Open and read in the config file
        with open(config_file_name, 'r') as config_file:

            # Read in the file, except for comment lines
            config_lines = []
            for config_line in config_file:
                if((config_line[0] != '#') and (len(config_line.strip()) > 0)):
                    config_lines.append(config_line.strip())

            # Get configuration file version from first line
            version = str(config_lines[0].split()[-1])

            # Check which configuration file version it is. This allows potential backwards-compatibility with
            # older config files.
            if(version == '2.0'):

                from galsim_images_generation.config.config_v2_0 import load_config_2_0
                survey, options = load_config_2_0(config_lines[1:])

            else:
                raise Exception("Unsupported config file version or improperly formatted"
                + "configuration file. Please check sample files and ensure it has"
                + "one of the proper formats and versions.")

            # End reading in the configuration file

    # Ensure the base output folder exists
    # At present there's no checking before trying to create it, so an error will
    # be printed if it already exists. This can be disregarded.

    # Check if the folder path was given with a slash at the end. If so, trim it
    if(options['output_folder'][-1] == '/'):
        options['output_folder'] = options['output_folder'][0:-1]

    # Ensure that the output folder exists
    cmd = 'mkdir -p ' + options['output_folder']
    subprocess.call(cmd, shell=True)

    # Set up pyfftw
    pyfftw.interfaces.cache.enable()
    try:
        pyfftw.import_wisdom(pickle.load(open(mv.fftw_wisdom_filename, "rb")))
    except IOError as _e:
        pass

    if profile:
        def run_generate_images():
            generate_images(survey, options)
        # We have the input we want, now generate the images
        cProfile.runctx('run_generate_images()', None, locals(),
                        filename="profiling_data.prof", sort="time")
    else:
        # We have the input we want, now generate the images
        generate_images(survey, options)

    # Save fftw wisdom
    pickle.dump(pyfftw.export_wisdom(), open(mv.fftw_wisdom_filename, "wb"))

    return
