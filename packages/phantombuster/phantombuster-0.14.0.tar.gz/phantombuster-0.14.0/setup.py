# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['phantombuster', 'phantombuster.remoter']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'pandas>=2.0,<3.0',
 'polars>=0.19.12,<0.20.0',
 'pyarrow>=15,<16',
 'pysam>=0.22.0,<0.23.0',
 'regex>=2022.10.31,<2023.0.0',
 'scipy>=1.10.1,<2.0.0',
 'trio>=0.22.0,<0.23.0',
 'zmq>=0.0.0,<0.0.1']

entry_points = \
{'console_scripts': ['phantombuster = phantombuster.cli:phantombuster']}

setup_kwargs = {
    'name': 'phantombuster',
    'version': '0.14.0',
    'description': 'Bioinformatical tool to remove sequencing artifacts originating from single-nucleotide errors and index hopping from barcode-based experiments',
    'long_description': 'PhantomBuster is a bioinformatical tool that removes phantom barcode combinations that occur due to single-nucleotide sequencing errors and index hopping.\nIt is written for lineage-tracing experiments and CRISPR-screens, but can be used for any experimental setups in which only barcodes and no genetic DNA is measured.\n\n# Installation\n\nPhantomBuster is available via [pypi](https://pypi.org/project/phantombuster/) and can be installed with standard python tools like pip or pipx.\n\n    pipx install phantombuster\n\n# QuickStart\n\nPhantomBuster is a command line tool which can be run via the `phantombuster` command.\nIt consists of four main steps: (1) demultplexing, (2) error correction of random barcodes, (3) hopping removal and (4) thresholding.\nFor CRISPR-screens a separate script can calculate p-values for guides.\n\n## Demultiplexing\n\nPhantomBuster demultiplexes BAM or FASTQ files, extracts all specified barcodes while error correcting barcodes with known reference sequences.\nFor demultiplexing additional worker processes must be started.\n\n```\nphantombuster demultiplex [INPUTFILE] --outdir [DIR] --barcode-hierarchy-file [FILE] --regex-file [FILE] \nphantombuster worker --outdir [DIR]\n```\n\nINPUTFILE must be a csv file that lists all BAM and FASTQ files that are processed.\n\nExample `input_files.csv`:\n```\nfile\n101.bam\n```\n\nThe barcode hierarchy file is a csv file that lists all barcodes to be extracted.\nThe order of the barcodes creates a hierarchy, in which barcodes higher up the hierarchy are more general, while barcodes lower in the hierarchy are more specific.\nThe hierarchy is used in the second step error correction, in which two random barcode sequences are only compared, if all barcode sequences higher up the hierarchy are the same.\nExample `barcode_hierarchy.csv`\n\n```\nbarcode,type,referencefile,threshold,min_length,max_length\nsample,reference,sample_barcodes.csv,auto,-,-\nlib,reference,library_barcodes.csv,1,-,-\nlid,random,-,-,50,50\n```\n\nThe regex file is a csv file that specifies for each read region how to extract barcodes by a regular expression.\n\nExample `regexes.csv`:\n```\ntag,regex\nb2,"^[ACGTN]{3}(?P<sample>[ACGTN]{5})"\nquery,"(?P<lid>[ACGTN]{5,6}(?P<lib>ACGT|GTAC){s<=1}[ACGTN]+)"\n```\n\nThe outdir is a directory that contains all output and temporary files.\nThe same out directory must be passed to all stages of phantombuster.\n\n## Error Correction\n\nThe error correction step employs the UMI-tools error correction algorithm to error correct random barcode sequences.\nFor error correction additional worker processes must be started.\n\n```\nphantombuster error-correct --outdir [DIR] --barcode-hierarchy-file [FILE]\nphantombuster worker --outdir [DIR]\n```\n\nThe out dir and barcode hierarchy file must be the same as in the demultiplexing step.\n\n## Index Hopping Removal\n\nThe index hopping removal step removes barcode combinations that likely arised due to index hopping.\nFor index hopping removal no worker processes need to be started.\n\n```\nphantombuster hopping-removal --outdir [DIR] [HOPPING_BARCODES]\n```\n\nThe out dir must be the same as in the previous steps.\nThe barcodes to test must correspond to one or a combination of barcodes of the barcode hierarchy (`sample`).\nCombinations can be given seperated by commas (`sample,lid`).\nMultiple barcodes or combinations can be given and are then processed one after another (`sample,lid lib`)\nIt is recommended to test the combination of barcodes on the i5 index and then the combination of barcodes on the i7 index.\n\n## Thresholding\n\nThresholding removes all barcode combinations with a read count below a user defined threshold.\nSeperate Thresholds can be chosen for different values of barcodes, for example for each sample.\nFor tresholding no worker processes need to be started.\n\n```\nphantombuster threshold --outdir [DIR] --threshold-file [FILE]\n```\n\nExample `thresholds.csv`:\n```\nsample,threshold\nsample1,10\n```\n',
    'author': 'Simon Haendeler',
    'author_email': 'simon.emanuel.haendeler@univie.ac.at',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.13',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
