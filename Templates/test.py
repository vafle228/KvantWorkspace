def action(a, b, action_):
    return {'+': a + b, '-': a - b, '*': a * b, '/': a // b}[action_]



def arr_action(arr, action_):
    res = int(arr[0])
    for i in arr[1:]:
        res = action(int(res), int(i), action_)
    return res



def exp_solver(exp):
    return arr_action(list(map(lambda sub_exp: arr_action(list(map(
        lambda sub_exp: arr_action(list(map(lambda sub_exp: arr_action(sub_exp.split('/'), '/'), sub_exp.split('*'))),
                                   '*'), sub_exp.split('-'))), '-'), exp.split('+'))), '+')



def bracket_shredder(exp):
    if '(' in exp:
        return bracket_shredder(
            exp[:exp.rfind('(')] + str(exp_solver(exp[exp.rfind('(') + 1:exp.find(')')])) + exp[exp.find(')') + 1:])
    return exp_solver(exp)



# Это чтобы вам не набирать выражение)
print(bracket_shredder('2*(3+(7*10+4))/7'))
# А это если вы хотите ввести свое выражение
print(bracket_shredder(input()))