# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from setuptools import setup
from io         import open

setup(
    # ? Genel Bilgiler
    name         = "Kekik_fastapi_cache",
    version      = "0.2.4",
    url          = "https://github.com/keyiflerolsun/Kekik_fastapi_cache",
    description  = "Kekik FastAPI Cache",
    keywords     = ["Kekik_fastapi_cache", "KekikAkademi", "keyiflerolsun"],

    author       = "keyiflerolsun",
    author_email = "keyiflerolsun@gmail.com",

    license      = "GPLv3+",
    classifiers  = [
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3"
    ],

    # ? Paket Bilgileri
    packages         = ["Kekik_fastapi_cache"],
    python_requires  = ">=3.10",
    install_requires = [
        "setuptools",
        "wheel",
        "fastapi",
        "aiomcache",
        "pendulum",
        "starlette"
    ],

    # ? PyPI Bilgileri
    long_description_content_type = "text/markdown",
    long_description              = "".join(open("README.md", encoding="utf-8").readlines()),
    include_package_data          = True
)