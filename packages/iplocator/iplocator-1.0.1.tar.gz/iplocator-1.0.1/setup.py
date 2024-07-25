from setuptools import setup, find_packages

setup(
    name='iplocator',
    version='1.0.1',
    author='Sayan Biswas',
    author_email='anonys0101@duck.com',
    description='The ultimate tool for IP location within the CLI, especially made for Hackers',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/sayanbiswas9/iplocate',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=2.0',
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'iplocate=iplocate.iplocate:main',
        ],
    },
)