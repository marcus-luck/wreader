from setuptools import setup

setup(name='wreader',
      version='0.01',
      description='Wunderground weather API reader for hourly data',
      url='https://github.com/marcus-luck/wreader',
      author='Marcus Luck'
      author_email='marcus.luck@outlook.com',
      license='MIT',
      packages=['wreader'],
      zip_safe=False,
      install_requires=['requests>=2.12.4','pandas>=0.19.2'])
