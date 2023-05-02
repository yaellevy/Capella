============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

Development
===========

To set up `capella` for local development:

https://github.com/AlexSpradling/Capella
git clone https://github.com/AlexSpradling/Capella.git
cd capella
docker run -it --name capella-dev -w /opt -v %cd%:/opt python:3.11 bash
pip install Capella
cd capella
run main.py
