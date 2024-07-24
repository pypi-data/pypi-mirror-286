# Copyright 2016 Akretion (http://www.akretion.com)
# Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Shopinvader price per quantity",
    "summary": "Shopinvader price per quantity",
    "version": "14.0.1.0.1",
    "category": "e-commerce",
    "website": "https://github.com/shopinvader/odoo-shopinvader",
    "author": "Akretion",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "auto_install": False,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        "shopinvader",
    ],
    "data": [],
    "demo": [
        "demo/pricelist_demo.xml",
    ],
    "qweb": [],
}
