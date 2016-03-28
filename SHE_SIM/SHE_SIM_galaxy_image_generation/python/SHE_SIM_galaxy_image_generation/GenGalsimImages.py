# #
# @file: python/SHE_SIM_galaxy_image_generation/GenGalsimImages.py
# @author: BRG
# @date: 25/3/16
# #

import argparse
import ElementsKernel.Logging as log

from SHE_SIM_galaxy_image_generation.config.config_default import (allowed_options,
                                                            allowed_fixed_params,
                                                            allowed_survey_settings,
                                                            str2bool)

def defineSpecificProgramOptions():
    """
    @brief Allows to define the (command line and configuration file) options
    specific to this program

    @details
        See the Elements documentation for more details.
    @return
        An  ArgumentParser.
    """

    parser = argparse.ArgumentParser()

    parser.add_argument('--config-file', type=str, default="",
                        help='Filename of the configuration file to use.')

    # Add in each allowed option, with a null default
    for option in allowed_options:
        type = allowed_options[option][1]
        if type == str2bool:
            type = bool
        parser.add_argument(option, type=type)

    # Add allowed fixed params
    for allowed_fixed_param in allowed_fixed_params:
        parser.add_argument(allowed_fixed_param, type=float)

    # Add allowed survey settings, with both level and setting possibilities
    for allowed_survey_setting in allowed_survey_settings:

        generation_level = allowed_survey_setting + "_level"
        parser.add_argument(generation_level, type=str)

        settings = allowed_survey_setting + "_setting"
        parser.add_argument(settings, type=str)

    return parser


def mainMethod(args):
    """
    @brief The "main" method.
    @details
        This method is the entry point to the program. In this sense, it is
        similar to a main (and it is why it is called mainMethod()).
    """

    logger = log.getLogger()

    logger.info('#')
    logger.info('# Entering GenGalsimImages mainMethod()')
    logger.info('#')

    args.parse_args()

    config_filename = args.config_filename

    if(config_filename == ""):
        logger.info('Using default configurations.')
    else:
        logger.info('Using configurations from file ' + config_filename + '.')

    run_from_config_file(config_file_name)

    logger.info('Exiting GenGalsimImages mainMethod()')
