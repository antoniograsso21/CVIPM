import os
import shutil
import random
import math
import xml.etree.ElementTree as Et
from source_finder import SourceFinder
# import gammalib
import ctools
# import cscripts

# test


def random_coords(ra, dec):
    module = random.uniform(0, 1)
    angle = random.uniform(0, 2 * math.pi)
    ra += math.cos(angle) * module
    dec += math.sin(angle) * module
    return ra, dec


def update_xml_file(file_name, flow, coords):
    # content = '<?xml version = "1.0" standalone = "no"?> <source_library title = "source library">' +\
    #     ' < source name = "Crab" type = "PointSource" > < spectrum type = "PowerLaw" >' +\
    #     ' < parameter name = "Prefactor" scale = "1e-17" value = "'
    # content += str(flow)
    # content += '" min="1e-07" max="1000.0" free="1"/> <parameter name="Index" scale="-1" value="2.48" min="0.0"' +\
    #     ' max="+5.0" free="1"/> <parameter name="PivotEnergy" scale="1e6" value="0.3" min="0.01" max="1000.0"' +\
    #     ' free="0"/> </spectrum> <spatialModel type="PointSource"> <parameter name="RA" scale="1.0" value="'
    # content += str(coords[0])
    # content += '" min="-360" max="360" free="0"/> < parameter name = "DEC" scale = "1.0" value = "'
    # content += str(coords[1])
    # content += '" min="-90"  max="90"  free="0"/> </spatialModel> </source> <source name="CTABackgroundModel" ' +\
    #     'type="CTAIrfBackground" instrument="CTA"> <spectrum type="PowerLaw"> <parameter name="Prefactor" ' +\
    #     'scale="1.0" value="1.0" min="1e-3" max="1e+3" free="1"/> <parameter name="Index" scale="1.0" value="0.0" ' +\
    #     'min="-5.0" max="+5.0"   free="1"/> <parameter name="PivotEnergy" scale="1e6"  value="1.0"  min="0.01" '+\
    #     'max="1000.0" free="0"/> </spectrum> </source> </source_library>'
    # with open(file_name, "w") as f:
    #     f.write(content)
    tree = Et.parse(file_name)
    root = tree.getroot()
    root[0][0][0].attrib['value'] = str(flow)
    root[0][1][0].attrib['value'] = str(coords[0])
    root[0][1][1].attrib['value'] = str(coords[1])
    tree.write(file_name)


def generate_events(i, coords):
    sim = ctools.ctobssim()
    sim['inmodel'] = 'Models/sigma4_'+str(i)+'.xml'
    sim['outevents'] = 'Events/'+str(i)+'.fits'
    sim['caldb'] = 'prod2'
    sim['irf'] = 'South_0.5h'
    sim['ra'] = coords[0]
    sim['dec'] = coords[1]
    sim['rad'] = 5.0
    sim['tmin'] = '2020-01-01T00:00:00'
    sim['tmax'] = '2020-01-01T00:15:00'
    sim['emin'] = 0.1
    sim['emax'] = 100.0
    sim.execute()


def generate_skymap(i):
    return


def source_finder_tests(flow=3, n=1):
    os.chdir("../../Tests")
    shutil.rmtree("Models")
    shutil.rmtree("Events")
    shutil.rmtree("Skymaps")
    os.mkdir("Models")
    os.mkdir("Events")
    os.mkdir("Skymaps")

    true_coords = []

    for i in range(0, n):
        coords = random_coords(221.0, 46.0)
        true_coords.append(coords)
        shutil.copy("default.xml", "Models/sigma4_"+str(i)+".xml")
        update_xml_file("Models/sigma4_"+str(i)+".xml", flow, coords)
        generate_events(i, coords)
        generate_skymap(i)

    sf = SourceFinder("../Src/conf.json")
    computed_coords = sf.compute_coords()

    print(true_coords)
    print(computed_coords)

    os.chdir("../Src/tests")


source_finder_tests()

