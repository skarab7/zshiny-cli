_VIRT_ENV_NAME=z_cli
_PYTHON_PATH=/usr/local/Cellar/python3/3.4.2_1/bin/python3
_PIP_EXEC=pip3

DOCKER_BOX_NAME="zshiny_cli_box"

_virtualenv_create:
	. $$(which virtualenvwrapper.sh) ; \
	mkvirtualenv --python=$(_PYTHON_PATH) $(_VIRT_ENV_NAME)

_virtualenv_install_packages:
	. $$(which virtualenvwrapper.sh) ; \
	workon $(_VIRT_ENV_NAME) ; \
	$(_PIP_EXEC) install -U -r requirements.txt ; \
	echo "Use workon: $(_VIRT_ENV_NAME)" ; 

test:
	python setup.py test

nosetest_nc_all:
	nosetests --nocapture ;

docker_build:
	docker build -t $(DOCKER_BOX_NAME) .

docker_cli_print_help:
	docker run -it --rm $(DOCKER_BOX_NAME) -h	
