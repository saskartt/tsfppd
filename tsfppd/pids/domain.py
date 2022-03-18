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

import warnings
from pyproj import CRS

class Domain:
    """
    Base class for domains. Used for root instance.
    """
    def __init__(self, domain_id, epsg=None, npe=None, origin=None, shape=None, resolution=None):
        """
        Initialize Domain object.

        Parameters
        ----------
        domain_id
        crs
        epsg
        pe
        orig_x
        orig_y
        nx
        ny
        nz
        dx
        dy
        dz
        """
        if isinstance(domain_id, int):
            self.id = domain_id
        else:
            raise ValueError(f"Expected integer domain id, got {domain_id}")

        # Grid mapping setup
        self.epsg = epsg
        self.crs = None
        self.origin = origin
        if self.origin is not None:
            self._validate_origin()
        if self.epsg is not None:
            self.set_mapping(epsg)

        # Grid shape and resolution
        self.shape = shape
        if self.shape is not None:
            self._validate_shape()
        self.resolution = resolution
        if self.resolution is not None:
            self._validate_resolution()

        # Number of processor elements number in x and y directions
        self.npe = npe

        self.children = []
        self.children_ids = []
        self._has_children = False

    def add_child(self, child):
        """
        Registers a child domain for self.
        Parameters
        ----------
        child

        """
        if ~isinstance(child, ChildDomain):
            raise ValueError(f"Expected ChildDomain instance, got {type(child)} instead.")

        self.register_id(child.id)
        child.set_parent(self)
        self.children.append(child)
        self._has_children = True

    def set_mapping(self, epsg):
        self.crs = CRS.from_epsg(self.epsg)

    def set_origin(self, origin):
        self.origin = origin
        self._validate_origin()

    def set_shape(self, shape):
        self.shape = shape
        self._validate_shape()

    def set_resolution(self, resolution):
        self.resolution = resolution
        self._validate_resolution()

    def set_pe(self, pe):
        self.npe = pe

    def generate_grid(self):
        pass

    def remove_child(self, child):
        """
        Removes a child domain from self.
        Parameters
        ----------
        child
        """
        if ~isinstance(child, ChildDomain):
            raise ValueError(f"Expected ChildDomain instance, got {type(child)} instead.")

        try:
            self.children.remove(child)
            self.children_ids.remove(child.id)
        except ValueError:
            warnings.warn(f"ChildDomain {child.id} is not a child of {self.id}.")

        if len(self.children) == 0:
            self._has_children = False

    def register_id(self, domain_id):
        """
        # Registers id to be in use.
        Parameters
        ----------
        domain_id
        """
        if domain_id in self.children_ids:
            raise ValueError(f"ChildDomain id {domain_id} already in use.")

        self.children_ids.append(domain_id)

    def add_static_field(self):
        pass

    def add_dynamic_field(self):
        pass

    def _validate_origin(self):
        if (len(self.origin) != 2) or (None in self.origin):
            raise ValueError(f"Invalid origin specified.")

    def _validate_shape(self):
        if (len(self.shape) != 3) or (None in self.shape):
            raise ValueError(f"Invalid shape specified.")

    def _validate_resolution(self):
        if (len(self.resolution) != 3) or (None in self.resolution):
            raise ValueError(f"Invalid shape specified.")

    def _validate_grid_config(self):
        self._validate_origin()
        self._validate_shape()
        self._validate_resolution()
        self._validate_npe()



class ChildDomain(Domain):
    """
    Class for the child domains.
    """
    def __init__(self, domain_id, offset_x=None, offset_y=None, **kwargs):
        """
        Initialize ChildDomain object.
        Parameters
        ----------
        domain_id
        """
        super().__init__(domain_id, **kwargs)

        self.parent = None

        # The offset of origin with respect to parent.
        self.offset_x = None
        self.offset_y = None

        if None in (self.offset_x, self.offset_y):
            self._orig_set = False
        else:
            self._orig_set = True

    def set_parent(self, parent):
        self.parent = parent

    def register_id(self, domain_id):
        """
        Wrapper around base class function for registering the domain id.
        The root domain keeps account of all domain ids in use.
        Parameters
        ----------
        domain_id
        """
        self.parent.register_id(domain_id)
        self.children_ids.append(domain_id)

