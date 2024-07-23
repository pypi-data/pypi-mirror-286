from setuptools import setup, find_packages

setup(
    name='rabbitmq_auto_scaler',
    version='0.1.2',
    description='A library for auto-scaling RabbitMQ consumers',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Nishantth1/RabbitMQAutoScaler',
    author='Nishant Thakre',
    author_email='nishantthakre9@gmail.com',
    license='MIT',
    packages=find_packages(include=["rabbitmq_auto_scaler", "rabbitmq_auto_scaler.*"]),
    install_requires=[
        'aio_pika',
        'asyncio'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
