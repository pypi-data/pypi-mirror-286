from setuptools import setup, find_packages

setup(
    name='solidity-python-sdk',
    version='0.1.8',
    description='SDK for interacting with Digital Product Passport smart contracts',
    author='Luthiano Trarbach',
    author_email='bhagah.trarbach@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'web3',
        'python-dotenv',
        'requests',
        'pinatapy-vourhey',
        'eth-tester'
    ],
    python_requires='>=3.6',
)
