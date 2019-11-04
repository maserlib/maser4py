from maser.data.pds.cassini.const import PDS_OBJECT_CLASSES as PDS_OBJECT_CLASSES_CASSINI
from maser.data.pds.voyager.const import PDS_OBJECT_CLASSES as PDS_OBJECT_CLASSES_VOYAGER
from maser.data.psa.mex.const import PDS_OBJECT_CLASSES as PDS_OBJECT_CLASSES_MARS_EXPRESS
import astropy.units as u

__all__ = ['PDS_OBJECT_CLASSES', 'PDS_UNITS']

PDS_OBJECT_CLASSES = {}
PDS_OBJECT_CLASSES.update(PDS_OBJECT_CLASSES_CASSINI)
PDS_OBJECT_CLASSES.update(PDS_OBJECT_CLASSES_VOYAGER)
PDS_OBJECT_CLASSES.update(PDS_OBJECT_CLASSES_MARS_EXPRESS)

PDS_UNITS = {
    'HERTZ': u.Unit('Hz'),
    'HZ': u.Unit('Hz'),
    'KILOHERTZ': u.Unit('kHz'),
    'MILLIBELL': u.def_unit('milliBell', 0.01 * u.dB),
    'N/A': u.dimensionless_unscaled,
    'NANOTESLA**2/HZ': u.Unit('nT**2/Hz'),
    'SECOND': u.s,
    'VOLT**2/M**2/HZ': u.Unit('V**2/(m**2 Hz)'),
}