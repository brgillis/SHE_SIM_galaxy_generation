#!/usr/bin/env python

""" @file /disk2/brg/Program_Files/workspace/Generate_GalSim_Images/test_profile_generation_time.py

    Created 10 Mar 2016

    @TODO: File docstring

    ---------------------------------------------------------------------

    Copyright (C) 2016 user_name

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

import sys

import galsim

from SHE_SIM_galaxy_image_generation.utility import timing
import numpy as np


use_gaus = False

def rand(lo, hi):
    return lo + (hi - lo) * np.random.random_sample();

def main(argv):
    """ @TODO main docstring
    """

    for _i in range(100):
        hlr = rand(0.1, 0.2)
        n = rand(0.4, 6.2)
        g_shear = rand(0.01, 0.04)
        beta_deg_shear = rand(0, 180)
        g_ell = rand(0.1, 0.4)
        beta_deg_ell = rand(0, 180)

        if use_gaus:
            gal_profile = galsim.Gaussian(sigma=hlr,
                                        flux=1.)
        else:
            gal_profile = galsim.Sersic(n=n,
                                        half_light_radius=hlr,
                                        flux=1.)

        shear_ell = galsim.Shear(g=g_ell, beta=beta_deg_ell * galsim.degrees)
        shear_lensing = galsim.Shear(g=g_shear, beta=beta_deg_shear * galsim.degrees)

        gal_profile = gal_profile.shear(shear_ell + shear_lensing)



if __name__ == "__main__":
    main(sys.argv)
