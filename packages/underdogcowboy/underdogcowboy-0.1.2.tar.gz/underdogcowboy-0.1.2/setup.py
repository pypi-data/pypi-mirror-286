from setuptools import setup, find_packages

setup(
    name="underdogcowboy",
    version="0.1.2",
    packages=find_packages(),

    entry_points={
        "console_scripts": [
            "timelineeditor=underdogcowboy.core.timeline_editor:main", 
        ],
    },

)

