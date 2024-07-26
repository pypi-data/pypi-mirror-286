from setuptools import setup, find_packages

setup(
    name='cryptionpy',
    version='1.0.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'cryptionpy = cryptionpy.cli:main',
        ],
    },
    author='MrFidal',
    author_email='mrfidal@proton.me',
    description='A package for encrypting and decrypting Python files using base64 or emoji obfuscation.',
    long_description=open('README.md').read(),
    url="https://github.com/ByteBreach/cryptionpy",
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
