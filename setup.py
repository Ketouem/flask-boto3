from pip.req import parse_requirements
from setuptools import setup

# Requirements
install_reqs = parse_requirements('requirements.txt', session='dummy')
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='Flask-Boto3',
    version='0.2.1',
    url='https://github.com/Ketouem/flask-boto3',
    license='MIT',
    author='Cyril "Ketouem" Thomas',
    author_email='ketouem@gmail.com',
    description='Flask extension that ties boto3 to the application',
    py_modules=['flask_boto3'],
    zip_safe=False,
    include_package_data=True,
    install_requires=reqs,
    platforms='any',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
