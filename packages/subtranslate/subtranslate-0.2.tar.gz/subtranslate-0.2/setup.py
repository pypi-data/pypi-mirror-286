from setuptools import setup,find_packages  

with open('readme.md','r') as f:
	description = f.read()

setup(
	name='subtranslate',
	version='0.2',
	packages=find_packages(), 
	install_requires = [
	'pysrt',
	'translate'],
	author="kumaresankp",
	long_description=description,
	long_description_content_type="text/markdown",
	)