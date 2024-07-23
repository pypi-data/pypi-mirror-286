from setuptools import setup, find_packages

setup(
    name='OCR_Lib',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'torch',
        'torchvision==0.13',
        'opencv-python',
        'scikit-image',
        'scipy',
        'vietocr',
        'einops',
        'numpy==1.24.1',
    ],
    entry_points={
        'console_scripts': [
            'run_OCR =OCR_Lib.main:main',
        ],
    },
    package_data={
        # Bao gồm các file weights hoặc tài nguyên cần thiết
        'OCR.Craft_OCR': ['weights/*.pth'],
        'OCR.VietOCR': ['weights/*.pth'],
    },
    author='Theduyet1812',
    author_email='theduyet1812@gmail.com',
    description='OCR model for text extraction and recognition',
    # url='https://github.com/yourusername/my_ocr_model',
)
