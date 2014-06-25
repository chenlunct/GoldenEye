import core
import StockInfo
import EmotionCore
import csv

if __name__ == '__main__':
    # data[0]:    id
    # data[1]:    create time
    # data[2]:    user id
    # data[3]:    stocklist
    # data[4]:    text
    # data[5]:    emotion score
    ##################init##################
    c = core.core(1)
    e = EmotionCore.EmotionalCalculator()
    e.Load()
    s = StockInfo.StockInfo()

    ##################basic info##################
    c.TryGetPage("http://xueqiu.com/")
    data = c.GetItemList("http://xueqiu.com/4080074145")

    ##################cal emotion##################
    for row in data:
        try:
            score = e.calStart(row[4])
            row[5] = str(score)
        except:
            print "cal emotion error!"
            continue

    ##################write csv##################
    csvfile = file('test.csv', 'wb')
    writer = csv.writer(csvfile)
    writer.writerows(data)
    csvfile.close()
