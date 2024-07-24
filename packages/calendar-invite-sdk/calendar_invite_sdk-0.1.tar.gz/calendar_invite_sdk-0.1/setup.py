from setuptools import setup, find_packages

setup(
    name='calendar_invite_sdk',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'dateparser',
        'ics',
        'slack_sdk'
    ],
    entry_points={
        'console_scripts': [
            'calendar-invite-sdk=main:main',
        ],
    },
)
