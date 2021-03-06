# Copyright (c) 2014 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from setuptools import setup, find_packages
from setuptools.command.sdist import sdist
from release import release
import re
import os
import glob

VERSION_PATTERN = re.compile(r"(?m)^__version__\s*=\s*['\"](.+)['\"]$")


def get_version():
    """Return the current version as defined by u2fval/__init__.py."""

    with open('u2fval/__init__.py', 'r') as f:
        match = VERSION_PATTERN.search(f.read())
        return match.group(1)


class custom_sdist(sdist):
    def run(self):
        print "copying default settings..."
        source = os.path.abspath('u2fval/default_settings.py')
        target = os.path.abspath('conf/u2fval.conf')
        with open(target, 'w') as target_f:
            with open(source, 'r') as source_f:
                target_f.write(source_f.read())
        os.chmod(target, 0600)
        sdist.run(self)
        os.remove(target)


setup(
    name='u2fval',
    version=get_version(),
    author='Dain Nilsson',
    author_email='dain@yubico.com',
    maintainer='Yubico Open Source Maintainers',
    maintainer_email='ossmaint@yubico.com',
    url='https://github.com/Yubico/u2fval',
    license='BSD 2 clause',
    packages=find_packages(),
    scripts=['scripts/u2fval'],
    setup_requires=['nose>=1.0'],
    data_files=[
        ('/etc/yubico/u2fval', ['conf/u2fval.conf', 'conf/logging.conf']),
        ('/etc/yubico/u2fval/metadata', glob.glob('conf/metadata/*.json'))
    ],
    install_requires=['python-u2flib-server>=3.1', 'SQLAlchemy',
                      'python-memcached', 'WebOb', 'cachetools'],
    test_suite='nose.collector',
    tests_require=[''],
    cmdclass={'release': release, 'sdist': custom_sdist},
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: Internet',
        'Topic :: Security',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application'
    ]
)
