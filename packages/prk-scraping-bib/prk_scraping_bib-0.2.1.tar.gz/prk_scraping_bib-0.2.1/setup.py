from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='prk_scraping_bib',
    version='0.2.1',
    author='latris',
    author_email='abde4872@gmail.com',
    description='Primark scraping',
    long_description=long_description,
    url='https://github.com/tbeninnovation/webScrapping',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'prk_scraping_bib': ['site_maps.txt'],
    },
    install_requires=[
        'curl_cffi',
        'beautifulsoup4',
        'pandas',
        'selenium',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'prk_scraping_bib=prk_scraping_bib:main',
        ],
    },
)
