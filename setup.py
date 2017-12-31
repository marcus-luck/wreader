from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='wreader',
      version='0.3',
      description='Wunderground weather API reader for hourly data',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
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
