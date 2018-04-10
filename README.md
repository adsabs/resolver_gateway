[![Build Status](https://travis-ci.org/adsabs/resolver_gateway.svg)](https://travis-ci.org/adsabs/resolver_gateway)
[![Coverage Status](https://coveralls.io/repos/adsabs/resolver_gateway/badge.svg)](https://coveralls.io/r/adsabs/resolver_gateway)


# ADS Resolver Gateway

## Short Summary

This microservice captures and logs information such as search, abstract view etc.



## Setup (recommended)

    $ virtualenv python
    $ source python/bin/activate
    $ pip install -r requirements.txt
    $ pip install -r dev-requirements.txt
    $ vim local_config.py # edit, edit
    $ docker run --name some-redis -d -p 6379:6379 redis

    
    
## Testing

On your desktop run:

    $ py.test
    
    
    
## API

#### Make a GET request with a bibcode to return all links associated with that bibcode:

    curl -X GET https://ui.adsabs.harvard.edu/resolver/<bibcode>

For example to return *all* links associated with 2017arXiv170909566R, you would do   

    curl -X GET https://ui.adsabs.harvard.edu/resolver/2017arXiv170909566R


#### Make a GET request with a bibcode and link type to return all links of the type specified associated for that bibcode:

    curl -X GET https://ui.adsabs.harvard.edu/resolver/<bibcode>/<link_type>

For example to return links for *all*  full text sources, you would do

    curl -X GET https://ui.adsabs.harvard.edu/resolver/2013MNRAS.435.1904M/esource

#### Available Link Types:

`<link_type>` is one of the following (case-insensitive):

* **abstract** *Abstract*
* **citations** *Citations to the Article*
* **references** *References in the Article*
* **coreads** *Also-Read Articles*
* **toc** *Table of Contents*
* **openurl**
* **metrics**
* **graphics**
* **esource** *Full text sources*
  * **pub_pdf** *Publisher PDF*
  * **eprint_pdf** *Arxiv eprint*
  * **author_pdf** *Link to PDF page provided by author*
  * **ads_pdf** *ADS PDF*
  * **pub_html** *Electronic on-line publisher article (HTML)*
  * **eprint_html** *Arxiv article*
  * **author_html** *Link to HTML page provided by author*
  * **ads_scan** *ADS scanned article*
  * **gif** *backward compatibility similar to /ads_scan*
  * **preprint** *backward compatibility similar to /eprint_html*
  * **ejournal** *backward compatibility similar to /pub_html*
* **data** *On-line data*
  * **aca** *Acta Astronomica Data Files*
  * **alma** *Atacama Large Millimeter/submillimeter Array*
  * **ari** *Astronomisches Rechen-Institut*
  * **astroverse** *CfA Dataverse*
  * **atnf** *Australia Telescope Online Archive*
  * **author** *Author Hosted Dataset*
  * **bicep2** *BICEP/Keck Data*
  * **cadc** *Canadian Astronomy Data Center*
  * **cds** *Strasbourg Astronomical Data Center*
  * **cxo** *Chandra X-Ray Observatory*
  * **esa** *ESAC Science Data Center*
  * **eso** *European Southern Observatory*
  * **gcpd** *The General Catalogue of Photometric Data*
  * **gtc** *Gran Telescopio CANARIAS Public Archive*
  * **heasarc** *NASA's High Energy Astrophysics Science Archive Research Center*
  * **herschel** *Herschel Science Center*
  * **ibvs** *Information Bulletin on Variable Stars*
  * **ines** *IUE Newly Extracted Spectra*
  * **iso** *Infrared Space Observatory*
  * **koa** *Keck Observatory Archive*
  * **mast** *Mikulski Archive for Space Telescopes*
  * **ned** *NASA/IPAC Extragalactic Database*
  * **nexsci** *NASA Exoplanet Archive*
  * **noao** *National Optical Astronomy Observatory*
  * **pasa** *Publication of the Astronomical Society of Australia Datasets*
  * **pdg** *Particle Data Group*
  * **pds** *The NASA Planetary Data System*
  * **simbad** *SIMBAD Database at the CDS*
  * **spitzer** *Spitzer Space Telescope*
  * **tns** *Transient Name Server*
  * **vizier** *VizieR Catalog Service*
  * **xmm** *XMM Newton Science Archive*
  * **zenodo** *Zenodo Archive*
* **inspire** *HEP/Spires Information*
* **librarycatalog**
* **presentation** *Multimedia Presentation*
* **associated** *Associated Articles*


## Maintainer(s)

Golnaz
