from setuptools import setup, find_packages

setup(
    name='vital-model-chars2vec-onnx',
    version='0.1.0',
    author='Marc Hadfield',
    author_email='marc@vital.ai',
    description='Vital Onnx version of char2vec',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/vital-ai/vital-onnx-model-packages',
    packages=find_packages(exclude=[]),
    entry_points={
    },
    scripts=[],
    package_data={
        'vital_model_chars2vec_onnx': ['models/**']
    },
    license='Apache License 2.0',
    install_requires=[
        'numpy==1.26.4',
        'onnxruntime==1.18.0'
    ],
    extras_require={

    },
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
