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
        self.labels = {}
        self.requireValueBiding = False

    def addValue(self, v, requireValueBiding:bool = False) -> bool:
        if self.lvalue == None:
            self.lvalue = v
            if requireValueBiding:
                self.requireValueBiding = True
                self.labels[v] = {"obj": 0}
            print("Condition: added L-value")
        else:
            self.rvalue = v
            if requireValueBiding:
                self.requireValueBiding = True
                self.labels[v] = {"obj": 1}
            print("Condition: added R-value")
            return True
        return False

    def addFunction(self, f):
        self.function = f
        print("Condition: function set")
    def bindValues(self, data) ->None:
        if self.requireValueBiding:
            for label in self.labels:
                if label in data:
                    if self.labels[label]['obj'] == 0: 
                        self.lvalue = data[label]
                    else:
                        self.rvalue = data[label]
                    

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
        elif c == "'":
            buff = ''
            j = index+1
            innerBracets = 0
            while j < length:
                ic = sample[j]
                if sample[j] == "'" and j-1 >= 0 and sample[j-1] != '\\':
                    break
                
                buff += ic
                j += 1

            if cond.addValue(buff):
                currentClaus.setCondition(cond)
                cond = Condition()
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
            
            if cond.addValue(buff, True):
                currentClaus.setCondition(cond)
                cond = Condition()         
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
            index += 1
        elif c == '=' and index+1 < length and sample[index+1] == '=':
            cond.addFunction(eq)
            index += 1
        elif c == '<' and index+1 < length and sample[index+1] == '=':
            cond.addFunction(le)
            index += 1
        elif c == '<':
            cond.addFunction(lt)
        elif c == '>' and index+1 < length and sample[index+1] == '=':
            cond.addFunction(ge)
            index += 1
        elif c == '>':
            cond.addFunction(gt)
        else:
            pass
        index += 1


    return collection

def evaluate_condition(collection:list[ConditionClaus()], data:{} = None):
    resultCollection = []
    for c in collection:
        result = True
        if c.isLinkClaus(): 
            # islinkclaus ||
            ls = evaluate_condition(c.innerRelatedConditions)
            #print("Sub condition :"+repr(ls))
            result = ls
        else:
            cond = c.condition
            if cond == None: # in case 1==1 && (0 > 9) the new ConditionClaus.condition would be none
                raise Exception("ConditionClaus.condtion is None")

            if data != None:
                cond.bindValues(data)
            result = cond.function(cond.lvalue, cond.rvalue)

        resultCollection.append(result)
        # islinkclaus &&
        ic = c.next
        while ic != None:
            cond = ic.condition
            if ic.isLinkClaus():
                ls = evaluate_condition(ic.innerRelatedConditions)
                #print("Sub condition :"+repr(ls))
                if ls == False:
                    resultCollection.append(False)
                    break
            if cond == None: 
                break
            #print(str(cond.lvalue) + "/" + str(cond.rvalue))
            if data != None:
                cond.bindValues(data)
            iresult = cond.function(cond.lvalue, cond.rvalue)
            if iresult == False:
                resultCollection.append(False)
                break

            ic = ic.next

        #print(resultCollection) 
    return True in resultCollection


dataRow = []
dataRow.append({
    "ID": 15,
    "Name": "Mohammad s. Albay",
    "Age": 24,
    "Birthdate": "24-4-1999"
})
dataRow.append({
    "ID": 16,
    "Name": "Abdo s. Albay",
    "Age": 20,
    "Birthdate": "24-4-1999"
})
dataRow.append({
    "ID": 17,
    "Name": "Salma Tresh",
    "Age": 52,
    "Birthdate": "24-4-1976"
})

print("Process: Building condition...")
c = parse_condition("ID < 17 && Age <= 24")
if c == None or c.__len__() == 0:
    print("Process: Error, faield to build condition")
else:
    print("Process: data selection phase...")
    for data in dataRow:
        if evaluate_condition(c,data):
            print ("Passed : "+ repr(data))
        else:
            print ("Not passed : "+ repr(data))
