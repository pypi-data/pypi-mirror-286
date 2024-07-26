from setuptools import setup, find_packages
import setuptools_scm

setup(
    name='icloudservice',  # Replace with your library name
    use_scm_version=True,
    setup_requires=["setuptools>=42", "setuptools_scm"],
    packages=find_packages(include=['icloudservice', 'icloudservice.*']),
    include_package_data=True,
    install_requires=[
        'boto3',  # AWS SDK for Python
        'rich', # Progress bar library
    ],
    description='The `icloudservice` class provides a Python interface for interacting with',
    long_description=open('README.md').read(),  # Long description from README
    long_description_content_type='text/markdown',  # Type of long description
    author='Leonardo Daniel Gonzalo Laura',  # Replace with your name
    author_email='glleonardodaniel@gmail.com',  # Replace with your email
    url='https://github.com/leonardogonzalolaura/workspace_icloudservice',  # Replace with your project URL
    license='MIT',  # Replace with the license you choose
)

