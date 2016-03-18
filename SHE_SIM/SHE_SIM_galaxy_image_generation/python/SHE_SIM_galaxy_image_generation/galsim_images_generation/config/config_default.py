""" @file config_default.py

    Created 23 Jul 2015

    This module defines functions for loading default configuration
    values for the Generate_GalSim_Images project.

    ---------------------------------------------------------------------

    Copyright (C) 2015 Bryan R. Gillis

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import galsim_images_generation.magic_values as mv
import SHE_SIM

__all__ = ['load_default_configurations']

# Some default values for configurations

def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")

allowed_options = { 'compress_images': (0, int),
                    'num_target_galaxies': (0, int),
                    'details_only': (False, str2bool),
                    'details_output_format': ('fits', str),
                    'dithering_scheme': ('none', str),
                    'image_datatype': (mv.default_image_datatype, str),
                    'magnitude_limit': (mv.default_magnitude_limit, float),
                    'mode': ('field', str),
                    'num_parallel_threads': (-1, int),
                    'output_folder': (mv.default_output_folder, str),
                    'output_file_name_base': ('simulated_image', str),
                    'render_background_galaxies': (True, str2bool),
                    'seed': (mv.default_random_seed, int),
                    'shape_noise_cancellation': (False, str2bool),
                    'stamp_size': (250, int),
                    'stamp_size_factor': (4.5, float),
                    'suppress_noise': (False, str2bool),
                    'gain': (3.3, float),
                    'exp_time': (565., float),
                    'read_noise': (5.4, float) }

allowed_option_values = { 'compress_images': (0, 1, 2),
                          'details_output_format': ('none', 'fits', 'ascii', 'both'),
                          'dithering_scheme': ('none', '2x2'),
                          'image_type': ('32f', '64f'),
                          'mode': ('field', 'stamps', 'cutouts')}

allowed_fixed_params = ('num_images',
                        'num_clusters',
                        'num_background_galaxies',
                        'num_fields',
                        'num_galaxies',
                        'pixel_scale',
                        'image_size_xp',
                        'image_size_yp')

allowed_settings = ( 'level',
                     'params',
                     'setting' )

generation_levels = { 'survey': 0,
                      'global': 0,
                      'image_group': 1,
                      'thread': 1,
                      'image': 2,
                      'cluster_group': 3,
                      'field_group': 3,
                      'cluster': 4,
                      'field': 4,
                      'galaxy_group': 5,
                      'group': 5,
                      'galaxy_block': 5,
                      'block': 5,
                      'galaxy_pair': 6 ,
                      'pair': 6 ,
                      'galaxy': 7 }


def load_default_configurations():
    """This function loads a default set of configuration parameters. If you wish to run
       this script without a configuration file, you can edit the parameters here. If you
       do so, ensure that all lines are entered in lower-case, which is what the program
       will be expecting.
    """
    
    print "No configuration script loaded. The script will proceed using the set of"
    print "configuration parameters hardcoded into it. These can be viewed and edited in"
    print "the file galsim_images_generation/magic_values.py."
    
    options = {}
    for option in allowed_options:
        options[option] = allowed_options[option][0]
    survey = SHE_SIM.Survey()
    
    # Set some defaults for the survey
    survey.set_param_param('num_images','fixed',mv.default_num_images)
    survey.set_param_param('pixel_scale','fixed',mv.default_pixel_scale)
    survey.set_param_param('subtracted_sky_level','fixed',mv.default_sky_level)
    survey.set_param_param('unsubtracted_sky_level','fixed',0.)
            
    return survey, options