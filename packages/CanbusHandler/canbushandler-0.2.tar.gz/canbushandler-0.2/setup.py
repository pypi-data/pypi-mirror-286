from setuptools import setup, find_packages

setup(
    name='CanbusHandler',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'python-can',
    ],
    author='Jaakko Talvitie',
    author_email='jaska.talvitie@gmail.com',
    description='With this canbus library, you can handle canbus data more easier',
    url='https://github.com/jaakka/PythonCanbusHandler',
)