from setuptools import setup

setup(
    name='my_node_selector',
    version='1.0.5',
    packages=['my_node_selector'],
    entry_points={
        'console_scripts': [
            'node-selector=my_node_selector.main:initialize_ui',
        ],
    },
    install_requires=[
        'Pillow',
    ],
    include_package_data=True,
    package_data={
        '': ['*.png'],
    },
    zip_safe=False,
)
