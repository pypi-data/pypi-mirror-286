from setuptools import setup, find_packages

setup(
    name="text_alchemy",
    version="0.4",
    packages=find_packages(),
    install_requires=[
        'openai',
        'google-cloud-vision',
        'python-dotenv',
        'google-generativeai',
        'python-magic',
        'pandas',
        'requests',
        'pdf2image',
        'Pillow',
        'pymupdf',
    ],
    author="Tanmay Deep Sharma",
    author_email="tanmaydeepsharma21@gmail.com",
    description="A package to extract text and structured information using OpenAI and Google Vision APIs",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/tds-1/text_extractor",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)