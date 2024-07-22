from setuptools import setup, find_packages
import os


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


extra_files = package_files('pkgsize/scripts')

setup(
    name='pkgsize',
    version='1.0.1',
    author='Navid M',
    author_email='navidnm_@outlook.com',
    description='CLI for finding size of Python libraries on PyPi, and comparing size with other libraries.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://gitlab.com/navid-m/pkgsize',
    packages=find_packages(),
    include_package_data=True,
    package_data={'': extra_files},
    entry_points={
        'console_scripts': [
            'pkgsize=pkgsize.pkgsize:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
    ],
    python_requires='>=3.6',
)
