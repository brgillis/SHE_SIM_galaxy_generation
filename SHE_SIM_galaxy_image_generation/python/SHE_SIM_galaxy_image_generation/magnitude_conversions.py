""" 
    @file magnitude_conversions.py

    Created 6 Oct 2015

    Functions to convert between Euclid Vis magnitude and electron count

    ---------------------------------------------------------------------

    Copyright (C) 2015, 2016 Bryan R. Gillis

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

import SHE_SIM_galaxy_image_generation.magic_values as mv
import numpy as np
from gain import get_I_from_count
from SHE_SIM_galaxy_image_generation.magic_values import mag_i_zeropoint,\
    mag_vis_zeropoint
from SHE_SIM_galaxy_image_generation.gain import get_count_from_I
from SHE_SIM_galaxy_image_generation.get_I_from_SN import get_I_from_SN

def get_count_from_mag_vis(m, exp_time=mv.default_exp_time):
    """ 
        @brief Gets the expected photoelectron count from the Euclid Vis magnitude.
    
        @param m
            The Euclid Vis magnitude
        @param exp_time
            The exposure time in seconds
        
        @returns
            The expected photoelectron count
    """
    
    return exp_time * 10.0**(0.4*(mv.mag_vis_zeropoint-m))

def get_mag_vis_from_count(c, exp_time=mv.default_exp_time):
    """ 
        @brief Gets the Euclid Vis magnitude from the expected photoelectron count
    
        @param c
            The expected photoelectron count
        @param exp_time
            The exposure time in seconds
        
        @returns
            The Euclid Vis magnitude
    """
    
    return mv.mag_vis_zeropoint-2.5*np.log10(c / exp_time)

def get_count_from_mag_i(m, exp_time=mv.default_exp_time):
    """
        @brief Gets the expected photoelectron count from the i-band magnitude.
    
        @param m
            The i-band magnitude
        @param exp_time
            The exposure time in seconds
        
        @returns
            The expected photoelectron count
    """
    
    return exp_time * 10.0**(0.4*(mv.mag_i_zeropoint-m))

def get_mag_i_from_count(c, exp_time=mv.default_exp_time):
    """
        @brief Gets the i-band magnitude from the expected photoelectron count
    
        @param c
            The expected photoelectron count
        @param exp_time
            The exposure time in seconds
        
        @returns
            The i-band magnitude
    """
    
    return mv.mag_i_zeropoint-2.5*np.log10(c / exp_time)

def get_I(I_parameter, parameter_type, gain=mv.default_gain, exp_time=mv.default_exp_time):
    """ 
        @brief Gets the measured intensity in ADU from the provided parameters
    
        @param I_parameter
            Either the intensity in ADU, the photoelectron count, the photoelectron flux,
            the Euclid Vis magnitude, or the i-band magnitude
        @param parameter_type
            A string describing which parameter is used for I_parameter. One of:
            --'intensity'
            --'count'
            --'flux'
            --'mag_vis'
            --'mag_i'
        @param gain
            The gain of the observation in e-/ADU
        @param exp_time
            The exposure time in seconds
        
        @returns The measured intensity in ADU
    """
    
    if(parameter_type=='intensity'):
        return I_parameter
    elif(parameter_type=='count'):
        return get_I_from_count(I_parameter,gain)
    elif(parameter_type=='flux'):
        return get_I_from_count(I_parameter*exp_time,gain)
    elif(parameter_type=='mag_vis'):
        return get_I_from_count(get_count_from_mag_vis(I_parameter, exp_time=exp_time))
    elif(parameter_type=='mag_i'):
        return get_I_from_count(get_count_from_mag_i(I_parameter, exp_time=exp_time))
    else:
        raise Exception("get_I can't handle parameter type '" + str(parameter_type) + "'")
    return
