PY=python
PIP=pip install
SOURCES= ./src/admin.py ./src/lectures.py ./src/main.py ./src/mainpage.py ./src/register_panel.py ./src/registration.py ./src/sql_setup.py ./src/words.py
all: info

venv:
	${PY} -m venv kivy_venv
	kivy_venv\Scripts\activate & ${PY} -m ${PIP} "kivy[base]" kivy_examples
	utils\sane_cp.exe ${SOURCES} kivy_venv/

venv_run:
	kivy_venv\Scripts\activate & ${PY} kivy_venv\main.py

global:
	${PIP} "kivy[base]" kivy_examples

global_run:
	${PY} src\main.py


info:
	@echo "if you want to install 'kivy' in a venv enter `make venv` then  `make venv_run`"
	@echo "if you want to install 'kivy' global enter `make global` then  `make global_run`"

