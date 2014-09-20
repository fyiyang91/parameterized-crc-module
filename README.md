parameterized-crc-module
========================

A parameterized Cyclic Redundancy Check verilog module generator in python, comes with automated testbench,
compatible with Python v2.5 and above.

The automated verilog testbench generates distinct random data input (200 test cases by default), including
2 fixed test case: all 0s and all 1s, and compares with the precalculated crc output result.
