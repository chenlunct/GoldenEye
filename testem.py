#coding=utf-8
import EmotionCore
import codecs


e = EmotionCore.EmotionalCalculator()
# e.readFamilyName()
# print e.fName.keys()[8].decode('utf8')
# e.readDict()
# print e.dict.keys()[8].decode('utf8')
# e.readNegDict()
# print e.negDict.keys()[8].decode('utf8')
# e.readDegDict()
# print e.degDict.keys()[8].decode('utf8')
# strList=[u'今天运行运行运行不改运行'.encode('utf8'),u'不改不改不改今天依旧天气好差'.encode('utf8')]
# e.preTreatment(strList)
# print e.origFile[0].decode('utf8')
# print e.origFile[1].decode('utf8')
# print e.origFile1[0].decode('utf8')
# print e.origFile1[1].decode('utf8')
# e.EmotionWordsInitial()
# print e.existWord.keys()[8].decode('utf8')
# e.ContainBookMark(u'我昨天看了本书叫《一二三四五六七》觉得没什么用'.encode('utf8'))
# print e.addMarks(u'第一。第二？第三.第四?第五；第六;'.encode('utf8'))[1].decode('utf8')
# score = [0]
# e.ContainQuestionMarkProcess(u'客观你不可以啊'.encode('utf8'),score)
# print score
# token = "你是个e*！"
# n=3
# e.Found(token,n,2,"坏人","e")
# print token,n
# print e.isPartOfName("a", "aaabbbccc", "bb")
e.Load()
print e.calStart('''回复<a href="http://xueqiu.com/n/陆上小白龙"  target="_blank">@陆上小白龙</a>: 绝对的挚爱，再涨一些就超过伊利成我第一重仓股<img src="http://js.xueqiu.com/images/face/21lol.png" title="[大笑]" alt="[大笑]"   height="24" />//<a href="http://xueqiu.com/n/陆上小白龙"  target="_blank">@陆上小白龙</a>:回复<a href="http://xueqiu.com/n/疯狂_de_石头"  target="_blank">@疯狂_de_石头</a>:这个欧亚简直就是你的至爱嘛。 真那么好？''')