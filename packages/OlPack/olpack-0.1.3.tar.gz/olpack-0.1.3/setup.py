from setuptools import setup, find_packages

setup(
    name='OlPack',
    version='0.1.3',
    description='A collection of tools to simplify your Python experience!',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Ollie Quayle',
    author_email='Olliequayle08@icloud.com',
    url='https://github.com/Ollieq1977336/PyPack',
    packages=find_packages(),  # Automatically find packages in the directory
    install_requires=[],  # List your dependencies here
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    
    extras_require={
        "dev": ["twine>=4.0.2"],
    },
    python_requires='>=3.6',

)
