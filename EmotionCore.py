# -*- coding: utf-8 -*- 
import codecs
import copy
import re
import string


class EmotionalCalculator:
    def __init__(self):
        self.fName = {}
        self.degDict = {}
        self.dict = {}
        self.existWord = {}
        self.negDict = {}
        self.selfDict = {}
        self.wordLocation = {}
        self.origFile = []
        self.origFile1 = []
        self.eSent = []
        self.errorImfor = ""

    class pattern:
        def __init__(self, t, v, b, e):
            self.kind = t
            self.value = v
            self.begin = b
            self.end = e

    def Initialization(self):
        self.origFile = []
        self.origFile1 = []
        self.errorImfor = ""

    def readFamilyName(self):
        file = open('.\dict\FamilyName.txt', 'r')
        for line in file.readlines():
            name = line.decode('utf8')
            if not self.fName.has_key(name) and not len(name) == 0:
                self.fName[name] = 0
        file.close()

    def readDict(self):
        file = open('.\dict\WeightFull.txt', 'r')
        for line in file.readlines():
            str = line.split('\t')
            self.dict[str[0]] = str[1].replace('\n', '')
        file.close()

    def readNegDict(self):
        file = open('.\dict\NegativeFull.txt', 'r')
        for line in file.readlines():
            self.negDict[line.replace('\n', '')] = -1
        file.close()

    def readDegDict(self):
        file = open('.\dict\DegreeFull.txt', 'r')
        for line in file.readlines():
            str = line.split('\t')
            self.degDict[str[0]] = str[1].replace('\n', '')
        file.close()

    def preTreatment(self, StrList):
        self.origFile = []

        strArray = []
        file = open('.\dict\stoplistFull.txt', 'r')
        for line in file.readlines():
            strArray.append(line.replace('\n', ''))
        file.close()

        content = copy.deepcopy(StrList)
        for stopword in strArray:
            length = len(stopword.decode('utf-8'))
            utf8_length = len(stopword)
            length = (utf8_length - length) / 2
            content = [line.replace(stopword, '0' * length) for line in content]

        self.origFile.extend(content)
        self.origFile1.extend(StrList)


    def EmotionWordsInitial(self):
        file = open('.\dict\EmotionWordsFull.txt', 'r')
        for line in file.readlines():
            str = line.split('\t')
            self.existWord[str[0]] = str[1].replace('\n', '')
        file.close()

    def cal(self):
        index = -1
        for item in self.origFile:
            valueToken = 0
            if item != "":
                str2 = ""
                strArray2 = str2.split("/t")
                token = self.addMarks(item)
                d = self.paragraphEmotionCal(token, valueToken)
                num6 = 0
                n = 0


    def addMarks(self, line):
        line = self.ContainBookMark(line)
        cuts = '(.+?(?:\?|;|:|"\.|。|！|？|……|\.))'
        p = re.compile(cuts)
        r = list(filter(None, re.split(p, line)))
        return r

    def FeatureWordsReplace(self, token, m, n, kind):
        mark = kind+'*'*(m-1)
        token = token[:n*3]+mark+token[(n+m)*3:]
        return token

    def ContainBookMark(self, token):
        if '《' in token and '》' in token:
            reobj = re.compile('《.*》')
            book = re.findall(reobj, token)[0]
            length = len(book.decode('utf-8'))
            utf8_length = len(book)
            length = (utf8_length - length) / 2
            result = reobj.sub('0' * length, token)
            return result
        else:
            return token

    def ContainQuestionMarkProcess(self, token, QuestionToken):
        str = ""
        flag = False
        if "不" in token:
            num = token.index("不")
            if num != -1 and num != (len(token) - 2):
                if token[num] == token[num + 2]:
                    str = token[num] + "不" + token[num + 2]
                    QuestionToken[0] = 0
                    flag = True
                else:
                    QuestionToken[0] = 1
            elif num == -1 and "吗" in token:
                flag = True
                QuestionToken[0] = -1.1
            else:
                QuestionToken[0] = 1
        if "是否" in token:
            QuestionToken[0] = 0
            flag = True
        if ("?" in token or "？" in token) and not flag:
            if "不是" in token:
                if "不是太" in token:
                    str = "不是"
                    QuestionToken[0] = 1.1
                elif "不是很" in token:
                    str = "不是"
                    QuestionToken[0] = 1.1
                elif "是不是" in token:
                    QuestionToken[0] = 0
            elif "难道" in token and "就" in token:
                str = "难道"
                QuestionToken[0] = -1.1
            elif "就不" in token:
                str = "难道"
                QuestionToken[0] = 1.1
            elif "就" in token:
                str = "就"
                QuestionToken[0] = 1.1
            elif "还不" in token:
                str = "还不"
                QuestionToken[0] = 1.1
            elif "不是" in token and ("了" in token or "已经" in token):
                str = "不是"
                QuestionToken[0] = 1.1
            elif "怎么" in token:
                str = "怎么"
                QuestionToken[0] = 1
            elif "怎" in token:
                str = "怎"
                QuestionToken[0] = -1.2
            elif "成这样" in token:
                QuestionToken[0] = 1.2
            else:
                QuestionToken[0] = 0
        elif not flag:
            QuestionToken[0] = 1
        if len(str) != 0 and str:
            token = self.FeatureWordsReplace(token, len(str), token.index(str), 'Q')

    def ContainExclamationMarkProcess(self, token, ExclamationToken):
        str = ""
        if "无论如何" in token:
            str = "无论如何"
            ExclamationToken[0] = 1.2
        elif "不管怎样" in token:
            str = "不管怎样"
            ExclamationToken[0] = 1.2
        elif "不得不" in token and ("呀" in token or "啊" in token):
            str = "不得"
            ExclamationToken[0] = 1.3
        elif "不得" in token and ("呀" in token or "啊" in token):
            str = "不得"
            ExclamationToken[0] = 1.2
        if "!" in token or "！" in token:
            ExclamationToken = 1.1 * ExclamationToken[0]
        if len(str) != 0 and str:
            token = self.FeatureWordsReplace(token, len(str), token.index(str), 'Q')

    def Found(self, token0, n, m, fragment, kind):
        strArray = []
        num = 0
        dictionary = {}
        strr = ""
        if kind == 'e':
            strArray.append("e\t")
            num = n + len(fragment)
            strArray.append(str(num))
            strArray.append("\t")
            strArray.append(str(fragment))
            strArray.append("\t")
            num = self.dict[fragment]
            strArray.append(str(num))
            self.wordLocation[n] = string.join(strArray)
            pattern = EmotionalCalculator.pattern(kind, int(float(self.dict[fragment])), n, n + len(fragment))
            self.eSent.append(pattern)
            if not self.existWord.has_key("e " + fragment):
                self.existWord["e " + fragment] = 1
            else:
                strr = "e " + fragment
                self.existWord[strr] = str(int(self.existWord[strr]) + 1)
                dictionary = self.existWord
        elif kind == 'd':
            strArray.append("d\t")
            num = n + len(fragment)
            strArray.append(str(num))
            strArray.append("\t")
            strArray.append(str(fragment))
            strArray.append("\t")
            strArray.append(str(self.degDict[fragment]))
            self.wordLocation[n] = string.join(strArray)
            pattern = EmotionalCalculator.pattern(kind, int(float(self.degDict[fragment])), n, n + len(fragment))
            self.eSent.append(pattern)
            if not self.existWord.has_key("d " + fragment):
                self.existWord["d " + fragment] = 1
            else:
                strr = "d " + fragment
                self.existWord[strr] = str(int(self.existWord[strr]) + 1)
                dictionary = self.existWord
        else:
            strArray.append("n\t")
            num = n + len(fragment)
            strArray.append(str(num))
            strArray.append("\t")
            strArray.append(str(fragment))
            strArray.append("\t")
            strArray.append(str(self.negDict[fragment]))
            self.wordLocation[n] = string.join(strArray)
            pattern = EmotionalCalculator.pattern(kind, int(float(self.negDict[fragment])), n, n + len(fragment))
            self.eSent.append(pattern)
            if not self.existWord.has_key("n " + fragment):
                self.existWord["n " + fragment] = 1
            else:
                strr = "n " + fragment
                self.existWord[strr] = str(int(self.existWord[strr]) + 1)
                dictionary = self.existWord
        n = (n + m) - 1

    def isPartOfName(self, t, token, s):
        index = token.find(s)
        if index != 0:
            if t == "2" and index > 1:
                return self.fName.has_key(token[index - 1:index]) or self.fName.has_key(token[index - 2:index])
            if t == "2" and index == 1:
                return self.fName.has_key(token[index - 1:index])
            if self.fName.has_key(token[index - 1:index]):
                return True
            if index >= 2:
                return (self.fName.has_key(token[index - 2:index - 1]) or self.fName.has_key(
                    token[index - 2:index])) or (index >= 3 and self.fName.has_key(token[index - 3:index - 1]))
        return False

    def compareIndex(self, a, b):
        if a.begin > b.begin:
            return 1
        if a.begin == b.begin:
            return 0
        return -1

    def paragraphEmotionCal(self, token, valueToken):
        num = 0
        for i in range(0, len(token)):
            d = 0
            strArray = re.split('\(|\)|,|~| ', token[i])
            for j in range(0, len(strArray)):
                questionToken = [1]
                exclamationToken = [1]
                if j == len(strArray) - 1:
                    self.ContainQuestionMarkProcess(strArray[j], questionToken)
                    self.ContainExclamationMarkProcess(strArray[j], exclamationToken)
                else:
                    self.ContainQuestionMarkProcess(strArray[j], questionToken)

                self.eSent = []
                strr = strArray[j]
                self.wordLocation = {}
                length = 8
                if length > len(strArray[j])/3:
                    length = len(strArray[j])/3
                for k in range(length, -1, -1):
                    num9 = 0
                    str3 = ""
                    str2 = strArray[j]
                    if k > 4:
                        num9 = 0
                        while (k + num9) <= len(strArray[j])/3:
                            str3 = strArray[j][num9*3:num9*3 + k*3]
                            if self.dict.has_key(str3):
                                str2 = self.FeatureWordsReplace(str2, k, num9, 'e')
                                self.Found(str2, num9, k, str3, "e")
                                strArray[j] = str2
                            num9 += 1
                    else:
                        num9 = 0
                        while (k + num9) <= len(strArray[j])/3:
                            str3 = strArray[j][num9*3:num9*3 + k*3]
                            if self.dict.has_key(str3):
                                str2 = strArray[j]
                                strArray[j] = self.FeatureWordsReplace(strArray[j], k, num9, 'e')
                                if ((((k == 1) or (k == 2)) and (int(self.dict[str3]) > 0)) and (
                                            ((k == 1) and self.isPartOfName("1", str2, str3)) or (
                                                    (k == 2) and self.isPartOfName("2", str2, str3)))):
                                    num9 = (num9 + k) - 1
                                else:
                                    self.Found(strArray[j], num9, k, str3, "e")
                            elif self.degDict.has_key(str3):
                                strArray[j] = self.FeatureWordsReplace(strArray[j], k, num9, 'd')
                                self.Found(strArray[j], num9, k, str3, "d")
                            elif self.negDict.has_key(str3):
                                strArray[j] = self.FeatureWordsReplace(strArray[j], k, num9, 'n')
                                self.Found(strArray[j], num9, k, str3, "n")
                            num9 += 1
                if len(self.eSent) != 0:
                    self.eSent.sort(cmp=lambda x, y: self.compareIndex(x, y))
                    num10 = (self.ResultCal(0, len(self.eSent) - 1) * questionToken[0]) * exclamationToken[0]
                    d += num10
            if d != 0:
                valueToken += 1
            num += d
        return num

    def ResultCal(self, begin, end):
        num = 0
        if begin == end:
            if self.eSent[begin].kind == "e":
                return self.eSent[begin].value
            return 0
        if self.eSent[begin].kind == "e":
            return self.eSent[begin].value + self.ResultCal(begin + 1, end)
        flag = True
        flag2 = False
        if not self.eSent[begin].kind == "n":
            if (self.eSent[begin + 1].begin - self.eSent[begin].end) > 3:
                return self.ResultCal(begin + 1, end)
            num = 0
            for num in range(begin, num < end, 1):
                if (self.eSent[num + 1].kind == "d") or ((self.eSent[num + 1].begin - self.eSent[num].end) > 3):
                    break
        else:
            if (self.eSent[begin + 1].begin - self.eSent[begin].end) > 3:
                return (-1 * self.ResultCal(begin + 1, end)) * 0.8
            num = 0
            num = begin
            while num < end:
                if (self.eSent[num + 1].kind == "n") and (num != (begin + 1)):
                    break
                if (self.eSent[num + 1].kind == "d") and (num != (begin + 1)):
                    flag = False
                    break
                if (self.eSent[num + 1].begin - self.eSent[num].end) > 3:
                    flag2 = True
                    break
                num += 1
            if (num == end) or (((num + 1) == end) and not flag2):
                return (-1 * self.ResultCal(begin + 1, end)) * 0.8
            if (num == begin) and flag:
                return self.ResultCal(begin + 2, end) * 1.1
            if (num == begin) and not flag:
                if self.eSent[num + 1].value < 1:
                    return (self.eSent[num + 1].value * 3) * self.ResultCal(begin + 2, end)
                return ((1 / self.eSent[num + 1].value) * self.ResultCal(begin + 2, end)) * -1
            return ((-1 * self.ResultCal(begin + 1, num)) * 0.8) + self.ResultCal(num + 1, end)
        if num == end:
            return self.eSent[begin].value * self.ResultCal(begin + 1, end)
        if self.eSent[begin + 1].kind == "d":
            if (begin + 1) != end:
                return (self.eSent[begin].value * self.eSent[begin + 1].value) * self.ResultCal(begin + 2, end)
            return 0
        return (self.eSent[begin].value * self.ResultCal(begin + 1, num)) + self.ResultCal(num + 1, end)

    def Load(self):
        self.readFamilyName()
        self.readDict()
        self.readNegDict()
        self.readDegDict()

    def calStart(self, content):
        self.Initialization()
        self.preTreatment(content)
        self.EmotionWordsInitial()
        token = self.addMarks(content)
        return self.paragraphEmotionCal(token,0)
        # return self.cal()





