import datetime
from datetime import timedelta
today = datetime.date.today()
tomorrow = today + timedelta(days=1)
todayWithTime = datetime.datetime.strptime(str(today) + " " + "01:44:03", "%Y-%m-%d %H:%M:%S")
todayWithLaterTime = datetime.datetime.strptime(str(today) + " " + "23:44:03", "%Y-%m-%d %H:%M:%S")
tomorrowWithTime = todayWithTime + timedelta(days=1)
print(todayWithTime < tomorrowWithTime)
print(todayWithTime < todayWithLaterTime)

