from setuptools import setup
import setuptools
with open('README.md','r', encoding='utf-8') as readme_file:
    readme = readme_file.read()

install_requires = [
	'requests'
]

version = '0.0.1.7'

setup(
    author='evergaster',
    version=version,
    description='sara api public based akaneko',
    install_package_data=True,
    install_requires=install_requires,
    license='MIT license',
    long_description=readme,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='sara anime wallpaper hentai',
    name='saraApi',
    python_requires='>=3.0',
    url='https://github.com/EverGasterXd/sara_api',
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    	"Development Status :: 4 - Beta",
    	"Natural Language :: English",
    	"Operating System :: Microsoft :: Windows :: Windows 10",
    	"Programming Language :: Python :: 3",
    	"Programming Language :: Python :: 3.9",
    	"Topic :: Internet"
    ]
)