"""Provides a reusable module for creating generator main functionality
imports all pdks
provides a command line arg for choosing pdk: -p or --pdk
    current options include:
    gf180
    sky130

generator main function can import this module as follows:
from pdk.util.standard_main import pdk

the pdk is the pdk object which defaults to sky130 if none selected
"""

from argparse import ArgumentParser

parser = ArgumentParser(prog="pdk agnostic generator")
parser.add_argument("--pdk", "-p", choices=["sky130", "gf180"])
args = parser.parse_known_args()

pdk = None

# WARNING: DO NOT CHANGE standard behavoir (importing sky130 by default)

if args[0].pdk == "gf180":
    from glayout.pdk.gf180_mapped import gf180_mapped_pdk
    pdk = gf180_mapped_pdk
else: #default to sky130
    from glayout.pdk.sky130_mapped import sky130_mapped_pdk
    pdk = sky130_mapped_pdk

pdk.activate()


