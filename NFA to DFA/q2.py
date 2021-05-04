import json
import copy
import sys

if __name__ == '__main__':

    args = len(sys.argv)
    if args != 3:
        print('Invalid number of arguments!')
        quit()

    with open(str(sys.argv[1]), 'r') as f:
        data = json.load(f)
    NUM_STATES = len(data['states'])
    STATES = data['states']
    LETTERS = data['letters']
    TRANS_FN = data['transition_function']
    START = data['start_states']
    FINAL = data['final_states']
    NFA_TRANS = {}
    for (st1,sym,st2) in TRANS_FN:
        # ch = (st1,sym)
        if (st1,sym) not in tuple(NFA_TRANS.keys()):
            NFA_TRANS[(st1,sym)] = set()
        NFA_TRANS[(st1,sym)].add((st2))

    dfa_num = 2**(NUM_STATES)
    dfa_start =  [[state] for state in START]

    stts = list(STATES)
    newts = []
    input_num = len(stts)
    for i in range(dfa_num):
        subset = []
        for j in range(input_num):  
            ck = i & 1<<j          
            if ck:
                subset.append(stts[j])
            else:
                continue
        newts.append(subset)        
    
    dfa_states = copy.deepcopy(newts)


    dfa_transition_function = []
    dfa_final_states = []
    dfa_transitions={}
    
    for in_state in dfa_states:
        
        for letter in LETTERS:
            dfa_transitions[(tuple(in_state), letter)] = set()
            for in_s in in_state:
                if (in_s, letter) in tuple(NFA_TRANS.keys()):
                    for next_s in NFA_TRANS[(in_s, letter)]:
                        dfa_transitions[(tuple(in_state), letter)].add(next_s)
    for key, value in dfa_transitions.items():
        temp_list = [ list(key[0]), key[1], list(value) ] 
        dfa_transition_function.append(list(temp_list))

    for f_state in FINAL:
        for state in dfa_states:
            if f_state in state:
                dfa_final_states.append(state)
    dfa = {
        'states': dfa_states,
        'letters': LETTERS,
        'transition_function': dfa_transition_function,
        'start_states': dfa_start,
        'final_states': dfa_final_states
    }
    with open(str(sys.argv[2]), 'w') as f:
        json.dump(dfa, f, indent=2)