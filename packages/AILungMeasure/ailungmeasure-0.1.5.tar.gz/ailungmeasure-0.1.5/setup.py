# setup.py
from setuptools import setup, find_packages

setup(
    name='AILungMeasure',
    version='0.1.5',  # Update this version number
    packages=find_packages(include=['AILungMeasure', 'AILungMeasure.*']),
    install_requires=[
        'torch',
        'Pillow',
        'torchvision',
        'matplotlib',
        'opencv-python',
        'numpy',
        'imutils',
        'gdown',
        'pydicom',
    ],
    author='Mostafa Ismail',
    author_email='mostafa.ismail.k@gmail.com',
    description='Automated lung size measurements using deep learning and computer vision on portable chest radiographs.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/AILungMeasure',  # Update with your project URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: Free for non-commercial use',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    include_package_data=True,
    license='Creative Commons ATTRIBUTION-NONCOMMERCIAL-SHAREALIKE 4.0 INTERNATIONAL',
)
