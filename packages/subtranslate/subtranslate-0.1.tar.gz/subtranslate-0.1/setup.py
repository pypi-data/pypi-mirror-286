from setuptools import setup,find_packages  
# import subtrans

setup(
	name='subtranslate',
	version='0.1',
	packages=find_packages(), 
	install_requires = [
	'pysrt',
	'translate'],
	author="kumaresankp"
	)