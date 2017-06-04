# cfbackup

Cloudflare DNS backup tool

Based on official [cloudflare](https://github.com/cloudflare/python-cloudflare) library.

## Installation instructions

with pip (automatically):

    pip install git+https://github.com/nordicdyno/cfbackup@master
    cfbackup -h

without pip (manually, installation dependencies is up to you):

    git clone https://github.com/nordicdyno/cfbackup
    cd cfbackup
    python -c "from cfbackup.__main__ import main; main()" -h

## How to use

### Set environment variables

```bash
 export CF_API_EMAIL=<your@ema.il>
 export CF_API_KEY=<YOURAPIKEY>
```

* [Where do I find my Cloudflare API key?](https://support.cloudflare.com/hc/en-us/articles/200167836-Where-do-I-find-my-Cloudflare-API-key-)

### Run commands

Show zones:

    cfbackup show zones --pretty

Show all DNS records with stats:

    cfbackup show dns -z <zone-name> --pretty

Dump DNS records data as JSON array in file:

    cfbackup show dns -z <zone-name> > backup_<zone-name>.json

## TODO

* `restore` command
* man page
* PyPI publication
* git tags for releases

### MAYBE

* add BIND output format
