from setuptools import setup, find_packages

setup(
    name='dlib_validation_dest',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'dlib',
        'opencv-python',   # The `cv2` module is included in `opencv-python`
        'numpy',
        'scikit-image',
        'joblib',
        'dateutil',
    ],
    author='Jack Ma',
    author_email='ma.jack@email.com',
    description='library for trainning model ai',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    # url='https://github.com/jackma/my_library',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)