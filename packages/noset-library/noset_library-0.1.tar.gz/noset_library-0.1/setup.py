import setuptools

setuptools.setup(
name = 'noset-library',
packages = ['noset-library'],
version = '0.1',
description = 'Repositório com funções frequentemente usadas em scripts dados noset para reutilização de código',
author = 'hfgarcia',
author_email = 'henrique.garcia@nos.pt',
url = 'https://github.com/nosportugal/noset-library',
download_url = 'https://github.com/nosportugal/noset-library/archive/refs/tags/v_01.tar.gz',    # I explain this later on
keywords = ['DATABASES', 'SFTP', 'ETLs'],
install_requires=[            
        'pandas',
        'pandas-gbq',
        'sqlalchemy',
        'requests',
        'pymysql',
        'paramiko',
        #pyodbc may be necessary as a hidden dependency
    ],

classifiers=[
'Development Status :: 3 - Alpha',      

'Intended Audience :: Developers',      

'Programming Language :: Python :: 3.10',
'Programming Language :: Python :: 3.12',
],
)