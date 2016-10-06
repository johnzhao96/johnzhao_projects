HOW TO USE (pptx_to_html)

INSTALLATION:
pptx_to_html requires the python-pptx library. To install, run the command:

$ pip install python-pptx

or go to https://python-pptx.readthedocs.org/en/latest/user/install.html for more options.

pptx_to_html also requires the html-1.16 library. To install, run the following command in the html-1.16/ directory:

$ python setup.py install


USAGE:
To translate a single pptx file, run the command:

$ ./pptx_to_html.py [--slideshow] <pres.pptx> <logdest>

where <pres.pptx> is the PowerPoint file to be translated and <logdest> is the path to the desired destination of the log. To translate the file in slideshow mode, use the --slideshow flag. In this case, use <logdest> to specify the directory in which to store the translated slides (one file will be created per slide in the pptx file).

To translate multiple pptx files, run the command:

$ ./run_translator.py <pptx_directory> <log_directory>

where <pptx_directory> is the desired directory of pptx files, <log_directory> is the desired destination of the resulting log files. run_translator finds all .pptx files in <pptx_directory> and runs pptx_to_html on each of the .pptx files it finds.

To empty the logs directory that is included in this directory, run the command:

$ ./clean_logs.sh