from setuptools import setup, find_packages

setup(
    name="async_chat_engine",
    version="1.0.11",
    author="Oscar",
    author_email="om@holograph.digital",
    description="An asynchronous chat engine using vLLM with a async producer-consumer pattern.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.10',
    install_requires=[
        "vllm",
        "websockets",
        "PyJWT",
    ],
)