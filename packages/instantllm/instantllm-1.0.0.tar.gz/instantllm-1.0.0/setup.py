from setuptools import setup, find_packages

with open('README.MD','r') as f:
    long_description = f.read()

setup(
    name='instantllm',
    version='1.0.0',  # Initial stable release
    description='Instantllm is the backend server for the Instant LLM app, enabling users to effortlessly connect and interact with any self-hosted large language model through our user-friendly mobile interface.',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='RubenRobadin',
    author_email='rubenjesusrobadin11@gmail.com',
    install_requires=[
        'asyncio',  # Required for asynchronous programming
        'websockets>=12.0',  # Required for WebSocket communication (version pin recommended)
        'typing>=3.7',  # Optional type hints support (version pin for older Python)
    ],
    python_requires='>=3.11',  # Require Python 3.11 or later
)
