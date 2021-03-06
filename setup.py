from setuptools import setup

setup(
    name='Workon',
    version='0.8.2',
    description='Switch between projects quickly from command line',
    long_description='...',
    keywords='terminal side projects manager work cli',
    url='https://github.com/henocdz/workon',
    download_url = 'https://github.com/henocdz/workon/tarball/0.8.2',
    author='henocdz',
    author_email='self@henocdz.com',
    license='MIT',
    packages=['workon'],
    scripts=['scripts/workon.sh'],
    install_requires=['peewee==2.8.8', 'fire==0.1.2', 'six'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
    ]
)
