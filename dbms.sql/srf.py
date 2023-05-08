def lt(v1, v2):
    return v1 < v2
def eq(v1, v2):
    return v1 == v2
def le(v1, v2):
    return v1 <= v2;
def gt(v1, v2):
    return v1 > v2;
def ge(v1, v2):
    return v1 >= v2;
def ne(v1, v2):
    return v1 != v2

class Condition:
    def __init__(self):
        self.lvalue = None
        self.rvalue = None
        self.function = None

    def addValue(self, v) -> bool:
        if self.lvalue == None:
            self.lvalue = v
            print("Condition: added L-value")
        else:
            self.rvalue = v
            print("Condition: added R-value")
            return True
        return False

    def addFunction(self, f):
        self.function = f
        print("Condition: function set")

class ConditionClaus:
    def __init__(self):
        self.condition:Condition = None
        self.next: ConditionClaus() = None
        self.linkclaus = False
        self.innerRelatedConditions = []
    def addRequired(self, cc) -> None:
        self.next = cc
    def setCondition(self, c:Condition()) ->None:
        self.condition = c
    def setAsLink(self, ls):
        self.linkclaus = True
        self.innerRelatedConditions = ls
    def isLinkClaus(self) -> bool:
        return self.linkclaus


# select id from students where name= 'Ali' and (age = 80 || abs(age) < 20+5)
def parse_condition(sample: str) -> list[ConditionClaus()]:
    resultCollection = []

    index = 0
    length = len(sample)

    collection = []
    collection.append(ConditionClaus())

    currentClaus = collection[0]
    cond = Condition()
    currentFunction = None
    lastOperand = None
    while index < length:
        c = sample[index]

        if c == ' ':
            index += 1
            continue
        elif c == '(':
            buff = ''
            j = index+1
            innerBracets = 0
            while j < length:
                if sample[j] == '(':
                    innerBracets += 1
                elif sample[j] == ')':
                    innerBracets -= 1
                
                if innerBracets <= -1:
                    break
                    
                buff += sample[j]
                j += 1
            
            #if lastOperand == '&&':
            currentClaus.setAsLink(parse_condition(buff))
            index = j
        elif c.isalpha():
            buff = c
            j = index + 1
            while j < length:
                if not sample[j].isalpha():
                    j -= 1
                    break
                else:
                    buff += sample[j]

                j += 1
            if cond.addValue(buff):
                currentClaus.setCondition(cond)
                cond = Condition()
            print("Collected : "+buff)            
            index = j
        elif c.isdigit() or (c == '-' and index+1 < length and sample[index+1].isdigit()):
            buff = c
            j = index + 1
            is_real = False
            while j < length:
                if sample[j] == '.':
                    is_real  =True
                if not sample[j].isdigit() and sample[j] != '.':
                    j -= 1
                    break
                else:
                    buff += sample[j]

                j += 1
            if cond.addValue(float(buff) if is_real else int(buff)):
                currentClaus.setCondition(cond)
                
            index = j
        elif c == '&' and index+1 < length and sample[index+1] == '&':
            currentClaus.addRequired(ConditionClaus())
            currentClaus = currentClaus.next # points to the next condition
            cond = Condition()
            lastOperand = '&&'
            print("Linked Section to previous claus created")
            index += 1
        elif c == '|' and index+1 < length and sample[index+1] == '|':
            collection.append(ConditionClaus())
            currentClaus = collection[len(collection)-1]
            cond = Condition()
            lastOperand = '||'
            print("New Section created")
            index += 1
        elif c == '!' and index+1 < length and sample[index+1] == '=':
            cond.addFunction(ne)
        elif c == '=':
            cond.addFunction(eq)
        elif c == '<' and index+1 < length and sample[index+1] == '=':
            cond.addFunction(le)
        elif c == '<':
            cond.addFunction(lt)
        elif c == '>' and index+1 < length and sample[index+1] == '=':
            cond.addFunction(ge)
        elif c == '>':
            cond.addFunction(gt)
        else:
            pass
        index += 1


    return collection

def evaluate_condition(collection:list[ConditionClaus()]):
    resultCollection = []
    for c in collection:
        result = True
        if c.isLinkClaus(): 
            # islinkclaus ||
            ls = evaluate_condition(c.innerRelatedConditions)
            print("Sub condition :"+repr(ls))
            result = ls
        cond = c.condition
        if cond != None: # in case 1==1 && (0 > 9) the new ConditionClaus.condition would be none
            print("L:"+str(cond.lvalue) + ", R:"+ str(cond.rvalue))
            result = cond.function(cond.lvalue, cond.rvalue)

        # islinkclaus &&
        ic = c.next
        while ic != None:
            cond = ic.condition
            if ic.isLinkClaus():
                ls = evaluate_condition(ic.innerRelatedConditions)
                print("Sub condition :"+repr(ls))
                if ls == False:
                    result = False
                    break
            if cond == None: 
                break
            print(str(cond.lvalue) + "/"+ str(cond.rvalue))
            iresult = cond.function(cond.lvalue, cond.rvalue)
            if iresult == False:
                result = False
                break

            ic = ic.next
        resultCollection.append(result)
        print(resultCollection) 
    return True in resultCollection

c = parse_condition("2 > 1 && (A=A && (1==1.1 || 9<5))")
print("result is  "+str(evaluate_condition(c)))
