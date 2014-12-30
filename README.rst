

Use case
-----------

A hacker would like to find a nice cloth for his girlfriend/boyfriend. His/Her partner likes colour red, 
in most cases goes for unisex. THe hacker knows the size and... he would like to do a good deal :D


:: 


	# show me all brands (example with the only polish brand I know ;) )
	zshiny --list-brands | grep evaminge 

	zshiny --get-brand --brand-id=ev2
	zshiny --get-brand --brand-name=evaminge

	export MY_BRAND_ID=$(z-shiny --list-brands | grep evaminge)

	# the type will be transform in the search fulltextquery
	# next we check whether name contains it, 
	# e.g.,
	#    "name" : "NEW B-MUSSILA - Summer jacket - black",
	zshiny --list-articles --type=shoes

	zshiny --list-articles --brand-id=evaminge --sale=True


Limitations 
-----------------

- only python3

