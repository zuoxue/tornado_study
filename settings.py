#coding=utf-8

import os

PORT = 8000

SITE_ROOT = os.path.dirname(__file__)

settings = {
    'template_path':os.path.join(os.path.dirname(__file__),'templates'),
    'static_path':os.path.join(os.path.dirname(__file__),'static'),
    'debug':True,
    'cookie_secret': "2hcicVu+TqShDpfsjMWQLZ0Mkq5NPEWSk9fi0zsSt3A="
}