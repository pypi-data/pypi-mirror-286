from setuptools import setup

setup(
    name='checkingress',
    version='1.0.2',
    author='Xizhen Du',
    author_email='xizhendu@gmail.com',
    url='https://devnull.cn',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    description='Check ingress status of your instance',
    # packages=['thedns'],
    install_requires=[
        "requests",
        "theid"
    ]
)
