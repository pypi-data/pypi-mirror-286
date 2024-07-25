from setuptools import setup, find_packages

setup(
    name='s3filetransfer',
    version='0.1.0',
    description='A package to transfer files between S3 buckets with a progress bar',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/s3filetransfer',  # Replace with your actual URL
    author='Your Name',
    author_email='your.email@example.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'boto3',
        'tqdm'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
