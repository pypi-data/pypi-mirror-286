from setuptools import setup, find_packages

setup(
    name='prk_scraping_bib',
    version='0.1',
    packages=find_packages(),
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
