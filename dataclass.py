from pydantic import BaseModel

class GPS(BaseModel):
    lat : float
    long : float


class Air(BaseModel):
    pm1 : float
    pm2_5 : float
    pm10 : float

class Gas(BaseModel):
    co : float
    no2 : float
    nh3 : float


class DataModel(BaseModel):
    temp : float
    pressure : float
    humidity : float
    lux : float
    geiger : float
    gas : Gas
    air : Air
    gps : GPS
    cam : str
    tcam : str


