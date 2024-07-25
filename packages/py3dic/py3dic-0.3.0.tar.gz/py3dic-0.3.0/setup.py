# import os
import setuptools

def get_version():
    version_file = 'py3dic/__init__.py'
    with open(version_file, 'r') as file:
        for line in file:
            if line.startswith('__version__'):
                # Extract the version number
                version = line.split('=')[1].strip().strip('\'"')
                return version
    raise RuntimeError('Cannot find version information')

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

requirements = [
    #  "tkinter",
    'scipy',
    'numpy',
    'matplotlib',
    'seaborn',
    'pandas',
    'openpyxl',
    'ipykernel',
    'jupyter',
    'opencv-python'
 ]

test_requirements = [
    'pytest',
    # 'pytest-pep8',
    # 'pytest-cov',
]


setuptools.setup(
    name="py3dic",
    version=get_version(),
    author="N. Papadakis",# Replace with your own username
    author_email="npapnet@gmail.com",
    # NOTE whenever entry points changes then you need to run `pip install -e .` to update the scripts
    entry_points={
        'console_scripts': [
            # 'tk_dic_main=py3dic.guis.dic_main.tkapp_dic:tk_analysis_app_launcher',
            'tk_dic_analysis=py3dic.guis.tk_dic_analysis.tk_dic_analysis_launcher:tk_analysis_app_launcher',
            # 'tk_dic_merge=py3dic.guis.dic_main.tkapp_dic:tk_analysis_app_launcher',
            'tk_dic_viewer=py3dic.guis.viewer_app.viewer_launcher:tk_viewer_app_launcher',
        ],
    },
    description="A package Digital Image Correlation (DIC) analysis in Python 3.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
    tests_require=test_requirements,
    python_requires='>=3.10',
    project_urls={
        'Documentation': 'https://npapnet.github.io/py3dic/',
        'Source': 'https://github.com/npapnet/py3dic'
    },

)
