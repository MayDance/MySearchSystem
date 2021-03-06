import nltk
import collections
from Searching import operateDocList as listSort
from Searching import searchWord as search


def infix_to_postfix(input_list):
    stack = []

    def bool_op_value(op):
        precedence = ['OR', 'AND', 'NOT']
        for i in range(3):
            if op == precedence[i]:
                return i
        return -1

    def op_order(op1, op2):
        if op1 == '(' or op2 == '(':
            return False
        elif op2 == ')':
            return True
        else:
            if bool_op_value(op1) < bool_op_value(op2):
                return False
            else:
                return True

    postfix = [];
    temp = [];
    for s in input_list:
        if s != 'AND' and s != 'OR' and s != 'NOT':
            temp.append(s)
        else:
            if temp:
                postfix.append(temp)
                temp = []
            while len(stack) != 0 and op_order(stack[-1], s):
                op = stack.pop()
                postfix.append(op)
            if len(stack) == 0 or s != ')':
                stack.append(s)
            else:
                top_op = stack.pop()
    if temp:
        postfix.append(temp)
    if len(stack):
        postfix += stack[::-1]
    return list_to_phrase(postfix)


def list_to_phrase(list):
    list2 = []
    for element in list:
        if len(element) > 1:
            if element == 'AND' or element == 'OR' or element == 'NOT':
                list2.append([element])
                continue
            str = ""
            for word in element:
                str = str + ' ' + word
            list2.append([str[1:]])
        else:
            list2.append(element)
    return list2


def phrase_to_list(list):
    list2 = []
    for element in list:
        word=element[0]
        if word == 'AND' or word == 'OR' or word == 'NOT':
            list2.append(word)
            continue
        if word.find(' ') != -1:
            l = word.split(" ")
            list2.append(l)
        else:
            list2.append(element)
    return list2


def bool_search(postfix, index):
    postfix = phrase_to_list(postfix)
    result = []
    limit = len(postfix)
    i = 0
    while i < limit:
        item = postfix[i]
        if item != 'AND' and item != 'OR':
            if i < limit - 1:
                if postfix[i + 1] == "NOT":
                    i = i + 1
                    result.append(search.search_bool_phrase(index, item, flag=False))
                else:
                    result.append(search.search_bool_phrase(index, item, flag=True))
            else:
                result.append(search.search_bool_phrase(index, item, flag=True))
        elif item == 'AND':
            if len(result) < 2:
                print("illegal query")
                return []
            else:
                list1 = result.pop()
                list2 = result.pop()
                result.append(listSort.and_list(list1, list2))
        elif item == 'OR':
            if len(result) < 2:
                print("illegal query")
                return []
            else:
                list1 = result.pop()
                list2 = result.pop()
                result.append(listSort.merge_list(list1, list2))
        i += 1
    if len(result) != 1:
        print("illegal query")
        return []
    else:
        return result.pop()
