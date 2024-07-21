from setuptools import setup, find_packages

setup(
    name="pipilong-notify",
    version="0.2.0",
    author="PiPiLONG256",
    author_email="66461682@qq.com",
    description="一个钉钉webhook包",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'certifi==2024.7.4',
        'charset-normalizer==3.3.2',
        'idna==3.7',
        'load-dotenv==0.1.0',
        'markdown-it-py==3.0.0',
        'mdurl==0.1.2',
        'Pygments==2.18.0',
       ' python-dotenv==1.0.1',
       ' requests==2.32.3',
       ' rich==13.7.1',
        'urllib3==2.2.2',
    ]

)