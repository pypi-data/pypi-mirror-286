from setuptools import setup, find_packages

setup(
    name='dollarwave',
    version="2.0.2",  
    author='Cedric Moore Jr.',
    author_email='cedricmoorejunior5@gmail.com',
    description='A Python library for inflation adjustment calculations using Consumer Price Index (CPI) data.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/cedricmoorejr/dollarwave/tree/v2.0.2',
    project_urls={
        'Source Code': 'https://github.com/cedricmoorejr/dollarwave/releases/tag/v2.0.2',
    },
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.6',
    install_requires=[
        'pandas',
        'requests',
        'matplotlib',
        'pillow',
    ],
    license='MIT',
)
