"""
Steam UI Framework - Setup Configuration
=========================================

Makes the Steam UI Framework installable as a Python package.

Installation:
    pip install -e .

Or from repository:
    pip install git+https://github.com/vitorpixel-6436/music-stream-app.git#subdirectory=steam_ui
"""

from setuptools import setup, find_packages
import os

# Read README for long description
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

# Read version from __init__.py
version = {}
with open('steam_ui/__init__.py', 'r', encoding='utf-8') as f:
    for line in f:
        if line.startswith('__version__'):
            exec(line, version)
            break

setup(
    # Package info
    name='steam-ui-framework',
    version=version.get('__version__', '1.0.0'),
    author='vitorpixel-6436',
    author_email='vitorleitye6436@gmail.com',
    description='A modular UI component library inspired by Steam\'s design',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/vitorpixel-6436/music-stream-app',
    
    # Package discovery
    packages=find_packages(include=['steam_ui', 'steam_ui.*']),
    include_package_data=True,
    
    # Dependencies
    install_requires=[
        'Django>=4.0',
    ],
    
    # Optional dependencies
    extras_require={
        'dev': [
            'pytest>=7.0',
            'black>=22.0',
            'flake8>=4.0',
        ],
    },
    
    # Package data
    package_data={
        'steam_ui': [
            'templates/**/*.html',
            'static/**/*.css',
            'static/**/*.js',
            'static/**/*.svg',
        ],
    },
    
    # Classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Framework :: Django :: 4.0',
        'Framework :: Django :: 5.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    
    # Requirements
    python_requires='>=3.8',
    
    # Entry points (if needed)
    entry_points={
        'console_scripts': [
            # Add CLI tools here if needed
        ],
    },
    
    # Metadata
    keywords='django ui components steam glass-morphism',
    project_urls={
        'Bug Reports': 'https://github.com/vitorpixel-6436/music-stream-app/issues',
        'Source': 'https://github.com/vitorpixel-6436/music-stream-app',
    },
)
