# Constraint Condenser

This script takes a Vivado constraints file on standard input, and condenses all `set_property` constraints on the same `[get_ports ...]` into a single `set_property -dict` statement before returning the adjusted file on stdout.

The new `set_property -dict` statements will be emitted at the location of the first matching `set_property`.  The tool can understand existing `set_property -dict` statements.
