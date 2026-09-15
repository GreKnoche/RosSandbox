from setuptools import find_packages, setup

package_name = 'ev3_exercises'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='GreKnoche',
    maintainer_email='todo@todo.todo',
    description='ROS-2-Übungsnodes mit Lücken für cmd_vel und Odometrie',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'uebung1 = ev3_exercises.uebung1:main',
            'uebung2 = ev3_exercises.uebung2:main',
            'uebung3 = ev3_exercises.uebung3:main',
            'uebung4 = ev3_exercises.uebung4:main',
            'uebung5 = ev3_exercises.uebung5:main',
            'uebung6 = ev3_exercises.uebung6:main',
            'uebung1_solution = ev3_exercises.solutions.uebung1:main',
            'uebung2_solution = ev3_exercises.solutions.uebung2:main',
            'uebung3_solution = ev3_exercises.solutions.uebung3:main',
            'uebung4_solution = ev3_exercises.solutions.uebung4:main',
            'uebung5_solution = ev3_exercises.solutions.uebung5:main',
            'uebung6_solution = ev3_exercises.solutions.uebung6:main',
        ],
    },
)
