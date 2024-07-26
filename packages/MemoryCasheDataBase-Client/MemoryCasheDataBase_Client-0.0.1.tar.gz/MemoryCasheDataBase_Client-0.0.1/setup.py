import setuptools; 

LongDescription : str = ""; 
with open("README.md", "r") as FileRead: 
    LongDescription = FileRead.read(); 

setuptools.setup( 
    name = "MemoryCasheDataBase_Client", version = "0.0.1", 

    author = "Никита Макаров, Мария Кутыркина", author_email = "ma-kar-ov@yandex.ru, mariahkutyrkina@yandex.ru", 

    description = "Python client for MemoryCasheDataBase_Server database and key-value store", long_description = LongDescription, 

    long_description_content_type = "text/markdown", 

    url = "https://github.com/ma-karov/MemoryCasheDataBase_Client/", download_url = "https://github.com/ma-karov/MemoryCasheDataBase_Client/archive/refs/tags/0.0.1.zip", 

    license = "Apache License, Version 2.0, see LICENSE file", 

    packages = [ "MemoryCasheDataBase_Client" ], 

    classifiers = ( 
        "Programming Language :: Python", 
        "Programming Language :: Python :: 3", 
        "Programming Language :: Python :: 3.0", 
        "Programming Language :: Python :: 3.1", 
        "Programming Language :: Python :: 3.2", 
        "Programming Language :: Python :: 3.3", 
        "Programming Language :: Python :: 3.4", 
        "Programming Language :: Python :: 3.5", 
        "Programming Language :: Python :: 3.6", 
        "Programming Language :: Python :: 3.7", 
        "Programming Language :: Python :: 3.8", 
        "Programming Language :: Python :: 3.9", 
        "Programming Language :: Python :: 3.10", 
        "Programming Language :: Python :: 3.11", 
        "Programming Language :: Python :: 3.12", 
        "Programming Language :: Python :: 3.13", 
        "Programming Language :: Python :: 3.14", 
        "Programming Language :: Python :: Implementation :: CPython", 
        "Programming Language :: Python :: Implementation :: PyPy" 
    ) 
); 
