#!/bin/bash

function install_packages {
    sudo apt install -y python3-virtualenv python3.10-venv python3-dev postgresql postgresql-client
    sed -n -e '/^Depends:/,/^Pre/ s/ python3-\(.*\),/python3-\1/p' debian/control | sudo xargs apt-get install -y
    python3 -m venv venv
    source venv/bin/activate
    pip3 install -r requirements.txt
    deactivate
}

function configure_psql {
    createuser -s shared
    createdb shared
    sudo cp pg_hba.conf /etc/postgresql/14/main/
    sudo cp postgresql.conf /etc/postgresql/14/main/postgresql.conf
    systemctl restart postgresql
}

function install_systemd_service {
    sudo cp project-odoo.service /etc/systemd/system/
    sudo systemctl enable project-odoo.service
}

function main {
    #install_packages
    configure_psql
    install_systemd_service
}

main
