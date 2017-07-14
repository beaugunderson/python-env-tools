from setuptools import setup

setup(
    name='env-tools',
    author='Beau Gunderson',
    author_email='beau@beaugunderson.com',

    url='https://github.com/beaugunderson/python-env-tools',

    description='Tools for using .env files in Python',
    long_description_markdown_filename='README.md',

    keywords='.env env heroku procfile foreman',

    version='2.1.0',

    license='MIT',

    py_modules=['env_tools'],

    install_requires=[
        'tini>=3.0.1',
    ],

    setup_requires=[
        'setuptools-markdown',
    ],

    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',

        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',

        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ])
