#! /bin/bash
echo "If you've got pytest installed globally, it seems to cause problems... Run via pythonenv/bin/pytest instead."
echo "Setting up development environment..."

rm -r pythonenv
pip3 install virtualenv
python3 -m venv pythonenv
source pythonenv/bin/activate
pythonenv/bin/pip3 install -r requirements.txt
cp -n communicator/config.json.example communicator/config.json

echo ""
echo "Done - Ready for development. Upgrade terminal with:"
echo "source pythonenv/bin/activate"
echo ""
