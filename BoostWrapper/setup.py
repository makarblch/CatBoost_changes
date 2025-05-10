from setuptools import setup, find_packages

setup(
    name="boost_wrapper",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "scikit-learn>=1.0",
        "catboost>=1.2",
        "xgboost>=2.0",
        "lightgbm>=4.0"
    ],
    author="Makar Kulishenko",
    description="Unified wrapper for CatBoost, XGBoost, LightGBM",
    long_description="Drop-in compatible wrapper for three popular gradient boosting libraries.",
    long_description_content_type="text/markdown",
    url="https://github.com/makarblch/CatBoost_changes",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
