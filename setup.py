'''this file is present to store the essential details about the projec such as it's meta-data and configuration .
It is used for distributing and packaging the project.
Used by setuptools.'''
from setuptools import find_packages , setup
from typing import List

requirement_list:List[str]=[]
def get_requirements()->List[str]:
    """This function will return list of requirements"""
    try:
        with open("requirements.txt",'r') as file:
            lines=file.readlines()
            #Process each line 
            for line in lines:
                requirement=line.strip()
                #will be ignoring empty  lines and -e.
                if requirement and requirement !="-e .":
                    requirement_list.append(requirement)

    except FileNotFoundError:
        print("Requirements file not found")
    return requirement_list

setup(
    name="Network Security",
    version="1.0.0",
    description="This is a network security project",
    author="Hardik Kumar",
    author_email="Hardikkumar@885@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)



