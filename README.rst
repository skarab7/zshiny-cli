ZShiny - Unofficial Zalando Shop API CLI 
============================================

Supported functionality
----------------------------

Exposed functionality in CLI (see `Official Zalando Shop API <https://github.com/zalando/shop-api-documentation/wiki/Api-introduction>`_):

- catalog:
  
  .. code:: bash

    zshiny catalog-list
    zshiny catalog-find --find-by-name shoe
    zshiny catalog-get <CATALOG_KEY>
    zshiny catalog-get <CATALOG_KEY> --machine-readable
    # show json schema of catalog:
    zshiny catalog-show-schema 
    # get size of the resource:
    zshiny catalog-stats

- article:
  
  .. code:: bash

    zshiny article-list
    zshiny article-list --fields name season modelId
    # support for sorting
    zshiny article-list --sort-by-popularity
    # full-text search
    zshiny article-search shoe --machine-readable
    # use filters
    zshiny article-find-by-filter --filter-value color:red
    # use multi-value filters
    zshiny article-find-by-filter --filter-value color:red color:white --machine-readable
    zshiny article-get <ARTICLE_ID>
    zshiny article-get <ARTICLE_ID>  --machine-readable
    # show json schema:
    zshiny article-show-schema
    # get size of the resource:
    zshiny article-stats

- filters (article-filters)

  .. code:: bash

    zshiny filter-list
    zshiny filter-get <FILTER_NAME>
    zshiny filter-show-schema --machine-readable


- brand:

  .. code:: bash

    zshiny brand-get <BRAND_KEY> 
    zshiny brand-show-schema 
    zshiny brand-stats        # stats of brand resource
    zshiny brand-list         # list all brands

How to install
--------------------

On Your machine
~~~~~~~~~~~~~~~~~~~

.. code:: bash
 
  git clone https://github.com/skarab7/zshiny-cli.git
  cd zshiny-cli
  python setup.py install 

  zshiny -h
  # uninstall with: pip3 uninstall zshiny_client

Docker
~~~~~~~~~~~~~

.. code:: bash

  git clone https://github.com/skarab7/zshiny-cli.git
  cd zshiny-cli
  
  make docker_build
  # print the help
  docker run -it --rm zshiny_cli_box -h

  # get a list of brands
  docker run -it --rm zshiny_cli_box brand-list


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

