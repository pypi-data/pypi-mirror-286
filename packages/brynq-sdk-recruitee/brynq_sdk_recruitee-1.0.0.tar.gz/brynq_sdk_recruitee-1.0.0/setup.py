from setuptools import setup


setup(
    name='brynq_sdk_recruitee',
    version='1.0.0',
    description='Recruitee wrapper from BrynQ',
    long_description='Recruitee wrapper from BrynQ',
    author='BrynQ',
    author_email='support@brynq.com',
    packages=["brynq_sdk.recruitee"],
    license='BrynQ License',
    install_requires=[
        'brynq-sdk-brynq>=1',
        'requests>=2,<=3',
        'pandas>=1,<3',
        'pyarrow>=10,<=10'
    ],
    zip_safe=False,
)