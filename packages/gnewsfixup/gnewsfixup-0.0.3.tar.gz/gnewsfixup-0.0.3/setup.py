from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='gnewsfixup',
    version='0.0.3',
    # setup_requires=['setuptools_scm'],
    # use_scm_version={
    #     "local_scheme": "no-local-version"
    # },

    author="Naassh",
    author_email="liuqingfeng00@gmail.com",
    description='Provide an API to search for articles on Google News and returns a usable JSON response.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=requirements,
    url='https://github.com/holygeek00/GNews/',
    project_urls={
        'Documentation': 'https://github.com/holygeek00/GNews/blob/master/README.md',
        'Source': 'https://github.com/holygeek00/GNews/',
        'Tracker': 'https://github.com/holygeek00/GNews/issues',
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
