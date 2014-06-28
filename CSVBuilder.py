# coding: utf-8
import core
import EmotionCore
import yaml
import csv
import codecs



if __name__ == '__main__':

    f = open('config.yml')
    config_data = yaml.load(f)
    f.close()
    userid_list = config_data['userid_list'].split(',')

    # itemList[0]:    id
    # itemList[1]:    user id
    # itemList[2]:    user name
    # itemList[3]:    stocklist
    # itemList[4]:    start_date
    # itemList[5]:    pricelist
    # itemList[6]:    end_date
    # itemList[7]:    end_pricelist
    # itemlist[8]:    stock price percentage
    # itemList[9]:   emotion score
    # itemList[10]:    text
    ##################init##################
    c = core.core(1)
    e = EmotionCore.EmotionalCalculator()
    e.Load()
    # This is must in order to get the cookie from xueqiu
    c.TryGetPage("http://xueqiu.com/")

    csvfile = file('test.csv','wb')
    csvfile.write(codecs.BOM_UTF8)
    csvfile.close()

    for userid in userid_list :
        ##################basic info##################

        url = "http://xueqiu.com/"+userid
        print url
        data = c.GetItemList(url)
        ##################cal emotion##################
        for row in data:
            try:
                score = e.calStart(row[10])
                row[9] = str(score)
            except:
                print "cal emotion error!"
                continue

        ##################write csv##################
        csvfile = file('test.csv', 'ab')
        csvfile.write(codecs.BOM_UTF8)
        writer = csv.writer(csvfile)
        writer.writerows(data)
        csvfile.close()
