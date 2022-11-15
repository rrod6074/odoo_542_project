#!/bin/bash

function list_pip_packages {
    source venv/bin/activate
    pip3 list
}

function show_psql_db {
    
}

function get_odoo_version {
    python3 odoo-bin --version
}

function main {
    list_pip_packages
    show_psql_db
    get_odoo_version
}
