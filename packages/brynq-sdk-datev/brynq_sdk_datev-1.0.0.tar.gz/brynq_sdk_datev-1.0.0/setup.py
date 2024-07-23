from setuptools import setup


setup(
    name='brynq_sdk_datev',
    version='1.0.0',
    description='Datev wrapper from Salure',
    long_description='Datev wrapper from Salure',
    author='D&A Salure',
    author_email='support@salureconnnect.com',
    packages=["brynq_sdk.datev"],
    license='BrynQ License',
    install_requires=[
        'brynq-sdk-brynq>=1',
        'brynq-sdk-functions>=1',
        'pandas>=1,<=3'
    ],
    zip_safe=False,
)