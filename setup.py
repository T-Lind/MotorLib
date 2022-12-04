from setuptools import setup, find_packages

setup(
    name='MotorLib',
    version='0.1',
    license='MIT',
    author="Tiernan Lindauer",
    author_email='tiernanxkl@gmail.com',
    packages=find_packages('MotorLib'),
    package_dir={'': 'MotorLib'},
    url='https://github.com/T-Lind/MotorLib',
    keywords='Robotics',
    install_requires=[
          'RPi.GPIO',
      ],

)