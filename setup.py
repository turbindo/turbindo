import pathlib

from setuptools import setup, find_packages
import subprocess
skel = pathlib.Path("turbindo/templates/skel")
skel_parts = ["/".join(x.parts[1:]) for x in skel.iterdir() if '__pycache__' not in x.parts]
deps = [line.strip() for line in open("requirements.txt").readlines()]
try:
    git_commit = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').strip()
except:
    git_commit = '-'
setup(name='turbindo',
      version=f'1.0.0',
      description='AIO Python Framework',
      author='Grant Haywood',
      author_email='grant@iowntheinter.net',
      license='MIT',
      include_package_data=True,
      package_dir={'turbindo': 'turbindo/'},
      package_data={'turbindo': skel_parts + ['*.j2', 'templates/*', 'templates/data_accessors.py.j2']},
      packages=find_packages("./"),
      entry_points={
          'console_scripts': [
              'turbindocli = turbindo.main:main'
          ]
      },
      zip_safe=False,
      install_requires=deps,
      setup_requires=deps)
