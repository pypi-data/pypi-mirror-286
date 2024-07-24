from setuptools import setup


name_library = 'SchoolManager'
version_library = '1.0.0'
description_long = ''
description_short = 'this library can use for all user and this is a school manager'
with open('README.md', 'r', encoding = 'utf-8') as file:
    description_long = file.read()
    
    
setup(
      name=name_library,
      version=version_library,
      author="Parsa Dehghani",
      author_email="<lspd099@gmail.com>",
      description=description_short,
      long_description=description_long,
      long_description_content_type="text/markdown",
      classifiers=[
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.11",
          "License :: OSI Approved :: MIT License",
          "Operating System :: Microsoft :: Windows :: Windows 10",
          "Operating System :: Microsoft :: Windows :: Windows 11",
          "Framework :: Django",
          "Development Status :: 5 - Production/Stable",
          "Intended Audience :: Customer Service",
          "Intended Audience :: Developers",
          
          ],
      python_requires =">=3.6",
      keywords = ["School","Manager","Python","Student","Teacher","Class"]
      
      
      
      
      )