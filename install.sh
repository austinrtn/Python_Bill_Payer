venv_directory="./.venv"

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
