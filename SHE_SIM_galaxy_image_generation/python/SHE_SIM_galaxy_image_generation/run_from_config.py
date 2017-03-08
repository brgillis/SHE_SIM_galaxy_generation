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

import subprocess

from SHE_SIM_galaxy_image_generation import magic_values as mv
from SHE_SIM_galaxy_image_generation.config.config_default import (allowed_options,
                                                            allowed_fixed_params,
                                                            allowed_survey_settings,
                                                            generation_levels,
                                                            generation_levels_inverse)
from SHE_SIM_galaxy_image_generation.generate_images import generate_images
from icebrgpy.logging import getLogger


try:
    import pyfftw
    import pickle
    have_pyfftw = True
except ImportError as _e:
    have_pyfftw = False

def clean_quotes(s):
    if not isinstance(s, basestring): return s

    if s[0] == "'" and s[-1] == "'":
        s = s[1:-1]
    if s[0] == '"' and s[-1] == '"':
        s = s[1:-1]

    return s


def run_from_config_file(config_file_name):

    survey, options = set_up_from_config_file(config_file_name)

    run_from_survey_and_options(survey, options)

    return

def run_from_config_file_and_args(config_file_name, args):

    survey, options = set_up_from_config_file(config_file_name)

    apply_args(survey, options, args)

    run_from_survey_and_options(survey, options)

    return

def run_from_survey_and_options(survey, options):

    # Check if the folder path was given with a slash at the end. If so, trim it
    if(options['output_folder'][-1] == '/'):
        options['output_folder'] = options['output_folder'][0:-1]

    logger = getLogger(mv.logger_name)

    # Print all options we're using to the logger
    logger.info("# Generating images with the following options: #")
    logger.info("")
    for name in options:
        logger.info(name + ": " + str(options[name]))
        logger.info("")

    # Print survey settings and levels too
    logger.info("# And using the following settings for the physical model: #")
    logger.info("")
    for name in allowed_survey_settings:

        gen_level = generation_levels_inverse[int(survey.get_generation_level(name))]
        logger.info(name + " generation level: " + gen_level)

        param_params = survey.get_param(name).get_params()
        pp_mode = param_params.name()
        logger.info(name + " generation mode: " + pp_mode)
        pp_params = param_params.get_parameters_string()
        logger.info(name + " generation parameters: " + pp_params)

        logger.info("")

    # Ensure that the output folder exists
    cmd = 'mkdir -p ' + options['output_folder']
    subprocess.call(cmd, shell=True)

    # Set up pyfftw
    if have_pyfftw:
        pyfftw.interfaces.cache.enable()
        try:
            pyfftw.import_wisdom(pickle.load(open(mv.fftw_wisdom_filename, "rb")))
        except IOError as _e:
            pass

    # We have the input we want, now generate the images
    generate_images(survey, options)

    # Save fftw wisdom
    if have_pyfftw:
        pickle.dump(pyfftw.export_wisdom(), open(mv.fftw_wisdom_filename, "wb"))

    return

def set_up_from_config_file(config_file_name):

    if config_file_name == "":
        from SHE_SIM_galaxy_image_generation.config.config_default import load_default_configurations
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

                from SHE_SIM_galaxy_image_generation.config.config_v2_0 import load_config_2_0
                survey, options = load_config_2_0(config_lines[1:])

            else:
                raise Exception("Unsupported config file version or improperly formatted"
                + "configuration file. Please check sample files and ensure it has"
                + "one of the proper formats and versions.")

            # End reading in the configuration file

    return survey, options

def apply_args(survey, options, args):

    arg_lib = vars(args)

    # Check if each option was overriden in the args
    for option in allowed_options:
        if option in arg_lib:
            if arg_lib[option] is not None:
                options[option] = clean_quotes(arg_lib[option])

    # Add allowed fixed params
    for fixed_param in allowed_fixed_params:
        if fixed_param in arg_lib:
            if arg_lib[fixed_param] is not None:
                survey.set_param_params(fixed_param, 'fixed', clean_quotes(arg_lib[fixed_param]))


    # Add allowed survey settings, with both level and setting possibilities
    for param_name in allowed_survey_settings:

        generation_level_name = param_name + "_level"
        if generation_level_name in arg_lib:
            if arg_lib[generation_level_name] is not None:
                survey.set_generation_level(param_name,
                                            generation_levels[clean_quotes(arg_lib[generation_level_name])])


        settings_name = param_name + "_setting"
        if settings_name in arg_lib:
            if arg_lib[settings_name] is not None:

                split_params = clean_quotes(arg_lib[settings_name]).split()

                flt_args = []
                for str_arg in split_params[1:]:
                    flt_args.append(float(str_arg.strip()))

                survey.set_param_params(param_name, split_params[0].strip(), *flt_args)
        else:
            assert(False)

    return
