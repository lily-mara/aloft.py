from setuptools import setup

with open('requirements.txt') as f:
	required = f.read().splitlines()

setup(
	name="aloft.py",
	version="0.0.3",
	author="Nate Mara",
	author_email="natemara@gmail.com",
	description="A simple API for getting winds aloft data from NOAA",
	license="MIT",
	test_suite="tests",
	keywords="aviation weather winds aloft",
	url="https://github.com/natemara/aloft.py",
	packages=['aloft'],
	classifiers=[
		"Development Status :: 3 - Alpha",
		"Topic :: Utilities",
		"License :: OSI Approved :: MIT License",
	],
	install_requires=required,
)
