{
    "name": "Open Academy",
    "summary": """This is a summary of Open Academy Module.""",
    "description": """This is a description of Open Academy Module.""",
    "author": "Vauxoo",
    "website": "https://www.vauxoo.com",
    "category": "Uncategorized",
    "version": "15.0.1.0.0",
    "license": "LGPL-3",
    "depends": ["base"],
    "data": [
        "security/openacademy_security.xml",
        "security/ir.model.access.csv",
        "views/openacademy_menu.xml",
        "views/openacademy_course_views.xml",
        "views/openacademy_session_views.xml",
        "views/res_partner_views.xml",
        "reports/openacademy_session_report.xml",
        "wizards/openacademy_wizard_views.xml",
    ],
    "demo": [
        "demo/openacademy_course_demo.xml",
    ],
}
