from setuptools import setup, find_packages

setup(
    name="FAIsdk",
    version="1.3.0",
    description="Python SDK combining FAImageGen and InstantLight",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Saliou Kane",
    author_email="saliou@fotographer.ai",
    url="https://github.com/FotographerAI/FAI_sdks/",
    packages=find_packages(),
    install_requires=[
        "requests",
        "Pillow"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
