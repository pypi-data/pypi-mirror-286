# setup.py
from setuptools import setup, find_packages

def read_readme():
    try:
        with open('README.md', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return ""

setup(
    name='flexiai',
    version='1.0.5',
    packages=find_packages(include=['flexiai', 'flexiai.*']),
    include_package_data=True,
    package_data={
        'flexiai': [
            'assistant/*.py',
            'config/*.py',
            'core/*.py',
            'core/flexi_managers/*.py',
            'core/utils/*.py',
            'credentials/*.py',
            'scripts/*.py',
            'tests/*.py'
        ],
    },
    install_requires=[
        'openai==1.35.0',
        'azure-common==1.1.28',
        'azure-core==1.30.2',
        'azure-identity==1.17.1',
        'azure-mgmt-core==1.4.0',
        'azure-mgmt-resource==23.1.1',
        'pydantic==2.7.4',
        'pydantic-settings==2.3.3',
        'pydantic-core==2.18.4',
        'platformdirs==3.7.0',
        'python-dotenv==1.0.1',
        'urllib3==2.2.2',
    ],
    entry_points={
        'console_scripts': [
            'setup-flexiai-rag=flexiai.scripts.flexiai_rag_extension:setup_project',
            'setup-flexiai-flask-app=flexiai.scripts.flexiai_basic_flask_app:setup_project',
        ],
    },
    author='Savin Ionut Razvan',
    author_email='razvan.i.savin@gmail.com',
    description="FlexiAI: A dynamic and modular AI framework leveraging Multi-Agent Systems and Retrieval Augmented Generation (RAG) for seamless integration with OpenAI and Azure OpenAI services.",
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/SavinRazvan/flexiai',
    classifiers=[
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
    ],
    python_requires='>=3.10.14',
    project_urls={
        'Bug Reports': 'https://github.com/SavinRazvan/flexiai/issues',
        'Source': 'https://github.com/SavinRazvan/flexiai',
    },
    license='MIT',
)
