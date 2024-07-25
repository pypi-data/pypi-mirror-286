from setuptools import setup, find_packages
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

with open("README.md", "r", encoding='utf-8') as fh:
    long_desc= fh.read()

setup(
    name='lbxtoolkit',
    version='2.0.5',
    packages=find_packages(),
    install_requires=[
        'psycopg2',
        'pandas',
        'numpy',
        'msal',
        'requests',
        'selenium',
        'webdriver-manager',
        'validators',
        'pygetwindow'
    ],
    license='MIT License',
    description='Biblioteca de ferramentas LBX S/A',
    long_description=long_desc,
    long_description_content_type="text/markdown",
    author='Cristiano P. Ferrari',
    author_email='boxferrari@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
