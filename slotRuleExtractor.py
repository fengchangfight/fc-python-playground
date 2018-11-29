import spacy
import re

class FrameRuleExtract(object):
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')

    class SlotResult(object):
        def __init__(self, key, val, type):
            self.key = key
            self.val = val
            self.type = type
        def __repr__(self):
            return self.key + ":" + self.val + ":" + self.type

    def match_rule(self, sentence, rule_expression, keylist):
        result = []
        print(sentence)
        matchObj = re.match(rule_expression, sentence, re.M | re.I)
        kl = keylist.split(",")
        if(matchObj==None):
            pass
        else:
            for i in range(len(matchObj.groups())):
                if(i<len(kl)):
                    print("Inserting item: ", kl[i] ,matchObj.group(i+1))
                    item = FrameRuleExtract.SlotResult(kl[i],matchObj.group(i+1),"by_rule")
                    result.append(item)
        print(result)
        return result

rule_expression = ".* from (\w+) to (\w+)"
sentence = "I would like to book a ticket from Shanghai to Beijing."
keylist = "origin,destination"
obj = FrameRuleExtract()
obj.match_rule(sentence, rule_expression, keylist)



