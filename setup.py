"""人文AI - Humanistic AI: 追求智慧的人文科学专家级AI系统"""

from setuptools import setup, find_packages

setup(
    name="humanistic-ai",
    version="3.2.0",
    author="灵台未央",
    author_email="10HQ@users.noreply.github.com",
    description="让AI具备深度人文素养 — 哲学思辨×CBT认知行为治疗×伦理检查×苏格拉底对话",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/10HQ/humanistic-ai",
    project_urls={
        "Bug Tracker": "https://github.com/10HQ/humanistic-ai/issues",
        "Documentation": "https://github.com/10HQ/humanistic-ai#readme",
        "Source": "https://github.com/10HQ/humanistic-ai",
    },
    packages=find_packages(exclude=["tests", "examples"]),
    py_modules=[
        "cognitive_distortion_detector",
        "concept_clarifier",
        "ethics_checker",
        "argument_analyzer",
        "socratic_engine",
        "semantic_analyzer",
        "humanistic_ai",
    ],
    python_requires=">=3.11",
    install_requires=[
        "requests>=2.28.0",
    ],
    extras_require={
        "semantic": ["requests>=2.28.0"],
        "web": ["gradio>=4.0.0"],
        "dev": ["pytest>=7.0.0"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Creative Commons",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Sociology",
    ],
    keywords="ai ethics philosophy psychology cbt socratic humanistic manifesto",
    license="CC-BY-SA-4.0",
)
