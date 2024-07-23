from setuptools import setup, find_packages

setup(
    name='mujoco_ar',
    version='0.1.0',
    description='A Python support package for an iOS app to receive position and rotation data using MuJoCo.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Omar Rayyan',
    author_email='olr7742@nyu.edu',
    url='https://github.com/omarrayyann/mujocoar',  # Replace with your actual GitHub URL
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'asyncio',
        'websockets',
        'numpy',
        'psutil',
        'opencv-python',
        'mujoco',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
