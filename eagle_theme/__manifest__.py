# -*- coding: utf-8 -*-
# Part of EagleERP. See LICENSE file for full copyright and licensing details.

{
    'name': 'Theme Eagleshop',
    'summary': 'Advanced Responsive Theme with A Range of Custom Snippets',
    'description': '''Theme Eagleshop
Business theme
Hardware theme
Hardware and tools theme
Single Page theme
Digital security theme
Event theme
Medical equipments theme
multipurpose template for industry
multipurpose template for all industries
eagle custom theme
customizable eagle theme
multi industry eagle theme
multi purpose responsive eagle theme
multipurpose website template for eagle
eagle multipurpose theme for industry
multipurpose templates for eagle
eagle ecommerce templates
eagle ecommerce theme
eagle ecommerce themes
eagle responsive themes
eagle website themes
eagle ecommerce website theme
eagle theme for ecommerce store
eagle bootstrap themes
customize eagle theme
eagle ecommerce store theme for business
eagle theme for business
eagle responsive website theme
Eagleshop Theme
Eagle Eagleshop Theme
Eagleshop theme for Eagle
eagle 11 theme
multipurpose theme
eagle multipurpose theme
eagle responsive theme
responsive theme
eagle theme
eagle themes
ecommerce theme
eagle ecommerce themes
eagle website themes
eagle bootstrap themes
bootstrap themes
bootstrap theme
customize eagle theme
ecommerce store theme
theme for business
theme for ecommerce store
    ''',
    'category': 'Theme/Ecommerce',
    'version': '12.0.1.0.6',

    'author': 'Shaheen Hossain',
    'website': 'https://www.eagle-erp.com/',
    'depends': [
        'website_theme_install',
        'mass_mailing',
        'website_hr',
        'website_sale',
        'website_blog',
        'website_event_sale',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/website_data.xml',
        'views/assets.xml',
        'views/views.xml',
        'views/website_view.xml',
        'views/slider_views.xml',
        'views/snippets.xml',
        'views/theme_customize.xml',
        'views/theme.xml',
    ],
    'support': 'support@eagle-erp.com',
    'live_test_url': 'https://eagle-erp.com/',
    'images': [
        'static/description/splash-screen.png',
        'static/description/splash-screen_screenshot.png',
    ],
    'application': True,
    'installable': True,
}
