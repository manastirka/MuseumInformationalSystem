#!/usr/bin/env python3
"""
Crystal Structure Database Access
Wrapper module that provides access to multiple crystallographic databases.

This module is maintained for backwards compatibility.
The actual implementation is in crystal_structure_databases.py
"""

# Import the multi-database implementation
from crystal_structure_databases import (
    CrystalStructureSearch,
    get_crystal_structure_database,
    get_cod_database
)

# Re-export for backwards compatibility
CODDatabase = CrystalStructureSearch

__all__ = [
    'CODDatabase',
    'CrystalStructureSearch',
    'get_cod_database',
    'get_crystal_structure_database'
]
