import gdsfactory as gf
import sys
import argparse

from gdsfactory.cell import Settings, cell
from gdsfactory.component import Component

from gdsfactory.generic_tech import get_generic_pdk

gf.config.rich_output()
PDK = get_generic_pdk()
PDK.activate()

# dim = 40        # dimension of floorplan
# spacing = 2.3     # spacing of wire
# width = 0.5     # width of wire
# res_sets = 8    # number of turns, must be even number
# wire_layer = 69

parser = argparse.ArgumentParser(description="Via-chain Generator")
parser.add_argument("--dimension", required=True, help="Dimension of Floorplan W & L")
parser.add_argument("--spacing", required=True, help="Spacing between horizontal wires")
parser.add_argument("--width", required=True, help="Wire width")
parser.add_argument(
    "--res_sets", required=True, help="Number of horizontal lines / 2 (EVEN)"
)
parser.add_argument(
    "--wire_layer", required=True, help="GDS layer number of upper metal (wire)"
)
parser.add_argument("--mode", default="0", help="Set to 1 for thick line generation")
parser.add_argument("--output_dir", default=".", help="GDS output directory")
args = parser.parse_args()

# process command line arguments
dim = float(args.dimension)
spacing = float(args.spacing)
width = float(args.width)
res_sets = int(args.res_sets)
wire_layer = int(args.wire_layer)
gen_mode = int(args.mode)
gds_outdir = str(args.output_dir)

# center wire width, also the distance between two sense connections
res_width = ((res_sets * 2) - 1) * spacing

# tail length on each end
res_tail = (dim - res_width) / 2

# WIRES
pt_x = 0
pt_y = 0

pt_list = []

for i in range(res_sets):
    # hor line in one direction
    pt_list.extend([(pt_x, pt_y), (pt_x + dim, pt_y)])
    # hor line in opposite direction
    pt_list.extend([(pt_x + dim, pt_y + spacing), (pt_x, pt_y + spacing)])

    # move the pts (really just pt_y) to next location
    pt_y += 2 * spacing

# create wire path from points
Pwire = gf.Path(pt_list)

# cross section of winded wires
Xwire = gf.CrossSection(width=width, offset=0, layer=(wire_layer, 20))

# create component for the winded wires
Cwire = gf.path.extrude(Pwire, Xwire)
translation = (dim / 2 - Cwire.center[0], dim / 2 - Cwire.center[1])


@cell
def create_Ctop() -> Component:
    # TOP
    # create top level component
    Ctop = gf.Component()

    # create a reference in top
    Rwire = Ctop << Cwire

    # move the wire component reference
    Rwire.move(translation)

    # create and reference tails
    Ctail1 = gf.path.extrude(gf.Path([(dim / 2, 0), (dim / 2, res_tail)]), Xwire)
    Ctail2 = gf.path.extrude(
        gf.Path([(dim / 2, dim), (dim / 2, dim - res_tail)]), Xwire
    )

    Ctop << Ctail1
    Ctop << Ctail2

    return Ctop


@cell
def create_Cstructure() -> Component:
    # STRUCTURE
    # create top gds with pads
    if gen_mode == 0:
        Cstructure = gf.Component()
    else:
        Cstructure = gf.Component()

    # import and place pads
    Cpad = gf.import_gds(gds_outdir + "/" + "pad_forty_met1_met5.GDS")
    for i in range(4):
        Rpad = Cstructure << Cpad
        Rpad.move([0, i * 60])

    Ctop = create_Ctop()
    # move top to a proper location
    Rtop = Cstructure << Ctop
    Rtop.move([50, 90])

    # connect current ports of top to pads
    if gen_mode == 0:
        Xwire_i = gf.CrossSection(width=3 * width, offset=0, layer=(wire_layer, 20))
    else:
        Xwire_i = gf.CrossSection(width=width, offset=0, layer=(wire_layer, 20))
    Ctail1 = gf.path.extrude(gf.Path([(70, 130), (70, 200), (40, 200)]), Xwire_i)
    Ctail2 = gf.path.extrude(gf.Path([(70, 90), (70, 20), (40, 20)]), Xwire_i)

    Cstructure << Ctail1
    Cstructure << Ctail2

    # connect voltage ports of top to pads
    v_pt_a_y = pt_list[0][1] + 90 + translation[1]
    v_pt_b_y = pt_list[-1][1] + 90 + translation[1]

    Ctail1 = gf.path.extrude(gf.Path([(40, v_pt_a_y), (50, v_pt_a_y)]), Xwire)
    Ctail2 = gf.path.extrude(gf.Path([(40, v_pt_b_y), (50, v_pt_b_y)]), Xwire)

    Cstructure << Ctail1
    Cstructure << Ctail2

    return Cstructure


# OUTPUT
if gen_mode == 0:
    Cstructure_name = str(wire_layer) + "_line_res.gds"
else:
    Cstructure_name = str(wire_layer) + "_thick_line_res.gds"

Cstructure = create_Cstructure()
Cstructure.write_gds(gds_outdir + "/" + Cstructure_name)
