""" Zinc Library: An advanced visualisation library for FE models

The Zinc library is an advanced visualisation library for FE models.  The
Zinc library understands a representation of mathematical fields, including
finite element, image-based and CAD.  It also understands fields derived by
mathematical operators.
"""

classifiers = """\
Development Status :: 5 - Production/Stable
Intended Audience :: Developers
Intended Audience :: Education
Intended Audience :: Science/Research
License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)
Programming Language :: Python
Operating System :: Microsoft :: Windows
Operating System :: Unix
Operating System :: MacOS :: MacOS X
Topic :: Scientific/Engineering :: Medical Science Apps.
Topic :: Scientific/Engineering :: Visualization
Topic :: Software Development :: Libraries :: Python Modules
"""

from setuptools import setup
from setuptools.dist import Distribution

doclines = __doc__.split("\n")


class BinaryDistribution(Distribution):
    def is_pure(self):
        return False

    def has_ext_modules(self):
        return True


setup(
    name='cmlibs.zinc',
    version='4.1.2',
    author='Zinc developers',
    author_email='h.sorby@auckland.ac.nz',
    packages=['cmlibs', 'cmlibs.zinc'],
    package_data={'cmlibs.zinc': ['libzinc.so.4.1.2','libzinc.so.4','_context.so','_differentialoperator.so','_element.so','_field.so','_fieldmodule.so','_fieldcache.so','_fieldassignment.so','_fieldparameters.so','_fieldrange.so','_fieldsmoothing.so','_font.so','_glyph.so','_graphics.so','_light.so','_logger.so','_material.so','_optimisation.so','_node.so','_scene.so','_scenecoordinatesystem.so','_scenefilter.so','_scenepicker.so','_sceneviewer.so','_sceneviewerinput.so','_selection.so','_shader.so','_spectrum.so','_region.so','_result.so','_status.so','_stream.so','_streamimage.so','_streamregion.so','_streamscene.so','_tessellation.so','_timekeeper.so','_timenotifier.so','_timesequence.so']},
    url='https://cmlibs.org',
    license='Mozilla Public License 2.0 (MPL 2.0)',
    description=doclines[0],
    classifiers=[cl for cl in classifiers.split('\n') if cl],
    long_description=open('README.rst').read(),
    long_description_content_type='text/x-rst',
    distclass=BinaryDistribution,
    include_package_data=True,
    zip_safe=False,
)
