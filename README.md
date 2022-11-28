Device Tracking App:
- Allows register companies
- Allows register employees and staff if user logged in (and has is_company status True)
- Allows register devices and device delegation for logged in staff and company
- Automatically counts device delegation's duration days


### Installation
- clone git repo 
```
git clone https://github.com/Zharkyn20/device_tracking_app.git
```
- mv to device_tracking_app
```
cd device_tracking_app
```
- install requirements
```
pip install -r requirements.txt
```
- run script
```
python3 manage.py makemigrations
```
```
python3 manage.py migrate
```
```
python3 manage.py runserver
```
