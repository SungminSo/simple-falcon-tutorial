VENV = venv
export VIRTUAL_ENV := $(abspath ${VENV})
export PATH := ${VIRTUAL_ENV}/bin:${PATH}

${VENV}:
	python3 -m venv

# TODO: activate 했을 때 터미너 유지할 수는 없나?
activate:
	source ${VENV}/bin/activate && exec bash
