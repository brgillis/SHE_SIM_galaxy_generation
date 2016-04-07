"""
    @file galaxy.py

    Created 11 Dec 2015

    Functions related to loading and preparing galaxy models.

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

import galsim
import numpy as np
from os.path import join

import SHE_SIM_galaxy_image_generation.magic_values as mv

from icebrgpy.function_cache import lru_cache

__all__ = ['get_galaxy_profile']

allowed_ns = np.array(( 1.8, 2.0, 2.56, 2.71, 3.0, 3.5, 4.0))

def is_target_galaxy(galaxy, options):
    """
        @brief Tells whether a galaxy meets the requirements to be a target galaxy or not
        
        @param galaxy
            <SHE_SIM.galaxy>
        @param options
            <dict> The options dictionary used for this run
        
        @returns
            <bool> Whether or not this is a target galaxy
    """
    return galaxy.get_param_value('apparent_mag_vis') <= options['magnitude_limit']

@lru_cache()
def load_galaxy_model_from_file( n, bulge=True, data_dir=mv.default_data_dir ):
    """
        @brief Cached function to load specific galaxy images. Should not be called directly.
        
        @param n
            <float> The Sersic index of the galaxy's bulge. Must be one of the specified values.
        @param bulge
            <bool> Whether we want the bulge model or not (if not, get disk model)
        @param data_dir
            <string> The directory where galaxy models are stored
        
        @returns x
            array<float> x coordinates of star particles
        @returns y
            array<float> y coordinates of star particles
        @returns z
            array<float> z coordinates of star particles
        @returns I
            array<float> Intensities of star particles
    """
    
    n_str = "%0.2f" % n

    if(bulge):
        model_filename = mv.bulge_model_head + n_str + mv.galaxy_model_tail
    else:
        model_filename = mv.disk_model_head + n_str + mv.galaxy_model_tail
        
    model = np.loadtxt(join(data_dir,mv.galaxy_model_path,model_filename))
    
    x = model[:,0]
    y = model[:,1]
    if(bulge):
        z = None
        I = model[:,2]
    else:
        z = model[:,2]
        I = model[:,3]
        
    return x, y, z, I

def load_galaxy_model( n, bulge=True, data_dir=mv.default_data_dir ):
    """
        @brief Load a galaxy model with a given sersic index.
        
        @param n
            <float> The Sersic index of the galaxy's bulge. Must be one of the specified values.
        @param bulge
            <bool> Whether we want the bulge model or not (if not, get disk model)
        @param data_dir
            <string> The directory where galaxy models are stored
        
        @returns x
            array<float> x coordinates of star particles
        @returns y
            array<float> y coordinates of star particles
        @returns z
            array<float> z coordinates of star particles
        @returns I
            array<float> Intensities of star particles
    """
    diffs = np.abs(allowed_ns - n)
    i_best = np.argmin(diffs)
    
    return load_galaxy_model_from_file( allowed_ns[i_best], bulge, data_dir=data_dir )

def rotate( x, y, theta_deg ):
    """
        @brief Rotates a pair of coordinate arrays by a given angle
        
        @param x
            <array<float>> The first array
        @param y
            <array<float>> The second array
        @param theta_deg
            <float> The rotation angle in degrees
            
        @returns new_x
            <array<float>> The new coordinates in the axis of the first array
        @returns new_y
            <array<float>> The new coordinates in the axis of the second array
    """
    
    theta = theta_deg * np.pi/180
    sin_theta = np.sin(theta)
    cos_theta = np.cos(theta)

    new_x, new_y = ( x * cos_theta - y * sin_theta ,
                     x * sin_theta + y * cos_theta )
    
    return new_x, new_y

def shear( x, y, g, beta_deg ):
    """
        @brief Shears a pair of coordinate arrays by a given amount
        
        @param x
            <array<float>> The first array
        @param y
            <array<float>> The second array
        @param g
            <float> The shear magnitude, using definition g = (1-r)/(1+r), where r is the axis ratio.
        @param beta_deg
            <float> The shear angle in degrees
            
        @returns new_x
            <array<float>> The new coordinates in the axis of the first array
        @returns new_y
            <array<float>> The new coordinates in the axis of the second array
    """
    
    beta = beta_deg * np.pi/180
    sin_2beta = np.sin(2*beta)
    cos_2beta = np.cos(2*beta)

    new_x, new_y = ( x + g*(x * cos_2beta + y * sin_2beta) ,
                     y + g*(x * sin_2beta - y * cos_2beta) )
    
    return new_x, new_y

def get_half_light_radius( x, y, I ):
    """
        @brief Gets the half-light radius of a set of coordinate arrays and their intensity.
        
        @details This requires that the intensity already be normalized.
        
        @param x
            <array<float>> The first coordinate array
        @param y
            <array<float>> The second coordinate array
        @param I
            <array<float>> The intensities of each particle
            
        @returns 
            <float> The half-light radius in the units of the coordinate arrays
    """
    
    r = np.sqrt( np.square(x) + np.square(y) )
            
    r_step = 0.001*np.max(r)
    
    goal_I = 0.5
    cur_I = 0
    
    test_r = r_step
    while(cur_I<goal_I):
        cur_I = I[r < test_r].sum()
        test_r += r_step
    
    return test_r - r_step/2

def get_target_galaxy_profile( sersic_index,
                        half_light_radius,
                        bulge,
                        **kwargs ):
    """ 
    """
    
    if bulge:
        return get_bulge_galaxy_profile(sersic_index, half_light_radius, **kwargs)
    else:
        return get_disk_galaxy_image(sersic_index, half_light_radius, **kwargs)

def get_background_galaxy_profile( sersic_index,
                        half_light_radius,
                        bulge,
                        **kwargs ):
    """ 
    """
    
    # Always use the faster get_bulge_galaxy_profile for background galaxies
    return get_bulge_galaxy_profile(sersic_index, half_light_radius, **kwargs)

def discretize(n,res=0.05):
    return res*(int(n/res)+0.5)
    
def get_bulge_galaxy_profile(sersic_index,
                             half_light_radius,
                             flux=1.,
                             g_ell=0.,
                             beta_deg_ell=0.,
                             g_shear=0.,
                             beta_deg_shear=0.,
                             ):
    n = discretize(sersic_index)
    
    gal_profile = galsim.Sersic(n=n,
                                half_light_radius=half_light_radius,
                                flux=flux)
    
    g_ell = 0
    shear_ell = galsim.Shear(g=g_ell,beta=beta_deg_ell*galsim.degrees)
    shear_lensing = galsim.Shear(g=g_shear,beta=beta_deg_shear*galsim.degrees)
     
    gal_profile = gal_profile.shear(shear_ell+shear_lensing)
    
    return gal_profile
    
    
def get_disk_galaxy_image(sersic_index,
                          half_light_radius,
                          stamp_size_factor=4.5,
                          rotation=0.,
                          tilt=0.,
                          spin=0.,
                          flux=1.,
                          data_dir=mv.default_data_dir,
                          image_scale=mv.default_pixel_scale,
                          g_shear=0.,
                          beta_deg_shear=0.,
                          xp_sp_shift=0,
                          yp_sp_shift=0,
                          subsampling_factor=1):
    
    gal_x, gal_y, gal_z, gal_I = load_galaxy_model(sersic_index, False, data_dir)
    
    # Apply spin, tilt, and rotation
    gal_x, gal_y = rotate( gal_x, gal_y, spin )
    gal_x, gal_z = rotate( gal_x, gal_z, tilt )
    gal_x, gal_y = rotate( gal_x, gal_y, -rotation ) # Rotation is opposite here due to transposed ordering
    
    # Apply shear
    
    gal_x, gal_y = shear( gal_x, gal_y, g_shear, 90-beta_deg_shear ) # Again, transposed ordering
    
    # Normalize the flux
    gal_I /= np.sum(gal_I)
    
    # Get the half-light radius
    gal_hlr = get_half_light_radius( gal_x, gal_y, gal_I )
    image_hlr = subsampling_factor*half_light_radius / image_scale # hlr in pixels
    gal_scale = image_hlr / gal_hlr
    
    image_size = 2*subsampling_factor*int(stamp_size_factor*image_hlr+1)
    
    # Create a binned image of the galaxy
    gal_data = np.zeros((image_size,image_size))
    image_midpoint = (image_size - 1) // 2
    
    for x, y, I in zip(gal_x, gal_y, gal_I):
        dx = x * gal_scale + xp_sp_shift
        dy = y * gal_scale + yp_sp_shift
        
        xp = image_midpoint + int(dx + 0.5 * (1 if dx >= 0 else -1))
        yp = image_midpoint + int(dy + 0.5 * (1 if dy >= 0 else -1))
        
        if (xp<0) or (yp<0) or (xp>=image_size) or (yp>=image_size):
            continue
        
        gal_data[xp,yp] += I
    
    return gal_data