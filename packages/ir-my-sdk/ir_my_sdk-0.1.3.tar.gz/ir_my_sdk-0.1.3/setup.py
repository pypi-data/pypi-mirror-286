from setuptools import setup, find_packages

setup(
    name='ir_my_sdk',
    version='0.1.3',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[],
    author='Irvan Ariyanto',
    author_email='irvan.ariyanto104@gmail.com',
    description='A simple SDK',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/irvanariyanto/ir_my_sdk',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    pythion_requires='>=3.6',
)