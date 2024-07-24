# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Shopinvader Customer Validation",
    "summary": """Provide configuration and machinery to validate customers.""",
    "version": "14.0.1.4.0",
    "license": "AGPL-3",
    "author": "Camptocamp,Odoo Community Association (OCA)",
    "website": "https://github.com/shopinvader/odoo-shopinvader",
    "depends": ["shopinvader", "shopinvader_notification_default"],
    "demo": ["demo/email_demo.xml", "demo/notification_demo.xml"],
    "data": [
        "security/ir.model.access.csv",
        "views/partner_view.xml",
        "views/shopinvader_backend_view.xml",
        "views/shopinvader_partner_view.xml",
        "wizards/shopinvader_address_validate.xml",
        "wizards/shopinvader_partner_validate.xml",
        "templates/customer_address_email.xml",
        "templates/customer_profile_email.xml",
        "data/email_template.xml",
        "data/shopinvader_notification.xml",
    ],
    "installable": True,
    "pre_init_hook": "pre_init_hook",
}
