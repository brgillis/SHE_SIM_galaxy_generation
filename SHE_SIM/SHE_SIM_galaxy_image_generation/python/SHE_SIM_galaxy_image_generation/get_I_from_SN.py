""" @file get_flux_I_SN.py

    Created 23 Jul 2015

    Contains function "get_I_from_SN" to estimate the required intensity of
    a galaxy to provide a given signal-to-noise.

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

import numpy as np


def get_I_from_SN(galaxy_SN             ,
             galaxy_stddev_arcsec  ,
             psf_stddev_arcsec     ,
             sky_level_subtracted  ,
             sky_level_unsubtracted,
             read_noise            ,
             pixel_scale           ,
             gain                  ):
    """This function calculates flux from galaxy SN. This depends on the particular definition of SN,
       and will most likely need to be rewritten for the correct definition.
 
       The definition used here is a simplified tophat model, with the tophat containing
       ~50% of the light for a circular galaxy and PSF. This definition is used simply
       because it's easy to analytically invert.
    """

    # Estimate the half-light radius of the galaxy (using the magic number 0.674490, which represents the
    # sigma for a Gaussian which contains half the distribution), and use it to calculate the area within
    # the half-light aperture in arcsec
    size_of_gal = np.pi * 0.674490 * ((galaxy_stddev_arcsec) ** 2 + (psf_stddev_arcsec) ** 2)
    
    # Calculate the sky noise and read noise in the half-light aperture, remembering that noise scales with
    # the sqrt of area.
    
    # Sky level is given initially in ADU/arcsec^2. So we convert to counts by multiplying by gain, then
    # take the sqrt of counts to get noise (assuming it's Poisson). Then we scale by sqrt(size_of_gal).  
    sky_noise_behind_galaxy = np.sqrt((sky_level_subtracted + sky_level_unsubtracted) * gain * size_of_gal)
    
    # Read noise is given initially in counts/pixel. So we convert to counts per arcsec (using just pixel_scale,
    # not pixel_scale^2 since it scales with sqrt(area), and then scale by sqrt(size_of_gal)
    read_noise_behind_galaxy = read_noise * np.sqrt(size_of_gal) / pixel_scale
    
    # Total noise is sum in quadrature of the two components
    background_noise = np.sqrt(sky_noise_behind_galaxy ** 2 + read_noise_behind_galaxy ** 2)
    
    # The galaxy's S/N is calculated from both its own Poisson noise and the background noise within its
    # half-light aperture. This can be analytically inverted to give the expression below.
    I = galaxy_SN * (galaxy_SN + np.sqrt(4 * background_noise ** 2 + galaxy_SN ** 2))
    
    return I