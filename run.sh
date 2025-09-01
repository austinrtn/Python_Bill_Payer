venv_directory="./.venv"

if ! command -v python3 > /dev/null 2>&1; then
	echo "Python3 not installed... installing"
	sudo apt install python3 
fi

if ! command -v pip3 > /dev/null 2>&1; then
	echo "Pip3 not installed... installing"
	sudo apt install python3-pip3
fi

if [ ! -d "$venv_directory" ]; then
	echo "Initializing Python3 Virtual Enviornment..."
	python3 -m venv .venv

	echo "Installing dependencies..."
	source ./.venv/bin/activate
	pip3 install -r requirements.txt
fi

source ./.venv/bin/activate
python3 app.py

if [ $? -eq 0 ]; then
	deactivate
fi
