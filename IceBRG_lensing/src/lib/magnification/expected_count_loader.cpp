/**********************************************************************\
 @file expected_count_loader.cpp
 ------------------

 TODO <Insert file description here>

 **********************************************************************

 Copyright (C) 2014  Bryan R. Gillis

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

 \**********************************************************************/


#include "IceBRG_lensing/magnification/detail/expected_count_loader.hpp"

#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

#include <boost/lexical_cast.hpp>

#include "IceBRG_main/common.hpp"

#include "IceBRG_main/file_access/ascii_table_map.hpp"
#include "IceBRG_main/math/misc_math.hpp"
#include "IceBRG_main/utility.hpp"
#include "IceBRG_main/vector/limit_vector.hpp"

#include "IceBRG_lensing/magnification/mag_global_values.hpp"

#undef USE_FIELD_WEIGHTING

namespace IceBRG {

// Initialisation of static vars
#if (1)
bool expected_count_loader::_loaded_(false);

IceBRG::limit_vector<flt_t> expected_count_loader::_z_limits_;
std::vector<IceBRG::limit_vector<flt_t>> expected_count_loader::_mag_limits_;
std::vector<std::vector<custom_unit_type<0,0,0,-2,0>>> expected_count_loader::_smoothed_count_;
std::vector<std::vector<custom_unit_type<0,0,0,-2,0>>> expected_count_loader::_smoothed_count_derivative_;

std::string expected_count_loader::_filename_base_("/disk2/brg/git/CFHTLenS_cat/Data/magnitude_hist_gz");
std::string expected_count_loader::_filename_tail_(".dat");

#ifdef USE_FIELD_WEIGHTING
#define COUNT_COLUMN "weighted_count"
#else
#define COUNT_COLUMN "count"
#endif

#endif

void expected_count_loader::_load()
{
	if(_loaded_) return;

	#ifdef _OPENMP
	#pragma omp critical(brg_expected_count_loader_load)
	#endif
	{

	if(!_loaded_)
	{

		_z_limits_.reconstruct(limit_vector<flt_t>::type::LINEAR, mag_z_min, mag_z_max, round_int((mag_z_max-mag_z_min)/mag_z_step));

		// Resize arrays as necessary
		size_t num_z_bins = _z_limits_.num_bins();

		_mag_limits_.resize(num_z_bins);
		_smoothed_count_.resize(num_z_bins);
		_smoothed_count_derivative_.resize(num_z_bins);

		// Loop over z, loading in all files
		for(size_t z_i=0; z_i<num_z_bins; ++z_i)
		{
			const int_t z1000(IceBRG::round_int(1000*_z_limits_.lower_limit(z_i)));
			const std::string filename(_filename_base_ + boost::lexical_cast<std::string>(z1000)
					+ _filename_tail_);

			try
			{
				auto table_map = IceBRG::load_table_map<flt_t>(filename);
				std::vector<flt_t> temp_mag_limits = table_map.at("mag_bin_lower");
				// Add a final value to the _mag_limits_ vector
				temp_mag_limits.push_back(2*temp_mag_limits.back()-
						temp_mag_limits.at(ssize(temp_mag_limits)-2));
				_mag_limits_[z_i] = std::move(temp_mag_limits);

				ssize_t size = _mag_limits_.size()-1;

				_smoothed_count_[z_i].resize(size);
				_smoothed_count_derivative_[z_i].resize(size);

				auto const & count_col = table_map.at(COUNT_COLUMN);
				auto const & deriv_col = table_map.at("smoothed_alpha");

				for(int mag_i=0; mag_i<size; ++mag_i)
				{
					_smoothed_count_[z_i][mag_i] =
							units_cast<custom_unit_type<0,0,0,-2,0>>(count_col[mag_i]);
					_smoothed_count_derivative_[z_i][mag_i] =
							units_cast<custom_unit_type<0,0,0,-2,0>>(deriv_col[mag_i]);
				}
			}
			catch(const std::runtime_error &e)
			{
				std::cerr << "ERROR: Cannot load data for expected_count_loader. Check that the filename\n"
						<< "base and root match the data (including path), and the z limits are set up to match.\n"
						<< "Original exception:" << e.what();
				throw;
			}

			// Normalize by magnitude bin size
			flt_t bin_size = _mag_limits_[z_i].at(1)-_mag_limits_[z_i].at(0);
			_smoothed_count_[z_i] = IceBRG::divide(_smoothed_count_[z_i],bin_size);

		} // Loop over z, loading in all files

		_loaded_ = true;

	}

	}
} // void expected_count_loader::_load()


custom_unit_type<0,0,0,-2,0> expected_count_loader::_get_interp(const flt_t & mag, const flt_t & z,
		const std::vector<std::vector<custom_unit_type<0,0,0,-2,0>>> & table, const custom_unit_type<0,0,0,-2,0> & )
{
	// Load if necessary
	_load();

	ssize_t z_i = _z_limits_.get_bin_index(z);

	if(z_i>=_z_limits_.num_bins()-1) z_i=_z_limits_.num_bins()-2;
	const flt_t & z_lo = _z_limits_.lower_limit(z_i);
	const flt_t & z_hi = _z_limits_.upper_limit(z_i);

	flt_t tot_weight;
	custom_unit_type<0,0,0,-2,0> temp_result;

	// Get the interpolated value at both the lower redshift and the higher

	// At the lower redshift first
	custom_unit_type<0,0,0,-2,0> lo_result;
	lo_result = _mag_limits_[z_i].interpolate_bins(mag,table[z_i]);

	// At the higher redshift now
	custom_unit_type<0,0,0,-2,0> hi_result;
	hi_result = _mag_limits_[z_i+1].interpolate_bins(mag,table[z_i+1]);

	// And now interpolate between these results

	tot_weight = z_hi-z_lo;

	temp_result = lo_result * (z_hi-z) + hi_result * (z-z_lo);
	return temp_result / tot_weight;

} // flt_t expected_count_loader::_get_interp(...)

// Setting parameters for where the data can be loaded from
#if(1)
void expected_count_loader::set_z_limits(const std::vector<flt_t> & new_limits_vector)
{
	if(!is_monotonically_increasing(new_limits_vector))
	{
		throw std::logic_error("New z_limits vector must be monotonically increasing.");
	}
	_z_limits_ = new_limits_vector;
}
void expected_count_loader::set_z_limits(std::vector<flt_t> && new_limits_vector)
{
	if(!is_monotonically_increasing(new_limits_vector))
	{
		throw std::logic_error("New z_limits vector must be monotonically increasing.");
	}
	_z_limits_ = std::move(new_limits_vector);
}
void expected_count_loader::set_filename_base(const std::string & new_filename_base)
{
	_filename_base_ = new_filename_base;
}
void expected_count_loader::set_filename_base(std::string && new_filename_base)
{
	_filename_base_ = std::move(new_filename_base);
}
void expected_count_loader::set_filename_tail(const std::string & new_filename_tail)
{
	_filename_tail_ = new_filename_tail;
}
void expected_count_loader::set_filename_tail(std::string && new_filename_tail)
{
	_filename_tail_ = std::move(new_filename_tail);
}
#endif // Setting parameters for where the data is

// Access data
#if(1)

custom_unit_type<0,0,0,-2,0> expected_count_loader::get_count(const flt_t & mag, const flt_t & z)
{
	return _get_interp(mag,z,_smoothed_count_);
}
custom_unit_type<0,0,0,-2,0> expected_count_loader::get_derivative(const flt_t & mag, const flt_t & z)
{
	return _get_interp(mag,z,_smoothed_count_derivative_,units_cast<custom_unit_type<0,0,0,-2,0>>(1.));
}

#endif // Access data

} // end namespace IceBRG
