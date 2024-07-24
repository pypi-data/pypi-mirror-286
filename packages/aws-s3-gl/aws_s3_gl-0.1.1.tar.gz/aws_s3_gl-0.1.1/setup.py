from setuptools import setup, find_packages

setup(
    name='aws_s3_gl',  # Replace with your library name
    version='0.1.1',  # Replace with your library version
    packages=find_packages(),  # Automatically find packages in the directory
    install_requires=[
        'boto3',  # AWS SDK for Python
        'polars',  # DataFrame library for Python
    ],
    description='The `aws_s3` class provides a Python interface for interacting with AWS S3 storage. It allows for operations such as uploading and downloading files, managing parquet files, and handling data partitions. This class is designed to work with the AWS SDK for Python (`boto3`) and the Polars library for data manipulation.',  # Short description
    long_description=open('README.md').read(),  # Long description from README
    long_description_content_type='text/markdown',  # Type of long description
    author='Leonardo Daniel Gonzalo Laura',  # Replace with your name
    author_email='glleonardodaniel@gmail.com',  # Replace with your email
    url='https://github.com/yourusername/my_library',  # Replace with your project URL
    license='MIT',  # Replace with the license you choose
)
