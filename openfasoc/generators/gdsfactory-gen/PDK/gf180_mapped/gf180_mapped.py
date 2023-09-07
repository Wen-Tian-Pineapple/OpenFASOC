# TODO: add all the cells from gf180 and a rule deck
# TODO: note that gf180 pip is not up to date with github repo (no layer views)
"""
usage: from gf180_mapped import gf180_mapped_pdk
"""

from gf180.layers import LAYER  # , LAYER_VIEWS

# import mappedpdk from the main pdk dir (parent of this dir)
import sys
from pathlib import Path

sys.path.append(Path(__file__).resolve().parent.parent)
from mappedpdk import MappedPDK


gf180_glayer_mapping = {
    "met4": "metal4",
    "via3": "via3",
    "met3": "metal3",
    "via2": "via2",
    "met2": "metal2",
    "via1": "via1",
    "met1": "metal1",
    "mcon": "contact",
    "poly": "poly2",
    "active": "comp",
    "n+s/d": "nplus",
    "p+s/d": "pplus",
    "nwell": "nwell",
    "pwell": "lvpwell",
    "dnwell": "dnwell",
}


gf180_mapped_pdk = MappedPDK(
    name="gf180",
    glayers=gf180_glayer_mapping,
    layers=LAYER.dict()
)
