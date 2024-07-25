from setuptools import setup, find_packages

setup(
    name="spider-cli",
    version="0.2.2",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'requests',
        'jmespath',
        'art',
        'halo',
        'python-dotenv',
        'urllib3>=1.25.8,<2.0',  # Add compatible urllib3 version
        'chardet>=3.0.2,<4.0',  # Add compatible chardet version
        'pkginfo<1.11'  # Ensure this is compatible with twine

    ],
    entry_points={
        'console_scripts': [
            'spider=usl.cli:cli',
        ],
    },
    author='Andrew Polykandriotis',
    author_email='support@minakilabs.com',
    description='SPIDER: Secure Proxy Infrastructure for Data Extraction and Retrieval',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/minakilabs-official/spider-cli',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
