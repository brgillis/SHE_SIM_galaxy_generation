""" @file gain.py

    Created 6 Oct 2015

    Functions to convert between count and intensity using gain, since I
    can never seem to remember whether to multiply or divide by it.

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

def get_I_from_count(c, gain=mv.default_gain):
    """ Calculated the intensity I from count with the given gain.
    
        @param c The electron count
        @param gain The gain
        
        @return The intensity
    """
    
    return c/gain

def get_count_from_I(I, gain=mv.default_gain):
    """ Calculated the electron count from intensity I with the given gain.
    
        @param I The intensity
        @param gain The gain
        
        @return The intensity
    """
    
    return I*gain