from setuptools import setup, find_packages

setup(
    name="imu_covariance_models",
    version="0.1",
    description="covariance models with IMU noises - simulation and real examples",
    author="Jagatpreet Singh Nir",
    author_email="nir.j@northeastern.edu",
    packages=find_packages(),
    install_requires=["gtsam", "maptlotlib", "pathlib", "typing"],
    keywords=["python", "imu covariance"],
    entry_points={
        'console_scripts':[
            'run_simulation=imu_covariance_models.simulation:main',            
        ]
    }
)