from setuptools import setup, find_packages

setup(
    name='mantlebio',
    version='1.0.6',
    author='MantleBio',
    description='MantleBio Python SDK',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'requests>=2.26.0',
        'boto3>=1.21.42',
        'python-dotenv>0.19.2',
        'protobuf>=5.00.0',
        'google-auth>=2.6.6',
        'python-dotenv',
        'pandas>=2.0.3',
        'numpy<1.29.0,>=1.22.4'
    ],
    package_data={
        'proto': ['*.py', '*.pyi'],
        'mantlebio': ['*.py'],
    }
)
