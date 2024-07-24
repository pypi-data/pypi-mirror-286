from setuptools import setup,find_packages

with open('readme.md') as file:
	descripiton = file.read()

setup(
	name='subtranslator',
	version='0.0.2',
	packages=find_packages(),
	install_requires = [
	'pysrt','translate'],
	long_description=descripiton,
	long_description_content_type="text/markdown"
	)