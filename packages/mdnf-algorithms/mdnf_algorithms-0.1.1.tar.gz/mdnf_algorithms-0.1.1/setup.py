from setuptools import setup, find_packages

setup(
    name='mdnf_algorithms',
    version='0.1.1',
    author='bcy',
    author_email='baochangyingi@gmail.com',
    description='A dnf algorithms of the module',
    packages=find_packages(),
    install_requires=[                  # 依赖包
        # 在这里列出你的依赖，例如：
        "matplotlib == 3.9.1",
        "numpy == 1.26.4",
        "opencv-contrib-python==4.10.0.82",
        "opencv_python == 4.10.0.84",
        "Pillow == 10.4.0",
        "setuptools == 69.5.1",
    ],
    classifiers=[                       # 分类信息
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
