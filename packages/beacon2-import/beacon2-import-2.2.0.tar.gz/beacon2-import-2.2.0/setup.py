from setuptools import setup, find_packages

setup(
    name='beacon2-import',
    version='2.2.0',
    author='Khaled Jumah',
    author_email='khalled.jooma@yahoo.com',
    description='Seamlessly import and query all of the beacon protocol collections',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license = 'CC-BY-NC-4.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'beacon2-import = beacon2_import.beacon2_import:beacon2_import',
            'beacon2-search = beacon2_search.beacon2_search:beacon_query'
        ]
    },
    install_requires=[
       'jsonschema',
       'dataclasses',
       'bioblend',
       'cyvcf2',
       'pymongo',
    ],
    dependency_links=[
        'git+https://github.com/CSCfi/beacon-python#egg=beacon-python',
    ],
    py_modules=['utils'],  # Add utils.py here
)
