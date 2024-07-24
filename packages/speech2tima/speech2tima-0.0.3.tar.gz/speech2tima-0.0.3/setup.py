# setup.py

from setuptools import setup, find_packages

setup(
    name='speech2tima',
    version='0.0.3',
    packages=find_packages(),
    install_requires=[
        'SpeechRecognition',
        'pyaudio'
    ],
    entry_points={
        'console_scripts': [
            'speech2tima = speech2tima.recognizer:main',
        ],
    },
    author='Titas Majumder',
    author_email='titas20031996@gmail.com',
    description='A package for speech recognition using SpeechRecognition library. Main function is gettext',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/titas2003/speech2tima.git',
    license='MIT',
)
