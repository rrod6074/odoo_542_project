#!/bin/bash

cd /home/shared/odoo_542_project/
source venv/bin/activate
python3 odoo-bin --addons-path=addons -d shared -i base
