ZShiny - Unofficial zalando API CLI 
=====================================

Warning - IN DEVELOPMENT. Holiday project :)

Supported functionality
----------------------------

- Exposed functionality in CLI:

 - catalog:
  
   .. code:: bash

     zshiny catalog-list
     zshiny catalog-find --find-by-name shoe
     zshiny catalog-get <CATALOG_ID>
     zshiny catalog-get <CATALOG_ID> --machine-readable
     # show json schema of catalog:
     zshiny catalog-show-schema 

- article:
  
   .. code:: bash

      zshiny article-list
      # simple single values supported now
      zshiny article-find-by-filter --filter-value color:red
      zshiny article-get IQ142B008-G11
      zshiny article-get IQ142B008-G11  --machine-readable
      # show json schema:
      zshiny article-show-schema

- filters (article-filters)

   .. code:: bash

      zshiny filter-list
      zshiny filter-get activationDate
      zshiny filter-show-schema --machine-readable


- brand
  
  IN PROGRESS



Use case
-----------

A hacker would like to find a nice clothing for his girlfriend/boyfriend. His/her partner likes color red, 
in most cases goes for unisex. The hacker knows the size and... he would like to do a good deal.

She/he can not live without showing off his bash/(any other tool) skills :D. Therefore, the zshiny *MUST* 
supports *--machine-readable*, so the output of CLI may be feed to any tool of her/his choice. Because, the gift-finding is an  iterative process, the CLI *MUST* be responsive and --- if necessary pre-fetch data.


.. code:: bash

	# show me all brands (example with the only polish brand I know ;) )
	zshiny brand-list | grep evaminge 

	zshiny brand-get <BRAND_ID>

	# we could use here brand-find as well
	export MY_BRAND_ID=$(zshiny brand-list --machine-readable | grep evaminge)

	# the type will be transform in the search full-text query
	# next we check whether name contains it, 
	# e.g.,
	#    "name" : "NEW B-MUSSILA - Summer jacket - black",

	zshiny article-list --type=shoes --brand-id=${MY_BRAND_ID} --sale=True | ... 

	# get fields with supported full-text queries
	zshiny article-filter-list

Development 
------------

The project entry point is *Makefile*:

  - setting up virtualenv
  - running tests
  - (more to come)

Status
------------

- version 0.1 (IN PROGRESS):

  - parallel calling API [COMPLETED]
  - support for all Zalando Resources in CLI:

    - catalog [COMPLETED]
    - article and article-filters [IN PROGRESS]
    - brand 
    - domains

    - command options:

      - fields [PARTIALLY]
      - pretty-print & machine-readable [PARTIALLY]

- version 0.2: caching for <tab> auto-completion
- version 0.3: port to python 2.6
- version 0.4: caching
- version x: 

    - we could support finding combinations of clothes.

Limitations 
-----------------

- only python3

