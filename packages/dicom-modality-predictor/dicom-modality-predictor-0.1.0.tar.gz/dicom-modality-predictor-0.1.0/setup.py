from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dicom-modality-predictor",
    version="0.1.0",
    author="Nima Ch",
    author_email="nima.ch@gmail.com",
    description="A package to predict DICOM image modalities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NeuroGranberg/dicom-modality-predictor",
    packages=find_packages(),
    include_package_data=True,
    package_data={'dicom_modality_predictor': ['model/mlp_9998.pkl']},
    install_requires=[
        'numpy',
        'pydicom',
        'opencv-python',
        'scikit-learn',
        'joblib'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'dicom_modality_predictor=dicom_modality_predictor.cli:main',
        ],
    },
)