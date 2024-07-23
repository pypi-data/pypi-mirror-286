from setuptools import setup, find_packages

setup(
    name="gen-talking-head",  # 项目的名称
    version="0.1.0",  # 项目的版本s
    author="Chen Yu, Cheng ZhiZhao",  # 项目作者的名称
    author_email="chengyu2024@unipus.cn",  # 项目作者的邮箱
    description="Self-developed TalkingHead video synthesis algorithm",  # 简短描述
    long_description="The algorithm consists of two parts: video synthesis and fine-tuning training.",  # 项目的详细描述
    long_description_content_type="text/markdown",  # 描述内容的类型，通常是Markdown
    url="https://github.com/unipus-wuhan/Algo_GenTalkingHead_Inference.git",  # 项目的网址或源码地址
    packages=find_packages(),  # 自动查找包含在你的项目中的包
    classifiers=[  # 项目的分类标签
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # 对Python的最低版本要求
    install_requires=[  # 依赖列表
        "numpy",
        "torch",
        "tqdm",
        "Pillow",
        # 在这里添加其他依赖
    ],
    include_package_data=True,  # 是否包含数据文件
    entry_points={
        'console_scripts': [
            'yourscript=yourpackage.module:function',  # 用于生成命令行工具
        ],
    },
)
