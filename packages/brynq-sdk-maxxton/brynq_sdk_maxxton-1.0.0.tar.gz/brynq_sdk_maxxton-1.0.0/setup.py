from setuptools import setup


setup(
    name='brynq_sdk_maxxton',
    version='1.0.0',
    description='Maxxton wrapper from BrynQ',
    long_description='Maxxton wrapper from BrynQ',
    author='BrynQ',
    author_email='support@brynq.com',
    packages=["brynq_sdk.maxxton"],
    package_data={'brynq_sdk.maxxton': ['templates/*']},
    license='BrynQ License',
    install_requires=[
        'brynq-sdk-brynq>=1',
    ],
    zip_safe=False,
)