from distutils.core import setup

setup(
    name='Asa_Lib',
    version='1.0.0',
    packages=['asa_tests', 'asa_modules', 'asa_modules.users', 'asa_modules.users.tests', 'asa_modules.routing',
              'asa_modules.routing.tests', 'asa_modules.access_lists', 'asa_modules.access_lists.tests'],
    url='https://github.com/Flexin1981/AsaLib',
    license='MIT',
    install_requires=[
          'paramiko==1.16.1', 'netaddr==0.7.18'
      ],
    author='John Dowling',
    author_email='johndowling01@live.co.uk',
    description='Asa ssh module'
)
