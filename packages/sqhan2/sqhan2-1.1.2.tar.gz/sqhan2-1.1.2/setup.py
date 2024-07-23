from setuptools import setup, find_packages

setup(
    name='sqhan2',
    version='1.1.2',
    packages=find_packages(),
    author='Han Shaoqing',
    author_email='sqhan1@whu.edu.cn',
    description='A brief description of the package',
    long_description=open('README.md').read(),
#    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/mypackage',
    install_requires=[
        # 依赖包列表
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

