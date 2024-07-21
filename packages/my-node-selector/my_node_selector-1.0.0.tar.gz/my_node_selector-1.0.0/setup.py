from setuptools import setup, find_packages

setup(
    name="my_node_selector",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'my_node_selector': ['resources/*.png']
    },
    install_requires=[
        'tkinter',
        'Pillow',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'node-selector=my_node_selector.main:main',
        ],
    },
    author="karthick kumar",
    author_email="karthick.kumar@gdn-commerce.com",
    description="A node selector application",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
