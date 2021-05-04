import json
import sys
import copy
import itertools

class DSU:
    def __init__(self, nodes):
        self.nodes = set(nodes)
        self.num = len(nodes)
        self.disjoint_set = [[node] for node in self.nodes]

    def get_ind(self, node):
        for s in self.disjoint_set:
            for val in s:
                if val != node:
                    continue
                else:
                    return self.disjoint_set.index(s)
        return None

    def find(self, item):
        res = None
        for s in self.disjoint_set:
            if item in s:
                res = s
                break
        return res

    def join(self, a, b):
        i = self.get_ind(a)
        j = self.get_ind(b)

        if i == j:
            return
        else:
            self.disjoint_set[i] += self.disjoint_set[j]
            del self.disjoint_set[j]


if __name__ == "__main__":

    args = len(sys.argv)
    if args != 3:
        print('Invalid number of arguments!')
        quit()

    with open(str(sys.argv[1]), 'r') as f:
        data = json.load(f)


    STATES = data['states']
    LETTERS = data['letters']
    T_FN = data['transition_function']
    START = data['start_states']
    FINAL = data['final_states']
    trans = {}

    for tran in T_FN:
        _from, letter, to = tran
        trans[(_from, letter)] = to

    reaching_states = copy.deepcopy(START)
    queue = copy.deepcopy(START)
    while len(queue) > 0:
        curr = queue.pop(0)
        for ch in LETTERS:
            if ((curr, ch) in trans) and (trans[(curr, ch)] not in reaching_states):
                queue.append(trans[(curr, ch)])
                reaching_states.append(trans[(curr, ch)])

    STATES = reaching_states
    FINAL = [ s for s in FINAL if s in reaching_states]

    checked_pairs = []
    for state in itertools.combinations(STATES, 2):
        if (state[0] in FINAL) and (state[1] not in FINAL):
            checked_pairs.append(copy.deepcopy(state))
        elif (state[0] not in FINAL) and (state[1] in FINAL):
            checked_pairs.append(copy.deepcopy(state))

    while True:
        flag = True
        for state in itertools.combinations(STATES, 2):
            if state not in checked_pairs:
                for ch in LETTERS:
                    if flag == False:
                        break
                    n0, n1 = trans[(state[0], ch)], trans[(state[1], ch)]
                    for tup in checked_pairs:
                        if tup == (n0,n1) or tup == (n1,n0):
                            checked_pairs.append(state)
                            flag = False
                            break
            else:
                continue
        if flag == True:
            break

    # remaining pairs
    stt = copy.deepcopy(STATES)
    dsu = DSU(stt)
    for state in itertools.combinations(STATES, 2):
        if state in checked_pairs:
            continue
        else:
            dsu.join(*state)

    # update start
    start_states = []
    ress = dsu.disjoint_set
    for new_state in ress:
        for state in new_state:
            if state not in START:
                continue
            else:
                start_states.append(new_state)
                break
    START = start_states

    # update final
    final_states = []
    for new_state in dsu.disjoint_set:
        for state in new_state:
            if state not in FINAL:
                continue
            else:
                final_states.append(new_state)
                break
    FINAL = final_states
    
    # update transition
    T_FN = []
    for (curr, ch), nxt in trans.items():
        if curr not in STATES:
            continue
        if nxt not in STATES:
            continue
        
        flag = False
        for curr1, ch1, nxt1 in T_FN:
            srt_c = sorted(curr1)
            srt_dss = sorted(dsu.find(curr))
            if srt_c == srt_dss:
                if ch1 == ch:
                    flag = True
        if flag:
            continue
        T_FN.append([dsu.find(curr),ch,dsu.find(nxt)])

    STATES = dsu.disjoint_set
    dfa = {
        'states': STATES,
        'letters': LETTERS,
        'transition_function': T_FN,
        'start_states': START,
        'final_states': FINAL
    }

    with open(str(sys.argv[2]), 'w') as f:
        json.dump(dfa, f, indent=4)
