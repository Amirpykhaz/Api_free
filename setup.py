from setuptools import setup, find_packages

setup(
    name="Api_free",
    version="0.1.0",
    description="ماژول Api_free پر از وب سرویس های کاربردی برای راحتی کاربران",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Amirabass Khazaei",
    author_email="amiradasskhazaei.000@gmail.com",
    url="None",
    packages=find_packages(),
    install_requires=["aiohttp","persiantools"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)