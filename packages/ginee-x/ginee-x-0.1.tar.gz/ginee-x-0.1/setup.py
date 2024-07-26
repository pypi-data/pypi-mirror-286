# coding:utf-8
from setuptools import setup
setup(
        name='ginee-x',
        version='0.1',
        description='This is a Python SDK for Ginee X, which provides a Python interface to interact with Ginee X\'s OpenAPI.',
        author='yi.xu',
        author_email='widebluesky@qq.com',
        url='https://www.ginee-x.com',
        packages=[
                'ginee_x.chat',
                'ginee_x.knowledge',
                'ginee_x.agent'
        ]
)