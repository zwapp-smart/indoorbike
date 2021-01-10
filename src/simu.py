'''
MIT License

Copyright (c) 2021 zwapp-smart

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

from zwapputil import debug

class Conversion():

    POWER_K = 0.8 * (60 * 9.80665) / (360 * 0.95 * 100) # 体重(60kg)

    def __init__(self):
        self._speedX = 1.0
        self._a = 0.9       # 斜度(%)-傾き
        self._b = 0.6       # 斜度(%)-切片

    def convSpeed(self, speed100):
        return self._speedX * speed100
    
    def calcPower(self, speed100, incline):
        # https://diary.cyclekikou.net/archives/15876
        return int(speed100 * (self._a*(incline-1)+self._b) * self.POWER_K)

c = Conversion()

def speedAndWatt(args):
    '''
    parameters
    -----
        args:tuple
        (
            [0] speed100:int,   unit - 0.01 km/h        Bike Speed
            [1] incline:int,    unit - level (1-24)     Incline Level
            [2] heartrate:int,  unit - bpm              Heartrate (=0)
            [3] cadence:int,    unit - rpm              Cadence (=0,1)
            [4] watt:int,       unit - watt             Power (=0)
        )
    
    return
    -----
        return:tutple
        (
            [0] speed100:int,   unit - 0.01 km/h    Bike Speed
            [1] watt:int,       unit - watt         Power
        )
    '''
    speed100 = c.convSpeed(args[0])
    watt = c.calcPower(speed100, args[1])
    debug("SPEED AND WATT: {} => {}".format(args, (speed100, watt,)))
    return (speed100, watt,)

class Grade100Threshold():
    def __init__(self):
        self._grade100={}
        self._grade100[ '1']= -420
        self._grade100[ '2']= -300
        self._grade100[ '3']= -180
        self._grade100[ '4']=  -60
        self._grade100[ '5']=   30
        self._grade100[ '6']=   60
        self._grade100[ '7']=   90
        self._grade100[ '8']=  120
        self._grade100[ '9']=  150
        self._grade100['10']=  200
        self._grade100['11']=  330
        self._grade100['12']=  420
        self._grade100['13']=  600
        self._grade100['14']=  690
        self._grade100['15']=  870
        self._grade100['16']=  960
        self._grade100['17']= 1140
        self._grade100['18']= 1230
        self._grade100['19']= 1410
        self._grade100['20']= 1500
        self._grade100['21']= 1680
        self._grade100['22']= 1770
        self._grade100['23']= 1950

        self._speed100={}
        self._speed100[ '1']=2000
        self._speed100[ '2']=3000
        self._speed100[ '3']=3500
        self._speed100[ '4']=3000
        self._speed100[ '5']=4500
        self._speed100[ '6']=5000
        self._speed100[ '7']=5500
        self._speed100[ '8']=6000
        self._speed100[ '9']=6300
        self._speed100['10']=6600
        self._speed100['11']=6900
        self._speed100['12']=7000
        
    def _getIncline(self, grade100):
        a = 0
        for v in range(len(self._grade100)):
            k = v+1
            if self._grade100["{}".format(k)]<grade100:
                a = k
            else:
                break
        return a+1
    
    def _getOffset(self, speed100):
        a = 0
        for v in range(len(self._speed100)):
            k = v+1
            if self._speed100["{}".format(k)]<speed100:
                a = k
            else:
                break
        return a

    def calcIncline(self, grade100, speed100):
        #return self._getIncline(grade100)+self._getOffset(speed100)
        return self._getIncline(grade100)

g = Grade100Threshold()

def simulateBike(args):
    '''
    parameters
    -----
        args:tuple
        (
            [0] windSpeed1000:int,  unit - 0.001 m/sec  Wind Speed
            [1] grade100:int,       unit - 0.01 %       Grade
            [2] crr10000:int,       unit - 0.0001       Crr (Coefficient of Rolling Resistance)
            [3] cw100:int,          unit - 0.01 kg/m    Cw (Wind Resistance Coefficient)
            [4] speed100:int,       unit - 0.01 km/h    Bike Speed
        )
    
    return
    -----
        return:tutple
        (
            [0] incline,            unit - level (1-24) Incline Level
        )
    '''
    incline = g.calcIncline(args[1], args[4])
    debug("SIMULATE BIKE: {} => {}".format(args, incline))
    return (incline,)
