# setup.py
from setuptools import setup, find_packages

setup(
    name='llm_package',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'kfp',
        'google-cloud-storage',
        'pandas',
    ],
    include_package_data=True,
    description='A package containing Kubeflow Pipelines components',
    url='https://github.com/githubuserrohith/llm_package',
    author='Rohith',
    author_email='your.email@example.com',
    license='MIT',
)
