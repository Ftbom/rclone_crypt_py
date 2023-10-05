import setuptools

with open('README.md', 'r', encoding = 'utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name = 'rclone-crypt',
    version = '1.1.1',
    license = 'MIT',
    description = 'Python implementation of encryption/decryption for rclone (crypt storage)',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    author = 'ftbom',
    author_email = 'lz490070@gmail.com',
    url = 'https://github.com/Ftbom/rclone_crypt_py',
    project_urls = {
        'Bug Tracker': 'https://github.com/Ftbom/rclone_crypt_py/issues',
    },
    keywords = ['rclone', 'decrypt', 'encrypt'],
    install_requires=[
        'PyNaCl',
        'pycryptodome',
    ],
    python_requires = '>=3.8',
    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    packages = setuptools.find_packages(exclude = ['tests*'], where = 'src'),
    package_dir = {'': 'src'},
)
