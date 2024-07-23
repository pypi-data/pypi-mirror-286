import setuptools
with open("README.md", "r") as fh:
	long_description = fh.read()
setuptools.setup(
	name="Agent99",
	version="0.0.1",
	author="Braden James Lang",
	author_email="braden.lang77@gmail.com",
	description="Chat and Agent Project",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/GaryOcean428/Agent99",
	packages=setuptools.find_packages(),
	classifiers=[
	"Programming Language :: Python :: 3.10",
	"License :: OSI Approved :: MIT License",
	"Operating System :: OS Independent",
	],
)