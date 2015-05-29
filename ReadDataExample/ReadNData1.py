import json
import numpy
import zipfile

# conditional imports
import sys
if sys.version < '3':
    import cStringIO as io
else:
    import io

def read_ndata1(path):
    """
        Read an ndata1 format file from path.

        Returns metadata, data.
    """
    zip_file = zipfile.ZipFile(path, 'r')
    namelist = zip_file.namelist()
    if "metadata.json" in namelist and "data.npy" in namelist:
        with zip_file.open("metadata.json") as fp:
            metadata = json.load(fp)
        with zip_file.open("data.npy") as fp:
            data_buffer = io.StringIO(fp.read())
            data = numpy.load(data_buffer)
    if data is not None:
        return metadata, data
    return None, None
