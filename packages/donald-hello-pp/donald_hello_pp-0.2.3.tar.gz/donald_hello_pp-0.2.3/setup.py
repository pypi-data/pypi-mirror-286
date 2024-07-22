from setuptools import setup, find_packages

setup(
    name='donald_hello_pp',  # Replace with your own username
    version='0.2.3',
    packages=find_packages(),
    install_requires=[
        'pandas>=1.0'
    ],
    author='AchillesReaper',
    author_email='dh3coding@gmail.com',
    description='A package for processing data with pandas',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/my_package',  # Replace with your repository URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)