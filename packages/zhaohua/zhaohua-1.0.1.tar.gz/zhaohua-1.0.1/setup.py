from setuptools import setup, find_packages

setup(
    name='zhaohua',  # 库的名称
    version='1.0.1',  # 库的版本 发布时间：2024年07月22日
    packages=find_packages(),  # 自动查找并包含所有子包
    description='一个简单的，自用的Python库。',  # 库的简短描述
    author='Zhao Hua',  # 库的作者
    author_email='zhaohua@126.com',  # 作者的电子邮件地址
    url='https://github.com/yourusername/mylibrary',  # 项目的URL地址
    install_requires=[ # 需要的环境支持
        'openpyxl',
        'pandas',
        'numpy',
        'requests',
        'selenium',
        'websocket-client',
        'webdriver-manager',
        'pillow',
        'pytesseract',
        'pdf2image',
        'chardet',
        'baidu-aip'

    ],
)
