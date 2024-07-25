# This file is part of daf_butler.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This software is dual licensed under the GNU General Public License and also
# under a 3-clause BSD license. Recipients may choose which of these licenses
# to use; please see the files gpl-3.0.txt and/or bsd_license.txt,
# respectively.  If you choose the GPL option then the following text applies
# (but note that there is still no warranty even if you opt for BSD instead):
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import annotations

__all__ = ("YamlFormatter",)

import contextlib
import dataclasses
from typing import Any

import yaml

from .file import FileFormatter


class YamlFormatter(FileFormatter):
    """Formatter implementation for YAML files."""

    extension = ".yaml"

    unsupportedParameters = None
    """This formatter does not support any parameters"""

    supportedWriteParameters = frozenset({"unsafe_dump"})
    """Allow the normal yaml.dump to be used to write the YAML. Use this
    if you know that your class has registered representers."""

    def _readFile(self, path: str, pytype: type[Any] | None = None) -> Any:
        """Read a file from the path in YAML format.

        Parameters
        ----------
        path : `str`
            Path to use to open YAML format file.
        pytype : `class`, optional
            Not used by this implementation.

        Returns
        -------
        data : `object`
            Either data as Python object read from YAML file, or None
            if the file could not be opened.

        Notes
        -----
        The `~yaml.SafeLoader` is used when parsing the YAML file.
        """
        try:
            with open(path, "rb") as fd:
                data = self._fromBytes(fd.read(), pytype)
        except FileNotFoundError:
            data = None

        return data

    def _fromBytes(self, serializedDataset: bytes, pytype: type[Any] | None = None) -> Any:
        """Read the bytes object as a python object.

        Parameters
        ----------
        serializedDataset : `bytes`
            Bytes object to unserialize.
        pytype : `class`, optional
            Not used by this implementation.

        Returns
        -------
        inMemoryDataset : `object`
            The requested data as an object, or None if the string could
            not be read.

        Notes
        -----
        The `~yaml.SafeLoader` is used when parsing the YAML.
        """
        data = yaml.safe_load(serializedDataset)

        with contextlib.suppress(AttributeError):
            data = data.exportAsDict()

        return data

    def _writeFile(self, inMemoryDataset: Any) -> None:
        """Write the in memory dataset to file on disk.

        Will look for `_asdict()` method to aid YAML serialization, following
        the approach of the simplejson module.  The `dict` will be passed
        to the relevant constructor on read.

        Parameters
        ----------
        inMemoryDataset : `object`
            Object to serialize.

        Raises
        ------
        Exception
            The file could not be written.

        Notes
        -----
        The `~yaml.SafeDumper` is used when generating the YAML serialization.
        This will fail for data structures that have complex python classes
        without a registered YAML representer.
        """
        self.fileDescriptor.location.uri.write(self._toBytes(inMemoryDataset))

    def _toBytes(self, inMemoryDataset: Any) -> bytes:
        """Write the in memory dataset to a bytestring.

        Will look for `_asdict()` method to aid YAML serialization, following
        the approach of the simplejson module.  The `dict` will be passed
        to the relevant constructor on read.

        Parameters
        ----------
        inMemoryDataset : `object`
            Object to serialize

        Returns
        -------
        serializedDataset : `bytes`
            YAML string encoded to bytes.

        Raises
        ------
        Exception
            The object could not be serialized.

        Notes
        -----
        The `~yaml.SafeDumper` is used when generating the YAML serialization.
        This will fail for data structures that have complex python classes
        without a registered YAML representer.
        """
        converted = False
        if hasattr(inMemoryDataset, "model_dump") and hasattr(inMemoryDataset, "model_dump_json"):
            # Pydantic v2-like model if both model_dump() and model_json()
            # exist.
            with contextlib.suppress(Exception):
                inMemoryDataset = inMemoryDataset.model_dump()
                converted = True

        if not converted and hasattr(inMemoryDataset, "dict") and hasattr(inMemoryDataset, "json"):
            # Pydantic v1-like model if both dict() and json() exist.
            with contextlib.suppress(Exception):
                inMemoryDataset = inMemoryDataset.dict()
                converted = True

        if not converted:
            # mypy needs the 'not a type' check because "is_dataclass" works
            # for both types and instances.
            if dataclasses.is_dataclass(inMemoryDataset) and not isinstance(inMemoryDataset, type):
                inMemoryDataset = dataclasses.asdict(inMemoryDataset)  # type: ignore[unreachable]
            elif hasattr(inMemoryDataset, "_asdict"):
                inMemoryDataset = inMemoryDataset._asdict()

        unsafe_dump = self.writeParameters.get("unsafe_dump", False)
        if unsafe_dump:
            serialized = yaml.dump(inMemoryDataset, sort_keys=False)
        else:
            serialized = yaml.safe_dump(inMemoryDataset, sort_keys=False)
        return serialized.encode()
