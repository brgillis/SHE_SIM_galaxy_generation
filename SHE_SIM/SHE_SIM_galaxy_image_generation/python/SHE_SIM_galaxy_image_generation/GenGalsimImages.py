# #
# @file: python/SHE_SIM_galaxy_image_generation/GenGalsimImages.py
# @author: BRG
# @date: 25/3/16
# #

import argparse
import ElementsKernel.Logging as log

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

    parser.add_argument('--config-file', type=string, default="",
                        help='Filename of the configuration file to use.')
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

    config_filename = args.config_filename

    if(config_filename == ""):
        logger.info('Using default configurations.')
    else:
        logger.info('Using configurations from file ' + config_filename + '.')

    run_from_config_file(config_file_name)

    logger.info('Exiting GenGalsimImages mainMethod()')
