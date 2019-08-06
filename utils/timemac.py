from datetime import datetime,timedelta,date
from config import time_zone
import time

time_model = '%Y-%m-%d %H:%M:%S'
day_model = '%Y-%m-%d'
chn_model = '%Y{y}%m{m}%d{d} %H{M}'

def strptime(dt = ''):
    if dt:
        dt = datetime.strptime(dt, time_model)
    else:
        dt = datetime.now()
    return dt

def strftime(dt:datetime = None):
    if dt:
        dt = dt.strftime(time_model)
    else:
        dt = (datetime.now()).strftime(time_model)
    return dt

def in_time_interval(start:str,interval:int):
    if type(start) == str:
        time_start = strptime(start)
    else:
        time_start = start
    return time_start+timedelta(seconds=interval) > datetime.now()

def today_range():
    day_start = datetime.strptime(str(datetime.now()).split(' ')[0], day_model)
    end = day_start + timedelta(days=1)
    return (day_start,end)

def strf_chn(dt:datetime = None):
    if dt:
        return datetime.strftime(dt,chn_model).format(y='年', m='月', d='日',M = '时')
    else:
        return datetime.now().strftime(chn_model).format(y='年', m='月', d='日',M = '时')

def time_jump(s=0,mi=0,h=0,d=0,dt = None):
    if not dt:
        return datetime.now()+timedelta(seconds=s,minutes=mi,hours=h,days=d)
    else:
        return dt+timedelta(seconds=s,minutes=mi,hours=h,days=d)

def month_range():
    now = datetime.now()
    month,year,day = 1,1,1
    if now.month == 12:
        month = 1
        year = now.year + 1
    else:
        month = now.month + 1
        year = now.year
    return (date(now.year,now.month,day),date(year,month,day))

def today():
    return datetime.now().strftime(day_model)

def yestoday():
    return (date.today() + timedelta(days=-1)).strftime('%Y-%m-%d')

def timecode():
    return datetime.now().strftime('%y%m%d%H%M%S')

def now():
    return datetime.now()

def timestamp(dt=None,model=None):
    if dt:
        model = model if model else time_model
        dt = datetime.strptime(dt, model)
    else:
        dt = datetime.now()
    return dt.timestamp()

#时间戳转时间
def from_timestamp(timestamp):
    timeArray = time.localtime(timestamp)
    dt = time.strftime(time_model, timeArray)
    return datetime.strptime(dt,time_model)

def stamp2datetime(stamp:int):
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(stamp))

def cur_month_day(day:int):
    today = time.strftime(day_model)
    return datetime.strptime(today,day_model).replace(day=day)

def last_month_chn():
    now = datetime.now()
    first_day = '{0}-{1}-{2}'.format(now.year,now.month,"01")
    last_month = datetime.strptime(first_day,"%Y-%m-%d")-timedelta(days=1)
    last_month = last_month.strftime("%Y-%m-").replace("-","年",1).replace("-","月",1)
    return last_month

def next_month_earned_day(earn_day):
    today = datetime.now()
    _first_day = "{0}-{1}-01 00:00:00".format(today.year, today.month)
    _first_day = datetime.strptime(_first_day,time_model)
    next_month = _first_day + timedelta(days=40)
    next_month = "{0}年{1}月{2}日".format(next_month.year, next_month.month,earn_day)
    return next_month






