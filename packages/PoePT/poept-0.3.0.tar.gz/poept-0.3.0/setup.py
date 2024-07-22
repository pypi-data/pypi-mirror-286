from setuptools import setup

with open('readme.md', 'r') as f:
    readme = f.read()

setup(
    name='PoePT',
    version='0.3.0',
    description='A Simple Selenium Based Python Library For Quora`s Poe.com',
    author='Saikyo0',
    author_email='mamaexus@gmail.com',
    url='https://github.com/saikyo0/PoePT',
    download_url="https://github.com/Saikyo0/PoePT/archive/refs/tags/v0.3.0.tar.gz",
    keywords = ['POE', 'QUORA', 'PYTHON'],
    packages=['poept'],
    install_requires=[
        'pyaudio',
        'seleniumbase',
        'SpeechRecognition'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    long_description=readme,
    long_description_content_type='text/markdown'
)