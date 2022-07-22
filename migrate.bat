.env\Scripts\activate.bat
cd src
manage.py makemigrations CoreApp
manage.py makemigrations LoginApp
manage.py makemigrations AdminApp
manage.py makemigrations NewsApp
manage.py makemigrations DiaryApp
manage.py makemigrations ChatApp
manage.py makemigrations ProjectApp
manage.py makemigrations ProfileApp
manage.py makemigrations MailApp
manage.py makemigrations ProjectApp
manage.py makemigrations RegisterApp
manage.py makemigrations JournalApp
manage.py makemigrations NotificationApp

manage.py migrate
