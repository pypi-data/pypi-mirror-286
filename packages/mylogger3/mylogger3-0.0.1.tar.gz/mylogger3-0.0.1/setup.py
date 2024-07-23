from distutils.core import setup
# import setuptools

packages = ['mylogger3']
setup(name='mylogger3',
      version='0.0.1',
      author='xigua, ',
      long_description='''
      一个有趣的日志器。
      ''',
      packages=packages,
      package_dir={'requests': 'requests'}, )
