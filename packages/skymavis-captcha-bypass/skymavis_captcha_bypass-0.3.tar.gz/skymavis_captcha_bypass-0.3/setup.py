from setuptools import setup, find_packages

setup(
    name='skymavis_captcha_bypass',
    version='0.3',
    packages=find_packages(),
    install_requires=[
        'numpy==2.0.1',
        'opencv_python==4.10.0.84',
        'opencv_python_headless==4.10.0.84',
        'Pillow==10.4.0',
        'selenium==4.23.0',
        'setuptools==71.1.0',
    ],
    author='Phuc Vo',
    author_email='phuc.vo@skymavis.com',
    description='Module Bypass Sky Mavis Security Verification',
    long_description_content_type='text/markdown',

)
