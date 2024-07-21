from setuptools import setup, find_packages

setup(
    name='UKLawScraper',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # list your dependencies here
    ],
    entry_points={
        'console_scripts': [
            # if you have any scripts to run from the command line
        ],
    },
    author='Mohammadreza Joneidi Jafari',
    author_email='m.r.joneidi.02@gmail.com',
    description='A package to scrape case law informations.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/mrjoneidi/UKLawScraper',  # replace with your package's URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # replace with your license
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
