from setuptools import setup, find_packages
import bltrade.bltrade.BLTradeVersion as bv
from os import path
this_directory = path.abspath(path.dirname(__file__))
#long_description = "BLTrade"
long_description = f"bltrade version:{bv.GetVersion()}，是可以嵌入任何交易软件的Trade工具库。"
print(long_description)
#with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
#    long_description = f.read()
 
setup(name='BLTrade', # 包名称
        #packages=find_packages(include=['bltrade', 'bltrade.blback']),
        packages=find_packages().append(["test","datas","doc","config"]),
        #include_package_data=True, # 需要处理的包目录
        
        #version='0.26', # 版本
        version=bv.GetVersion(),
        classifiers=[
            'Development Status :: 3 - Alpha',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python', 'Intended Audience :: Developers',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.12',
        ],
        install_requires=['backtrader'],
        #entry_points={'console_scripts': ['pmm=pimm.pimm_module:main']},
        package_data={'': ['*.txt','*.csv','*.docx','*.ini']},
        author='Jiawenze', # 作者
        author_email='s.gua@163.com', # 作者邮箱
        description='BLTrade', # 介绍
        long_description=long_description, # 长介绍，在pypi项目页显示
        long_description_content_type='text/markdown', # 长介绍使用的类型，我使用的是md
        url='', # 包主页，一般是github项目主页
        license='MIT', # 协议
        keywords='BLTrade',
        #packages=["BLTrade","BLStrategy","test","BLBack","BLNetwork","datas"],
      ) # 关键字 搜索用