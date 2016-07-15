from setuptools import setup

setup(
    name='savingzelda',
    description="Check if all your webpage's links are ok. Because you can't save the day with a dead Link.",
    long_description="Check if all your webpage's links are ok. Because you can't save the day with a dead Link.",
    author='Renata Carreira',
    author_email='contato@renatacarreira.com',
    url='https://github.com/recarreira/saving-zelda',
    version='0.4',
    zip_safe=False,
    include_package_data=True,
    entry_points={
        'console_scripts':
        ['savingzelda = savingzelda.cli:main'],
        },
    packages=[
        'savingzelda',
        ],
    install_requires=[
        'beautifulsoup4==4.3.2',
        'requests==2.2.1',
        ],
)