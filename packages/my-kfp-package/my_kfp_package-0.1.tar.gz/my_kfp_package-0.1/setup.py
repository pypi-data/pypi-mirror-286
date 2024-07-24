from setuptools import setup, find_packages

setup(
    name='my_kfp_package',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'kfp',
        'google-cloud-storage',
        'pandas',
    ],
    include_package_data=True,
    description='A package containing Kubeflow Pipelines components',
    url='https://github.com/githubuserohith/my_kfp_package',
    author='Rohith',
    author_email='your.email@example.com',
    license='MIT',
)
