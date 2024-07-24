from setuptools import setup, find_packages

setup(
    name='bash_class_example',
    version='0.1.3',
    author='Donatus Ajaezu',
    author_email='donatusajaezu@example.com',
    description='A test of Classes stored in Bash Class',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/stbbash/bash_class_example.git',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        # List your package dependencies here
    ],
)
