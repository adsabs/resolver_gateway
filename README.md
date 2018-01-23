[![Build Status](https://travis-ci.org/adsabs/resolver_gateway.svg?branch=master)](https://travis-ci.org/adsabs/resolver_gateway)
[![Coverage Status](https://coveralls.io/repos/adsabs/resolver_gateway/badge.svg?branch=master)](https://coveralls.io/r/adsabs/resolver_gateway?branch=master)


# ADS Resolver Gateway


#### Make a GET request with bibcode to return all links associated with that bibcode:

`curl http://localhost:5050/<bibcode>`


#### Make a GET request with bibcode and link type to return all links of the type specified associated for that bibcode:

`curl http://localhost:5050/<bibcode>/<link_type>`


##### where `<link_type>` is one of the following (case-insensitive):
* /abstract
* /citations
* /references
* /coreads
* /toc
* /openurl
* /esource
* /pub_pdf
* /eprint_pdf
* /author_pdf
* /ads_pdf
* /pub_html
* /eprint_html
* /author_html
* /ads_scan
* /gif
* /preprint
* /ejournal
* /data
* /ari
* /simbad
* /ned
* /cds
* /vizier
* /gcpd
* /author
* /pdg
* /mast
* /heasarc
* /ines
* /ibvs
* /astroverse
* /esa
* /nexsci
* /pds
* /aca
* /iso
* /eso
* /cxo
* /noao
* /xmm
* /spitzer
* /pasa
* /atnf
* /koa
* /herschel
* /gtc
* /bicep2
* /alma
* /cadc
* /zenodo
* /tns
* /inspire
* /librarycatalog
* /presentation
* /associated


##### For example:

`curl http://localhost:5050/2001ASPC..238..321D`

`curl http://localhost:5050/2012ASPC..461..763H/esource`

