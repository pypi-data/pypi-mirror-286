from setuptools import setup, find_packages
from setuptools import setup, find_packages

setup(
    name='skymavis_solver',
    version='1.1',
    packages=find_packages(),
    install_requires=[
        'numpy==2.0.1',
        'opencv_python==4.10.0.84',
        'opencv_python_headless==4.10.0.84',
        'Pillow==10.4.0',
        'setuptools==71.1.0',
    ],
    author='Phuc Vo',
    author_email='phuc.vo@skymavis.com',
    description='Module Bypass Sky Mavis Security Verification',
    long_description_content_type='text/markdown',
    long_description="""
**`skymavis_solver`** is a Python package designed to bypass CAPTCHA security verification used by Sky Mavis. This tool processes CAPTCHA images to determine if the challenge has been successfully bypassed.

### Features:

- **Specific to Sky Mavis CAPTCHA**: Works exclusively with Sky Mavis security verifications.
- **Image Zooming Required**: Ensure CAPTCHA images are properly zoomed in before processing for best results.

### Usage:

```python
from skymavis_solver import bypass_captcha

# Provide a properly zoomed CAPTCHA image
image_path = 'path/to/captcha_image.png'

# Process the CAPTCHA
result = bypass_captcha(image_path)

# Check the result
if result:
    print("CAPTCHA bypassed successfully!")
else:
    print("CAPTCHA not bypassed.")
"""
)