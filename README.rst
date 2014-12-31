ZShiny - Unofficial zalando API CLI 
=====================================

Warning - IN DEVELOPMENT. Holiday project :)

Supported functionality
----------------------------

- Exposed functionality in CLI:

 - list categories for all the articles:
  
 ::

   zshiny catalog-list


Use case
-----------

A hacker would like to find a nice clothing for his girlfriend/boyfriend. His/her partner likes color red, 
in most cases goes for unisex. The hacker knows the size and... he would like to do a good deal.

She/he can not live without showing off his bash/(any other tool) skills :D. Therefore, the zshiny *MUST* 
supports *--machine-readable*, so the output of CLI may be feed to any tool of her/his choice. Because, the gift-finding is an  iterative process, the CLI *MUST* be responsive and --- if necessary pre-fetch data.


:: 

	# show me all brands (example with the only polish brand I know ;) )
	zshiny brand-list | grep evaminge 

	zshiny brand-get --id=ev2
	zshiny brand-get --name=evaminge

	# we could use here brand-find as well
	export MY_BRAND_ID=$(zshiny brand-list --machine-readable | grep evaminge)

	# the type will be transform in the search full-text query
	# next we check whether name contains it, 
	# e.g.,
	#    "name" : "NEW B-MUSSILA - Summer jacket - black",

	zshiny article-list --type=shoes --brand-id=${MY_BRAND_ID} --sale=True | ... 

	# get fields with supported full-text queries
	zshiny article-filter-list

Roadmap
------------

- version 0.1 (IN PROGRESS):
	
	- support for all Zalando Resources

- version 0.2: parallel calling API, not (slow) sequential calling API    
- version 0.3: caching for <tab> auto-completion
- version 0.4: python2 
- version 0.5: caching
- version x: 

    - we could support finding combinations of clothes.

Limitations 
-----------------

- only python3

