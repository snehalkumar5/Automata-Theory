import json 
import sys

preceding = {
  '*': 4,
  '.': 3,
  '+': 2
}
OPS={
    'E':'$',
    'STAR':'*',
    'CONCAT':'.',
    'UNION':'+',
}
letters = None
def ck_precede(a):
    return preceding[a] if a in preceding else 1

def get_str(state):
    return 'Q' + str(state)
 

class NFA: 
    def __init__(self, states, chars, t_func, start_states, final_states):
        self.states = states if states != None else None
        self.letters = chars if chars != None else None
        self.t_func = t_func if t_func != None else None
        self.start_states = start_states if start_states != None else None
        self.final_states = final_states if final_states != None else None
   
def star_app(nfa):
    new_state = nfa.states
    nfa.states += 1
    for _, start_state in enumerate(nfa.start_states):
        nfa.t_func.append((new_state, OPS['E'], start_state))
    
    for _, finish_state in enumerate(nfa.final_states):
        nfa.t_func.append((finish_state, OPS['E'], new_state))

    nfa.start_states, nfa.final_states = [new_state],[new_state]
    return nfa 

def union_app(nfa1, nfa2):
    delta = nfa1.states
    nfa = NFA(None,None,None,None,None)  
    nfa.states = delta + nfa2.states + 1
    nfa.start_states = [nfa.states - 1]
    nfa.letters = letters
    for i, val in enumerate(nfa2.final_states):
        nfa2.final_states[i] = delta + val
    nfa.final_states = nfa1.final_states + nfa2.final_states

    for i, val in enumerate(nfa2.start_states):
        nfa2.start_states[i] = delta + val

    for i, val in enumerate(nfa2.t_func):
        nfa2.t_func[i] = (delta + val[0], val[1], delta + val[2])
    nfa.t_func = nfa1.t_func + nfa2.t_func
    
    for _, start_state in enumerate(nfa1.start_states):
        nfa.t_func.append((nfa.start_states[0], OPS['E'], start_state))
    for _, start_state in enumerate(nfa2.start_states):
        nfa.t_func.append((nfa.start_states[0], OPS['E'], start_state))        
    return nfa
    
def concat_app(nfa1, nfa2):
    delta = nfa1.states
    nfa = NFA(None,None,None,None,None)  
    nfa.states = delta + nfa2.states
    nfa.letters = letters

    for i, val in enumerate(nfa2.final_states):
        nfa2.final_states[i] = delta + val
    nfa.final_states = nfa2.final_states

    for i, val in enumerate(nfa2.start_states):
        nfa2.start_states[i] = delta + val
    nfa.start_states = nfa1.start_states

    for i, val in enumerate(nfa2.t_func):
        nfa2.t_func[i] = (delta + val[0], val[1], delta + val[2])
    nfa.t_func = nfa1.t_func + nfa2.t_func
        
    for _, state1 in enumerate(nfa1.final_states):
        for _, state2 in enumerate(nfa2.start_states):
            nfa.t_func.append((state1, OPS['E'], state2))
    return nfa
    
    
class RegEx:
    '''
    Regex module
    '''
    def __init__(self, regex):
        self.exp = str(regex)
    
    def ck_concat(self, c1, c2):
        ck = [')',OPS['STAR'],OPS['E']]
        ck1 = ['(',OPS['E']]
        if ((c1.isalnum() == True) or c1 in ck):
            if ((c2.isalnum() == True) or c2 in ck1):
                return True
        return False

    def add_concat(self, exp):
        new_exp = ''
        lng = len(exp)
        for i in range(lng):
            if i == lng-1:
                new_exp += (exp[i])
                break
            ck = self.ck_concat(exp[i],exp[i+1])
            if ck == True:
                new_exp += (exp[i] + OPS['CONCAT'])
            else:
                new_exp += (exp[i])
        return new_exp
    
    def infix_to_posfix_re(self, exp):
        stack = []
        # print(exp)
        postfix_exp = []
        for c in exp:
            if c.isalnum() or c == OPS['E']:
                postfix_exp.append(c)
            elif c == ')':
                while stack[-1] != '(':
                    val = stack[-1]
                    # print('into stack',val)
                    postfix_exp.append(val)
                    stack.pop()
                stack.pop() 
            elif c == '(':
                stack.append(c)
            else:
                length = len(stack)
                while length>0:
                    if(stack[-1] == '(' or (ck_precede(stack[-1]) < ck_precede(c))):
                        break
                    postfix_exp.append(stack[-1])
                    stack.pop()
                    length-=1
                stack.append(c)
        length = len(stack)
        while length>0:
            val = stack[-1]
            # print(val)
            postfix_exp.append(val)
            stack.pop()
            length-=1

        return ''.join(postfix_exp)

def convert_to_NFA(regg: RegEx):
    global letters
    expression = regg.exp
    letters = set()
    for a in expression:
        if a.isalnum() == False and a!= OPS['E']:
            continue
        letters.add(a)
    
    regg.exp = regg.add_concat(regg.exp)
    # print('After adding concats: ', regg.exp) 
    
    regg.exp = regg.infix_to_posfix_re(regg.exp)
    # print('Post fix expression:', regg.exp)

    # a stack of NFAs
    stack = []
    letters = list(letters)
    for a in regg.exp:
        if a.isalnum() == False and a!=OPS['E']:
            if a == OPS['STAR']:
                nfa = stack[-1]
                stack.pop()
                stack.append(star_app(nfa))
            elif a == OPS['CONCAT']:
                nfa2,nfa1 = stack[-1],stack[-2]
                stack.pop()
                stack.pop()
                stack.append(concat_app(nfa1, nfa2))
            elif a == OPS['UNION']:
                nfa2,nfa1 = stack[-1],stack[-2]
                stack.pop()
                stack.pop()
                stack.append(union_app(nfa1, nfa2))
        else:
            trans = [(0, a, 1)]
            res = NFA(2, letters, trans, [0], [1])
            stack.append(res)
    
    return stack[0]


if __name__ == "__main__":

    args = len(sys.argv)
    if args != 3:
        print('Invalid number of arguments!')
        quit()

    with open(str(sys.argv[1]), 'r') as f:
        data = json.load(f)
        # print('Regular expression:',data["regex"])

    re = RegEx(data["regex"])
    nfa = convert_to_NFA(re)
    st = []
    lt = []
    tt = []
    ss = []
    fs = []
    for state in range(nfa.states):
        st.append('Q'+str(state))
    for i,l in enumerate(nfa.letters):
        lt.append(l)
    for trans in nfa.t_func:
        tt.append(('Q'+str(trans[0]),trans[1],'Q'+str(trans[2])))
    for state in nfa.start_states:
        ss.append('Q'+str(state))
    for state in nfa.final_states:
        fs.append(get_str(state))
        
    nfa = {
            'states': st,
            'letters': lt,
            'transition_function': tt,
            'start_states': ss,
            'final_states': fs
        }
    with open(str(sys.argv[2]), 'w') as f:
        json.dump(nfa, f, indent=4)
