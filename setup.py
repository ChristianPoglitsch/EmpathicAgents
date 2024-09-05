# pip install --editable .
# source : https://stackoverflow.com/questions/49039436/how-to-import-a-module-from-a-different-folder


from setuptools import setup, find_packages

setup(
    name='llm_character',
    version='0.1',
    packages=find_packages(include=['LLM_Character', 'LLM_Character.*']),
    install_requires=[
        # todo: 
    ],
    python_requires='>=3.6',
)