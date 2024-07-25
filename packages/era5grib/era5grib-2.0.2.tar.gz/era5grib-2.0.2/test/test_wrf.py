#!/g/data/hh5/public/apps/nci_scripts/python-analysis3
# Copyright 2020 Scott Wales
# author: Scott Wales <scott.wales@unimelb.edu.au>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import era5grib
import pytest

# currently both tests are failing because of issue with to_netcdf-throttled call
@pytest.mark.xfail
def test_single_time(tmpdir):
    era5grib.era5grib_wrf(
        namelist="test/single-time.wps",
        geo="test/geo_em.d01.nc",
        output=tmpdir / "test.grib",
        source="NCI",
    )

@pytest.mark.xfail
def test_multi_time(tmpdir):
    era5grib.era5grib_wrf(
        namelist="test/multi-time.wps",
        geo="test/geo_em.d01.nc",
        output=tmpdir / "test.grib",
        source="NCI",
    )
