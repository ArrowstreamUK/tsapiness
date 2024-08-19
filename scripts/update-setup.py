# Read dependencies from requirements.txt
with open('../requirements.txt', encoding='utf-8') as f:
    requirements = f.read().splitlines()

# Update setup.py
setup_code = """
from setuptools import setup, find_packages

setup(
    name='tsapiness',
    version='0.0.4',
    packages=find_packages(),
    install_requires={},
    author='Andrew Le Breuilly',
    author_email='andrew@arrowstream.co.uk',
    description='An open source python package to connect survey data to the survey definition defined by tsapi',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ArrowstreamUK/TSAPI-py',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
""".format(requirements)

# Write the updated setup.py
with open('../setup.py', 'w', encoding='utf-8-sig') as f:
    f.write(setup_code)
    