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
            'ex01_hello = ev3_exercises.ex01_hello:main',
            'ex02_drive_forward = ev3_exercises.ex02_drive_forward:main',
            'ex03_turn = ev3_exercises.ex03_turn:main',
            'ex04_timed_move = ev3_exercises.ex04_timed_move:main',
            'ex05_track = ev3_exercises.ex05_track:main',
            'ex06_odom = ev3_exercises.ex06_odom:main',
            'ex01_hello_solution = ev3_exercises.solutions.ex01_hello:main',
            'ex02_drive_forward_solution = ev3_exercises.solutions.ex02_drive_forward:main',
            'ex03_turn_solution = ev3_exercises.solutions.ex03_turn:main',
            'ex04_timed_move_solution = ev3_exercises.solutions.ex04_timed_move:main',
            'ex05_track_solution = ev3_exercises.solutions.ex05_track:main',
            'ex06_odom_solution = ev3_exercises.solutions.ex06_odom:main',
        ],
    },
)
