

Use case
-----------

A hacker would like to find a nice cloth for his girlfriend/boyfriend. His/Her partner likes colour red, 
in most cases goes for unisex. THe hacker knows the size and... he would like to do a good deal :D


:: 


	# show me all brands (example with the only PL mark I know ;) )
	z-shiny --list-brands | grep evaminge 

	z-shiny --get-brand --brand-id=ev2
	z-shiny --get-brand --brand-name=evaminge

	export MY_BRAND_ID=$(z-shiny --list-brands | grep evaminge)

	# the type will be transform in the search fulltextquery
	# next we check whether name contains it, 
	# e.g.,
	#    "name" : "NEW B-MUSSILA - Summer jacket - black",
	z-shiny --list-articles --type=shoes

	z-shiny --list-articles --brand-id=evaminge --sale=True


Limitations 
-----------------

TO BE DONE
