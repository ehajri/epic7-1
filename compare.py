# from output import output
# from verification import inventory

def printable(list):
    result = []
    for i in list:
        result.append(i['key'] + ': ('+ ', '.join(str(v) for v in i['values']) +')')
    return ', '.join(result)


def compare(img_id, inv, op):
    result = []
    for k in inv.keys():
        if k != 'subs':
            if inv[k] != op[k]:
                result.append({'key': k, 'values': [inv[k], op[k]]})
        else:
            for index in range(len(inv[k])):
                if inv[k][index] != op[k][index]:
                    result.append({'key': k, 'values': [inv[k][index], op[k][index]]})
    if result:
        print('['+str(img_id)+']', printable(result))
    # else:
    #     print(img_id, "is a match")

# for i in range(len(inventory)):
#     op = output[i]
#     inv = inventory[i]
#     compare(i, inv, op)