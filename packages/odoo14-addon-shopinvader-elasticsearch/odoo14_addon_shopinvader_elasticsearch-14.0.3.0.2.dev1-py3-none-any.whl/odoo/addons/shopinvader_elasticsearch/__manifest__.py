# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Shopinvader Elasticsearch",
    "summary": """
        Shopinvader Elasticsearch Connector""",
    "version": "14.0.3.0.1",
    "license": "AGPL-3",
    "author": "ACSONE SA/NV",
    "website": "https://github.com/shopinvader/odoo-shopinvader",
    "depends": [
        "base_sparse_field",
        "shopinvader_search_engine",
        "connector_elasticsearch",
    ],
    "data": ["data/ir_export_product.xml"],
    "demo": ["demo/index_config_demo.xml", "demo/backend_demo.xml"],
    "installable": True,
}
