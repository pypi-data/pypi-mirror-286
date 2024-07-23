from setuptools import setup, find_packages

VERSION = '1.0.1'
DESCRIPTION = 'Extracting timetable from image and converting it to JSON format.'
LONG_DESCRIPTION = 'A package that allows to extract timetables from images and converting them to JSON format using Gemini MM-LLM.'

# Setting up
setup(
    name="Image-to-Table",
    version=VERSION,
    author="Adem Bouatay",
    author_email="<adem.bouatay@eniso.u-sousse.tn>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(include=['image_to_table', 'image_to_table.*']),
    install_requires=['llama-index', 'llama-index-multi-modal-llms-gemini', 'pillow', 'tabulate'],
    keywords=['python', 'image', 'json', 'MM LLM', 'AI'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
