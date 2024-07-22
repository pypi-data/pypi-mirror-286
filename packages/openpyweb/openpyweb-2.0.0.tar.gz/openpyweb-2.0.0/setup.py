from setuptools import setup, find_namespace_packages

from openpyweb import Version

with open("README.md", "r", encoding="utf8") as fd:
    longdescription = fd.read()


setup(
    name='openpyweb',
    version=Version.VERSION_TEXT + Version.EDITION,
    description='openpyweb is a python framework built to enhance web development fast and easy, also help web developers to build more apps with less codes',
    url="https://github.com/emmanuelessiens/openpyweb",
    author='Emmanuel Essien',
    author_email='emmanuelessiens@outlook.com',
    maintainer='Emmanuel Essien',
    maintainer_email='emmanuelessiens@outlook.com',
    include_package_data=True,
    packages=find_namespace_packages(include=['*', '']),
    long_description=longdescription,
    long_description_content_type='text/markdown',
    license=Version.LICENSE,
    keywords=Version.KEYWORDS,
    entry_points={
        'console_scripts': ['openpyweb = openpyweb.cmd.help:main', 'openpyweb-install = openpyweb.cmd.install:main', 'openpyweb-start = openpyweb.cmd.start:main', 'openpyweb-docs = openpyweb.cmd.doc:main',  'openpyweb-server = openpyweb.cmd.server:main']
    },
    install_requires=['Pillow', 'colorama',
                      'mysql-connector-python', 'psycopg2-binary', 'cx-Oracle'],
    zip_safe=False,
    classifiers=[
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Topic :: Office/Business',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python'
    ],
    python_requires='>3, >=3.3',
)