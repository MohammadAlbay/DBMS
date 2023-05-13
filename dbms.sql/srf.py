import copy

def lt(v1, v2):
    return v1 < v2
def eq(v1, v2):
    return v1 == v2
def li(v1:str, v2:str):
    return v1.__contains__(v2)
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
        self.lvalue:Operand = None
        self.rvalue:Operand = None
        self.function = None
        self.labels = {}
        self.requireValueBiding = False

    def addValue(self, v, requireValueBiding:bool = False) -> bool:
        if self.lvalue == None:
            self.lvalue = v
        else:
            self.rvalue = v
            return True
        return False

    def addFunction(self, f):
        self.function = f
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

def sumNumbers(n1, n2):
    return n1+n2
def sumString(s1, s2):
    return s1+s2
def sumStringNumber(s1:str, n1):
    return s1+str(n1)

MethodMap = {
    '+' : {
        "TowNumbers" : lambda a,b : a + b,
        "TowStrings" : lambda a,b : a + b,
        "OneStringOneNumber" : lambda a,b : a + str(b),
        "SupportedTypes" : ['int', 'float', 'string']
    },
    '-' : {
        "TowNumbers" : lambda a,b : a - b,
        "TowStrings" : None,
        "OneStringOneNumber" : None,
        "SupportedTypes" : ['int', 'float']
    },
    '*' : {
        "TowNumbers" : lambda a,b : a * b,
        "TowStrings" : None,
        "OneStringOneNumber" : None,
        "SupportedTypes" : ['int', 'float']
    },
    '/' : {
        "TowNumbers" : lambda a,b : a / b,
        "TowStrings" : None,
        "OneStringOneNumber" : None,
        "SupportedTypes" : ['int', 'float']
    },
    '^' : {
        "TowNumbers" : lambda a,b : pow(a,b),
        "TowStrings" : None,
        "OneStringOneNumber" : None,
        "SupportedTypes" : ['int', 'float']
    }
}


class Operand:
    def __init__(self):
        self.elements:list = []
        self.operators:list[str] = []
        self.inlineValues: list[Operand] = []
        self.__containsDynamicElements: bool = False
        self.__prepared:bool = False
    def addElement(self, v, type):
        self.elements.append({"value": v, "type": type})
    def addOperator(self, o):
        self.operators.append(o)

        length = self.operators.__len__()
        if length > self.elements.__len__():
            numberToAdd = 0
            if o == '/' or o == '*':
                numberToAdd = 1
            if length > 0: 
                prev_operator = self.operators[length-1]
                if prev_operator == '/' or prev_operator == '*':
                    numberToAdd = 1
                
            self.addElement(numberToAdd, "int")
    def addInlineOperand(self, op):
        self.inlineValues.append(op)
        self.elements.append(None)
    def setContainsDynamicElements(self, b):
        self.__containsDynamicElements = b
    def prepare(self, dataRow) -> list:
        newElement: list = None
        if self.__containsDynamicElements:
            import copy
            newElement = copy.deepcopy(self.elements)
        else: 
            if self.__prepared:
                return self.elements
            newElement = self.elements
        index = 0
        length = len(newElement)
        inlineIndex = 0
        while index < length:
            item = newElement[index]
            if item == None:
                inlineValue = self.inlineValues[inlineIndex]
                newElement[index] = inlineValue.solve(dataRow)
                inlineIndex += 1
            elif item["type"] == 'var':
                varInfo = getVariable(item["value"])
                if varInfo == None:
                    raise Exception("Operand Process: failed to bind value for variable '"+item["value"]+"'")
                else:
                    newElement[index] = varInfo
            elif item["type"] == 'column':
                colInfo = getColumn(item["value"])
                if colInfo == None:
                    raise Exception("Operand Process: failed to bind value for column '"+item["value"]+"'")
                else:
                    if item["value"] in dataRow:
                        newElement[index]['value'] = dataRow[item["value"]]
                    else:
                        newElement[index]['value'] = colInfo['default']
                    newElement[index]['type'] = colInfo['type']
                    
            index += 1
        
        if not self.__containsDynamicElements:
            self.__prepared = True
            self.elements = newElement
            return self.elements
        return newElement
    def __try0(self, items: list) -> []:
        finalSet = items
        ops = copy.deepcopy(self.operators)
        implementation_piority = [['^'], ['*', '/'], ['+', '-']]
        
        length = len(ops)
        ip_index = 0
        
        if len(finalSet) == 1:
            return finalSet[0]
        
        while ip_index < implementation_piority.__len__():
            index = 0
            while length > 0 and index < ops.__len__():
                
                current_operator = ops[index]
                if current_operator in implementation_piority[ip_index]:
                    # now we need values  at 1, +1 index from elements
                    function_bundle = MethodMap[current_operator]
                    l = finalSet[index]
                    r = finalSet[index+1]
                    ltype = l['type']
                    rtype = r['type']

                    if not ltype  in function_bundle['SupportedTypes'] or not rtype in function_bundle['SupportedTypes']:
                        raise Exception("Data type error. cannot use types : ("+ltype + " and/or "+rtype + ") with operator '"+current_operator+"'")
                    # so far so good...
                    # into the business..
                    if ltype == 'int' or ltype == 'float': 
                        if rtype == 'int' or rtype == 'float':
                            function = function_bundle["TowNumbers"](l['value'], r['value'])
                            finalType = 'int' if isinstance(function, int) else 'float'
                        elif rtype == 'string':
                            function = function_bundle["OneStringOneNumber"](r['value'], l['value'])
                            finalType = 'string'
                
                    elif ltype == 'string':
                        if rtype == 'string':
                            function = function_bundle["TowStrings"](l['value'], r['value'])
                        elif rtype == 'int' or rtype == 'float':
                            function = function_bundle["OneStringOneNumber"](l['value'], r['value'])
                        finalType = 'string'
            
                    finalSet[index+1] = {"type": finalType, "value": function}
                    
                    # if ltype == 'string':
                    #     finalSet[index]['value'] = ''
                    # else:
                    #     finalSet[index]['value'] = 0
                        
                    del finalSet[index]

                    del ops[index]
                    length -=1
                else:
                    index += 1

                
            ip_index += 1
        #print(finalSet[finalSet.__len__()-1])
        return finalSet[finalSet.__len__()-1]
    
    def solve(self, dataRow) -> {}:
        items = self.prepare(dataRow)
        result = self.__try0(items)
        return result

def getColumn(c):
    table = {}
    table["ID"] = {"type": "int", "default": 0}
    table["Name"] = {"type": "string", "default": "student"}
    table["Birthdate"] = {"type": "string", "default": "Null"}
    table["From"] = {"type": "string", "default": "Libya"}
    table["Age"] = {"type": "int", "default": 0}

    if c in table:
        return table[c]
    return None
def getVariable(v):
    table = {}
    table["MAX_COLUMN_NUMBER"] = {"type": "int", "value": 15}
    table["PI"] = {"type": "float", "value": 3.14159}
    table["myName"] = {"type": "string", "value": "MD"}
    table["myAge"] = {"type": "int", "value": 24}

    if v in table:
        return table[v]
    return None
def parse_operand(part: str) -> Operand:
    if part == None or len(part) == 0:
        return None
    op: Operand = Operand()
    
    index = 0
    length = len(part)
    
    numbersCollected = 0
    while index < length:
        c = part[index]

        if c == ' ': pass
        elif c == '(':
            buff = ''
            j = index+1
            innerBracets = 0
            while j < length:
                if part[j] == '(':
                    innerBracets += 1
                elif part[j] == ')':
                    innerBracets -= 1
                
                if innerBracets <= -1:
                    break
                    
                buff += part[j]
                j += 1
            
            #if lastOperand == '&&':
            innerOP = parse_operand(buff)
            #innerOP_Value = innerOP.solve()
            op.addInlineOperand(innerOP)
            #op.addElement(innerOP_Value["value"], innerOP_Value["type"])
            index = j
        elif c.isdigit():
            buff = c
            j = index + 1
            is_real = False
            while j < length:
                if part[j] == '.':
                    is_real  =True
                if not part[j].isdigit() and part[j] != '.':
                    j -= 1
                    break
                else:
                    buff += part[j]

                j += 1
            
            if is_real:
                op.addElement(float(buff), "float")
            else:
                op.addElement(int(buff), "int")
                
            index = j     
        elif c == "'":
            buff = ''
            j = index+1
            innerBracets = 0
            while j < length:
                ic = part[j]
                if part[j] == "'" and j-1 >= 0 and part[j-1] != '\\':
                    break
                
                buff += ic
                j += 1

            op.addElement(buff, 'string')
            index = j
        elif c.isalpha():
            collectedType = "column"
            if index -1 > -1:
                if part[index-1] == '@':
                    collectedType = "var"

            buff = c
            j = index + 1
            while j < length:
                if not part[j].isalpha() and not part[j] == '_':
                    j -= 1
                    break
                else:
                    buff += part[j]

                j += 1
            
            if buff == 'True' or buff == 'False':
                op.addElement(1 if buff == 'True' else 0, 'int')
            elif buff == 'Null':
                op.addElement(0, 'int')
            else:
                op.addElement(buff, collectedType)
                op.setContainsDynamicElements(True)
            index = j
        elif c == '+':
            op.addOperator(c)
        elif c == '-':
            op.addOperator(c)
        elif c == '*':
            op.addOperator(c)
        elif c == '/':
            op.addOperator(c)
        elif c == '^':
            op.addOperator(c)
        index += 1

    return op
def parse_condition(sample: str) -> list[ConditionClaus()]:
    resultCollection = []

    collectingIndex = 0
    index = 0
    length = len(sample)

    collection = []
    collection.append(ConditionClaus())
    collection[0].condition = Condition()
    currentClaus = collection[0]
    bracets_switch = True
    while index < length:
        c = sample[index]

        if c == ' ':
            index += 1
            continue
        elif bracets_switch and c == '(':
            buff = ''
            foundLogicalOperator = False
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
            
            if buff.__contains__('&&') or buff.__contains__('||') or buff.__contains__('==') or buff.__contains__('!=') or buff.__contains__('~=') or buff.__contains__('>') or buff.__contains__('<') or buff.__contains__('>=') or buff.__contains__('<='):
                foundLogicalOperator = True

            if foundLogicalOperator:
                currentClaus.setAsLink(parse_condition(buff))
                index = j
                collectingIndex = index+1
            else:
                bracets_switch = False
                continue
            
        elif c == '&' and index+1 < length and sample[index+1] == '&':
            bracets_switch = True
            currentClaus.condition.addValue(parse_operand(sample[collectingIndex:index]))
            collectingIndex = index + 2
            currentClaus.addRequired(ConditionClaus())
            currentClaus = currentClaus.next # points to the next condition
            
            currentClaus.setCondition(Condition())
            print("Linked Section to previous claus created")
            index += 1
        elif c == '|' and index+1 < length and sample[index+1] == '|':
            bracets_switch = True
            print("Values sliced >> "+sample[collectingIndex:index])
            currentClaus.condition.addValue(parse_operand(sample[collectingIndex:index]))
            collectingIndex = index + 2
            # new section
            collection.append(ConditionClaus())
            currentClaus = collection[len(collection)-1]
            currentClaus.setCondition(Condition())
            print("New Section created")
            index += 1
        elif c == '!' and index+1 < length and sample[index+1] == '=':
            currentClaus.condition.addFunction(ne)
            currentClaus.condition.addValue(parse_operand(sample[collectingIndex:index]))
            collectingIndex = index + 2
            index += 1
        elif c == '=' and index+1 < length and sample[index+1] == '=':
            currentClaus.condition.addFunction(eq)
            currentClaus.condition.addValue(parse_operand(sample[collectingIndex:index]))
            collectingIndex = index + 2
            index += 1
        elif c == '~' and index+1 < length and sample[index+1] == '=':
            currentClaus.condition.addFunction(li)
            currentClaus.condition.addValue(parse_operand(sample[collectingIndex:index]))
            collectingIndex = index + 2
            index += 1
        elif c == '<' and index+1 < length and sample[index+1] == '=':
            currentClaus.condition.addFunction(le)
            currentClaus.condition.addValue(parse_operand(sample[collectingIndex:index]))
            collectingIndex = index + 2
            index += 1
        elif c == '<':
            currentClaus.condition.addFunction(lt)
            currentClaus.condition.addValue(parse_operand(sample[collectingIndex:index]))
            collectingIndex = index + 1
        elif c == '>' and index+1 < length and sample[index+1] == '=':
            currentClaus.condition.addFunction(ge)
            currentClaus.condition.addValue(parse_operand(sample[collectingIndex:index]))
            collectingIndex = index + 2
            index += 1
        elif c == '>':
            currentClaus.condition.addFunction(gt)
            currentClaus.condition.addValue(parse_operand(sample[collectingIndex:index]))
            collectingIndex = index + 1
        else:
            pass
        index += 1

    if collectingIndex < length:
        #print("Values sliced >> "+sample[collectingIndex:index])
        currentClaus.condition.addValue(parse_operand(sample[collectingIndex:index]))
        collectingIndex = index + 2

    return collection
def evaluate_condition(collection:list[ConditionClaus()], data:{} = None):
    resultCollection = []
    for c in collection:
        result = True
        if c.isLinkClaus(): 
            # islinkclaus ||
            ls = evaluate_condition(c.innerRelatedConditions, data)
            #print("Sub condition :"+repr(ls))
            result = ls
        else:
            cond = c.condition
            if cond == None: # in case 1==1 && (0 > 9) the new ConditionClaus.condition would be none
                raise Exception("ConditionClaus.condtion is None")

            leftOperand = cond.lvalue.solve(data)
            rightOperand = cond.rvalue.solve(data)
            result = cond.function(leftOperand['value'], rightOperand['value'])

        # islinkclaus &&
        ic = c.next
        while ic != None:
            cond = ic.condition
            if ic.isLinkClaus():
                ls = evaluate_condition(ic.innerRelatedConditions, data)
                #print("Sub condition :"+repr(ls))
                if ls == False:
                    result = False
                    break
            if cond == None: 
                break
            #print(str(cond.lvalue) + "/" + str(cond.rvalue))
            if cond.lvalue == None or cond.rvalue == None:
                pass
            else:
                leftOperand = cond.lvalue.solve(data)
                rightOperand = cond.rvalue.solve(data)
                result = cond.function(leftOperand['value'], rightOperand['value'])
                if result == False:
                    break

            ic = ic.next
        
        resultCollection.append(result)

        #print(resultCollection) 
    return True in resultCollection

dataRow = []
dataRow.append({
    "ID" : 19,
    "Name": "Mohammad s. Albay",
    "Age": 24,
    "Birthdate": "24-4-1999",
    "From": "Souq-aljomaa"
})
dataRow.append({
    "ID": 20,
    "Name": "Hesham Albay",
    "Age": 47,
    "Birthdate": "2-5-1981"
    # When you forgot to insert column value, the system falls back to use 'default' value
})
dataRow.append({
    "ID": 20,
    "Name": "Moad wafee",
    "Age": 25,
    "Birthdate": "9-10-1998",
    "From": "Gharyan"
})
dataRow.append({
    "ID": 17,
    "Name": "Salma Tresh",
    "Age": 52,
    "Birthdate": "24-4-1976",
    "From": "Tajoura"
})
dataRow.append({
    "ID": 12,
    "Name": "Reema Tresh",
    "Age": 45,
    "Birthdate": "15-2-1988",
    "From": "Tajoura"
})

print("Process: Building condition...")
c = parse_condition("From == 'Souq-aljomaa' || Name ~= 'Albay'")
if c == None or c.__len__() == 0:
    print("Process: Error, faield to build condition")
else:
    print("Process: Data selection phase...")
    for data in dataRow:
        if evaluate_condition(c,data):
            print ("Passed : "+ repr(data))
        else:
            print ("Not passed : "+ repr(data))
