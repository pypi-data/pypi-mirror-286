from setuptools import setup

setup(
	name='ipfs_model_manager',
	version='0.0.12',
	packages=[
		'ipfs_model_manager',
	],
	install_requires=[
        'ipfs_kit@git+https://github.com/endomorphosis/ipfs_kit.git',
        'orbitdb_kit@git+https://github.com/endomorphosis/orbitdb_kit.git',
		'datasets',
		'urllib3',
		'requests',
		'boto3',
        'toml',
	],
    package_data={
		'ipfs_model_manager': [
		's3_kit/s3_kit.py',
        'test/test_fio.py',
        'test/test_hf_ipfs.py',
        'config/config.py',
        'aria2/aria2.py',
        'aria2/aria2c',
        'config/config_template.toml',
        'config/config.toml',
        'config/__init__.py',
        'config/config.py',
		]
	},
	include_package_data=True,
)