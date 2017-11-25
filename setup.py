from setuptools import setup

setup(name='wreader',
      version='0.01',
      description='Wunderground weather API reader for hourly data',
      long_description=readme(),
      classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
      ],
      keywords='wreader wunderground weather wunderground-api',
      url='https://github.com/marcus-luck/wreader',
      author='Marcus Luck',
      author_email='marcus.luck@outlook.com',
      license='MIT',
      packages=['wreader'],
      zip_safe=False,
      install_requires=[
          'requests>=2.12.4',
          'pandas>=0.19.2',
          ],
      test_suite='nose.collector',
      tests_require=['nose', 'nose-cover3'],
      include_package_data=True
      )
