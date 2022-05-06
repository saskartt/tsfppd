"""
Copyright 2022 University of Helsinki

This file is part of tsfppd.

tsfppd is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Foobar is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Foobar.
If not, see <https://www.gnu.org/licenses/>.

Authors:
Sasu Karttunen, University of Helsinki <sasu.karttunen@helsinki.fi>
"""


class Field():
    """
    Base class for both static and dynamic input fields.
    """
    def __init__(self, name, long_name, coords, fill_value, units):
        self.name = name
        self.long_name = long_name
        self.coords = coords
        self.fill_value = fill_value
        self.units = units
