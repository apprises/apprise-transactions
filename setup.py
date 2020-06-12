from setuptools import setup
from setuptools import find_packages

setup(
    name="apprise-transactions",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    url="https://github.com/apprises/apprise-transactions",
    keywords="Push Notifications Alerts Apprise Email AWS SNS Boxcar ClickSend "
    "Discord Dbus Emby Faast Flock Gitter Gnome Gotify Growl IFTTT Join "
    "Kavenegar KODI Kumulos MacOS Mailgun Matrix Mattermost MessageBird "
    "MSG91 Nexmo Nextcloud Notica Notifico Office365 Prowl PushBullet "
    "Pushjet Pushed Pushover PushSafer Rocket.Chat Ryver SendGrid "
    "SimplePush Sinch Slack Stride Syslog Techulus Push Telegram Twilio "
    "Twist Twitter XBMC Monero MSTeams Windows Webex CLI API",
    license="MIT",
    author="Apprises",
    author_email="",
    description="Push Notifications that work with just about every payment platform!",
    install_requires=open("requirements.txt").readlines(),
    entry_points={
        "console_scripts": ["apprisetransactions=apprisetransactions.cli:main"]
    },
    tests_require=open("dev-requirements.txt").readlines(),
)
