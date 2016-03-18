""" @file config_v2_0.py

    Created 8 Dec 2015

    @TODO: File docstring

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

from string import split

import SHE_SIM

from galsim_images_generation.config.config_default import (allowed_options,
                                                            allowed_fixed_params,
                                                            allowed_settings,
                                                            generation_levels)
from galsim_images_generation.config.check_config import (check_options,
                                                          check_survey_settings,
                                                          handle_special_settings)

__all__ = ['load_config_2_0']

def parse_option( name, value, survey, options ):
    
    if name not in allowed_options:
        
        if name in allowed_fixed_params:
            
            # Parse it as a fixed survey setting
            parse_survey_setting(name, 'setting', 'fixed '+value, survey)
            
        else:
            
            # Bad option
            raise Exception("Unrecognized option: " + name)
         
    # Save it as the appropriate type
    option_setting = allowed_options[name][1](value)
    
    # If it's a string, make it lower-case
    if isinstance(options[name], basestring):
        option_setting = option_setting.lower()
            
    options[name] = option_setting
    
    return

def parse_survey_setting( param_name, setting, parameters, survey ):
    
    if setting not in allowed_settings:
        # Bad option
        raise Exception("Unrecognized survey setting: " + setting)
    
    split_params = split(parameters)
    
    if setting == 'level':
        
        if len(split_params) != 1:
            raise Exception("Too many options passed to generation level: " + str(parameters))
        
        level = split_params[0].lower()
        if level not in generation_levels:
            raise Exception("Unrecognized generation level: " + level)
        
        survey.set_generation_level( param_name, generation_levels[level] )
        
    else:
        
        if len(split_params) < 1:
            raise Exception("No parameters passed to set survey params.")
        
        flt_args = []
        for str_arg in split_params[1:]:
            flt_args.append(float(str_arg.strip()))
            
        try:
            survey.set_param_params( param_name, split_params[0].strip(), *flt_args )
        except IndexError as _e:
            raise Exception("Unrecognized param name or param_param name.\n" +
                            "Param name: " + param_name + "\n" +
                            "Param param name: " + split_params[0])

def parse_line( line, survey, options ):
    
    # Split by comments
    no_comments_line = split(line, sep='#')[0]
    
    # Split by colon
    colon_split_line = split(no_comments_line, sep=':')
    
    # Check if this looks good
    if len(colon_split_line) != 2:
        if len(colon_split_line) < 2:
            # It's empty or only a comment, so ignore it
            return
        else:
            # More than one colon outside of comments - it's malformatted
            raise Exception("Comment line is malformatted: '" + line + "'")
        
    # Split on spaces to check the tokens before the colon
    tokens = split(colon_split_line[0])
    
    # Check if it looks good
    if len(tokens)>2:
        # More than one space before the colon - it's malformatted
        raise Exception("Comment line is malformatted: '" + line + "'")
    
    name = tokens[0].strip().lower()
    
    # Decide if we're doing an option or a survey setting
    if len(tokens)==1:
        parse_option( name, colon_split_line[1].strip(), survey, options )
    else:
        parse_survey_setting( name, tokens[1].strip(), colon_split_line[1], survey )

def load_config_2_0( config_lines ):
    
    survey = SHE_SIM.Survey()
    
    # Load default options
    options = {}
    for option in allowed_options:
        options[option] = allowed_options[option][0]
    
    # Load from the config file, overwriting defaults for any present
    for line in config_lines:
        parse_line( line, survey, options )
        
    check_options(options)
    check_survey_settings(survey)
    handle_special_settings(options,survey)
        
    return survey, options

def read_config_file( config_filename ):
    
    with open(config_filename, 'r') as config_file:
        # Read in the file, except for comment lines
        config_lines = []
        for config_line in config_file:
            if((config_line[0] != '#') and (len(config_line.strip()) > 0)):
                config_lines.append(config_line.strip())
                
    version = str(config_lines[0].split()[-1])
    
    if(version != '2.0'): 
        raise Exception("Invalid or deprecated config version: " + version)
    
    return load_config_2_0(config_lines[1:])