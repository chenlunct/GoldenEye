import urllib
import time
import datetime

debug=True
class StockInfo:
    csvbody = ""
    stockitem = ""

    # change the format from SZ600000 to 600000.SZ
    # change the format from SH600000 to 600000.SS
    def IDformat(self,ID):
        prefix = ID[0:2]
        if prefix == 'SH':
            myid = ID[2:8] + '.SS'
        elif prefix == 'SZ':
            myid = ID[2:8] + '.SZ'
        else:
            myid = '000000.SS'
        return myid

    # return the Yahoo style list [year,month,day]
    def DateParam(self,qdate):
        mydate = time.strptime(qdate,'%Y-%m-%d')
        # The yahoo interface requires month starting from '00'
        tmonth = int( time.strftime('%m',mydate) )
        month = str(tmonth - 1).zfill(2)
        day = time.strftime('%d',mydate)
        year = time.strftime('%Y',mydate)
        dstream = [year,month,day]
        return dstream

    # Change the input date of Saturday/Sunday to last Friday since Sat/Sun is invalidate date.
    def AlignDate(self,startdate):
        x = time.strptime(startdate,'%Y-%m-%d')
        sdate = datetime.datetime(x[0],x[1],x[2] )
        # Saturday & Sunday is not a valid date
        if sdate.weekday() == 5 :
            sdate = sdate + datetime.timedelta(days = -1 )
        if sdate.weekday() == 6 :
            sdate = sdate + datetime.timedelta(days = -2 )

        return sdate.strftime('%Y-%m-%d')

    # Return  startdate + ndays under YYYY-MM-DD format
    def PlusDate(self,startdate,ndays):
        x = time.strptime(startdate,'%Y-%m-%d')
        sdate = datetime.datetime(x[0],x[1],x[2] )
        edate = sdate + datetime.timedelta(days = ndays )

        # Saturday & Sunday is not a valid date
        if edate.weekday() == 5 :
            edate = edate + datetime.timedelta(days = -1 )
        if sdate.weekday() == 6 :
            edate = edate + datetime.timedelta(days = -2 )

        return edate.strftime('%Y-%m-%d')

    # Function : Read the stock csv file from Yahoo interfaces
    # Save the stock csv file into local file.
    # startdate should be on the format of 'yyyy-mm-dd'
    # ndays means the enddate = qdate + ndays
    def GetStockStrByNum(self,ID,startdate):
        startdate = self.AlignDate(startdate)
        myid = self.IDformat(ID)
        s = self.DateParam(startdate)
        # Yahoo query interface is : &a=mm&b=dd&c=yyyy
        startfrom = '&a='+s[1]+'&b='+s[2]+'&c='+s[0]
        endto = '&d='+s[1]+'&e='+s[2]+'&f='+s[0]
        myurl = 'http://ichart.yahoo.com/table.csv?s='+ myid + startfrom + endto +'&g=d'
        #print myurl
        # retrieve csf info from remote url
        f = urllib.urlopen(myurl)
        self.csvbody = f.readlines()
        f.close()
        if len(self.csvbody) == 2 :
            self.stockitem = self.csvbody[1].split(',')
            return True
        else :
            return False


def Main():
    c = StockInfo()
    if c.GetStockStrByNum('SZ002312','2014-06-25') :
        print c.stockitem
    else :
        print "Unable to retrieve stock info"

Main()
