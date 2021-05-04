import json
import copy
import sys
OPS={
    'PHI':'ϕ',
    'STAR':'*',
    'UNION':'+',
    'DOLLAR':'$'
}
def get_preds(state, trans):
    res = []
    for key, val in trans.items():
        if key != state:
            if state in val and val[state] != OPS['PHI']:
                res.append(key)
        else:
            continue
    return res

def get_sucs(state, trans):
    res = []
    for key, val in trans[state].items():
        if val != OPS['PHI'] and key != state:
            res.append(key)
    return res

def bracket(x, y, tran):
    st = ''
    if tran == OPS['PHI']:
        return st
    else:
        st = '('+str(tran)+')'
        return str(st)
    
def reduce_trans(i, rip, j, trans):
    r1 = bracket(i, rip, trans[i][rip])
    r2 = bracket(rip, rip, trans[rip][rip])
    r3 = bracket(rip, j, trans[rip][j])
    r4 = bracket(i, j, trans[i][j])
    if r2 != '':
        if r4 != '':
            res = (r1 + r2 + OPS['STAR'] + r3 + OPS['UNION'] + r4)
        else:
            res = (r1 + r2 + OPS['STAR'] + r3)            
    else:
        if r4 != '':
            res = (r1 + r3 + OPS['UNION'] + r4)
        else:
            res = (r1 + r3)            
    return res
    

if __name__ == "__main__":
     
    args = len(sys.argv)
    if args != 3:
        print('Invalid number of arguments!')
        quit()

    with open(str(sys.argv[1]), 'r') as f:
        data = json.load(f)

    # dfa = DFA(data)

    STATES = data['states']
    LETTERS = data['letters']
    T_FN = data['transition_function']
    START = data['start_states']
    FINAL = data['final_states']
    move = {}


    trans = {}
    # initliaze with phi
    for i in STATES:
        trans[i] = {}
        for j in STATES:
            trans[i][j] = OPS['PHI']
    # add re to edge 
    for _from, ch, to in T_FN:
        if trans[_from][to] == OPS['PHI']:
            trans[_from][to] = ch
        else:
            trans[_from][to] += f'+{ch}'
    
    gnfa_start = 'Q#' + str(len(STATES)) 
    gnfa_final = 'Q#' + str(len(STATES) + 1)
    trans[gnfa_start] = {}
    trans[gnfa_final] = {}
    trans[gnfa_start][gnfa_final] = OPS['PHI']
    for state in STATES:
        if state in START:
            trans[gnfa_start][state] = OPS['DOLLAR']
        else:
            trans[gnfa_start][state] = OPS['PHI']

        if state in FINAL:
            trans[state][gnfa_final] = OPS['DOLLAR']
        else:
            trans[state][gnfa_final] = OPS['PHI']


    interstate = STATES
    for rip in interstate:
        new_trans = {}
        preds = get_preds(rip, trans)
        sucs = get_sucs(rip, trans)
        tmp_trans = copy.deepcopy(trans)
        for i in preds:
            for j in sucs:
                tmp_trans[i][j] = reduce_trans(i, rip, j, trans)
        
        # remove rip from trans
        for i, nxt in tmp_trans.items():
            if i != rip:
                new_trans[i] = {}
                for j, exp in nxt.items():
                    if j != rip:
                        new_trans[i][j] = exp
                    else:
                        continue
            else:
                continue
        trans = copy.deepcopy(new_trans)    
    REGEX = trans[gnfa_start][gnfa_final]

    REGEX = {
        'regex':REGEX
    }
    with open(str(sys.argv[2]), 'w') as f:
        json.dump(REGEX, f, indent=4)
   