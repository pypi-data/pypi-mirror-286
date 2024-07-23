# Beacon2 Import Toolkit

## Overview

Beacon Import facilitates the seamless transfer of local genetic data to the Beacon database server, enhancing collaboration and knowledge sharing. 
Meanwhile, Beacon Query empowers users to efficiently explore the database for specific genetic information, including genes, sequences, variants, 
cnv, and genomic ranges. The search tools also search the phenopacket and other metadata b2ri collections (individuals, runs, datasets, biosamples, 
cohorts and analyses), catalyzing genomic research and clinical applications


## Requirements

* Python 3.6 or newer. ([download instructions](https://www.python.org/downloads/))

## Installation and update

### Using Pip3

1. Install beacon2-import using pip3.

    ```bash
    sudo pip3 install beacon2-import
    ```

1. Update beacon2-import, if needed, using pip3.

    ```bash
    pip3 install beacon2-import --upgrade
    ```

1. Test your pip3 installation by running beacon2-import or beacon2-search.

    ```bash
    beacon2-import --help
    beacon2-search --help
    ```

### Using conda (bioconda channel)

1. Install beacon2-import using conda.

    ```bash
    conda config --add channels bioconda
    conda config --add channels conda-forge
    conda install beacon2-import
    ```

1. Update beacon2-import, if needed, using conda.

    ```bash
    conda update beacon2-import
    ```

1. Test your conda installation by running beacon2-import or beacon2-search.

    ```bash
    beacon2-import --help
    beacon2-search --help
    ```


## Usage - beacon2-import

```bash
usage: beacon2_import.py [-h] [-H DATABASE_HOST] [-P DATABASE_PORT] [-a]
                         [-A DATABASE_AUTH_CONFIG] [-g] [-u GALAXY_URL]
                         [-k GALAXY_KEY] [-d DATABASE] [-c COLLECTION]
                         [-i INPUT_JSON_FILE] [-s] [-o] [-D] [-V] [-ca] [-cc]
                         [-r REMOVED_COLL_NAME]

Input arguments

optional arguments:
  -h, --help            show this help message and exit

Connection to MongoDB:
  -H DATABASE_HOST, --db-host DATABASE_HOST
                        Hostname/IP of the beacon database
  -P DATABASE_PORT, --db-port DATABASE_PORT
                        Port of the beacon database

Addvanced Connection to MongoDB:
  -a, --advance-connection
                        Connect to beacon database with authentication
  -A DATABASE_AUTH_CONFIG, --db-auth-config DATABASE_AUTH_CONFIG
                        JSON file containing credentials/config e.g.{'db_auth_
                        source':'admin','db_user':'root','db_password':'exampl
                        e'}

Connection to Galaxy:
  -g, --galaxy          Import data from Galaxy
  -u GALAXY_URL, --galaxy-url GALAXY_URL
                        Galaxy hostname or IP
  -k GALAXY_KEY, --galaxy-key GALAXY_KEY
                        API key of a galaxy user WITH ADMIN PRIVILEGES

Database Configuration:
  -d DATABASE, --database  DATABASE
                        The targeted beacon database
  -c COLLECTION, --collection COLLECTION
                        The targeted beacon collection from the desired
                        database

Import Json Arguments:
  -i INPUT_JSON_FILE, --input_json_file INPUT_JSON_FILE
                        Input the local path to the JSON file or it's name on
                        your Galaxy Hitory to import to beacon

store origin:
  -s, --store-origins   Make a local file containing variantIDs with the
                        dataset they stem from
  -o , --origins-file   Full file path of where variant origins should be
                        stored (if enabled)

control output:
  -D, --debug
  -V, --verbose         Be verbose

Clear beacon database:
  -ca, --clearAll       Delete all data before the new import
  -cc, --clearColl      Delete specific collection before the new import
  -r REMOVED_COLL_NAME, --removeCollection REMOVED_COLL_NAME
                        Define the collection name for deletion

```





## Usage - beacon2-search

```bash
usage: beacon2_search.py [-h]
                         {sequence,range,gene,bracket,analyses,biosamples,cohorts,datasets,individuals,runs,cnv}
                         ...

Query Beacon Database

positional arguments:
  {sequence,range,gene,bracket,analyses,biosamples,cohorts,datasets,individuals,runs,cnv}
    sequence            Connect to MongoDB and perform sequence-based querys
                        to the genomicVariations collection
    range               Connect to MongoDB and perform range-based querys to
                        the genomicVariations collection
    gene                Connect to MongoDB and perform geneID-based querys to
                        the genomicVariations collection
    bracket             Connect to MongoDB and perform bracket-based querys to
                        the genomicVariations collection
    analyses            Connect to MongoDB and query the analyses collection
    biosamples          Connect to MongoDB and query the biosample collection
    cohorts             Connect to MongoDB and query the cohorts collection
    datasets            Connect to MongoDB and query the datasets collection
    individuals         Connect to MongoDB and query the individuals
                        collection
    runs                Connect to MongoDB and query the runs collection
    cnv                 Connect to MongoDB and query the copy number variants
                        (cnv) collection

optional arguments:
  -h, --help            show this help message and exit

```