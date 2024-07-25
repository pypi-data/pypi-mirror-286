from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='spider_cloud_cos',
    version='5.1.9.30',
    description='文件云存储连接',
    long_description=long_description,
    install_requires=[
        "certifi==2024.7.4",
        "charset-normalizer==3.3.2",
        "crcmod==1.7",
        "idna==3.7",
        "pycryptodome==3.20.0",
        "requests==2.31.0",
        "retrying==1.3.4",
        "six==1.16.0",
        "urllib3==2.0.7",
        "xmltodict==0.13.0",
    ],
    author='xfc',
    packages=find_packages(),
    url='https://gitlab.zhuanspirit.com/xiefengcheng/spider_cloud_cos',
    include_package_data=True,
    python_requires='>=3.7',
    # entry_points={
    #     'console_scripts': [
    #         'spider_cloud_cos=spider_cloud_cos.mian:main'
    #     ]
    # },
)
