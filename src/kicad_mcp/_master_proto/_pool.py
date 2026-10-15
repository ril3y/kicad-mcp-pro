"""Isolated descriptor pool for master KiCad protos.

kipy 0.7.1 registers its proto descriptors in the global default pool
via ``_descriptor_pool.Default()``. Our master-aligned regenerated stubs
use the same protobuf package names (``kiapi.common.*`` etc.) and would
collide on symbols like ``kiapi.common.ApiStatusCode``. We give them a
separate :class:`DescriptorPool` so both can co-exist in the same
process.

Every generated ``*_pb2.py`` file in this tree is post-processed to use
``shared_pool`` from this module instead of the default pool.

Well-known protos (``google.protobuf.field_mask``, ``any``, ``empty``,
etc.) are referenced by master's descriptors but normally live only in
the global default pool. We seed our pool with their FileDescriptor
protos so cross-references resolve at AddSerializedFile time.
"""

from __future__ import annotations

from google.protobuf import any_pb2  # noqa: F401
from google.protobuf import descriptor_pb2
from google.protobuf import descriptor_pool
from google.protobuf import empty_pb2  # noqa: F401
from google.protobuf import field_mask_pb2  # noqa: F401

shared_pool: descriptor_pool.DescriptorPool = descriptor_pool.DescriptorPool()


def _seed_well_known(module) -> None:
    """Copy a well-known proto's FileDescriptor into shared_pool."""
    file_desc = module.DESCRIPTOR
    proto = descriptor_pb2.FileDescriptorProto()
    file_desc.CopyToProto(proto)
    shared_pool.Add(proto)


for _mod in (field_mask_pb2, any_pb2, empty_pb2):
    try:
        _seed_well_known(_mod)
    except TypeError:
        # Already added (e.g. on module reimport) or pool already has
        # a compatible descriptor (well-known protos can be looked up
        # via descriptor_pool.Default() fallback in some protobuf
        # builds).
        pass


# When our schematic_pb2 generated stubs reference Any/Empty fields,
# protobuf needs to resolve the python class. For Any specifically we
# want callers to be able to pass standard ``google.protobuf.Any``
# objects — keeping their type identity matching what kipy / the rest
# of the application uses. Cross-pool messages of the same fully-
# qualified name are protocol-compatible at the wire level even if
# Python's isinstance() disagrees.
