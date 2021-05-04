## Converting Regex to NFA:

To convert regex to nfa, we need to check the elements in the expressions and convert it to NFA form. To achieve this, we use a stack implementation to get the elements and make the NFA.

Convert the expression to post-fix form (for stack) after adding the concatenation operator between elements at the appropriate places. 

```python
def infix_to_posfix_re(self, exp):
        for c in exp:
            if c.isalnum() or c == OPS['E']:
                postfix_exp.append(c)
            elif c == ')':
                while stack[-1] != '(':
                    postfix_exp.append(val)
                    stack.pop()
            elif c == '(':
                stack.append(c)
            else:
                while len(stack)0:
                    if(stack[-1] == '(' or (ck_precede(stack[-1]) < ck_precede(c))):
                        break
                    postfix_exp.append(stack[-1])
                    stack.pop()                
                stack.append(c)
```

Using the stack created, we take the elements of the expression and create the stack of NFA. 

- Make the NFA that accepts a single character and mark one of the states as the initial state and the other as the final state.
- When the element is '*' :  Take the NFA that accepts regex, create another NFA' that accepts the regex1* of the NFA and create a start state:
    - Start state of NFA' makes an $\epsilon$ -transition to the start state of the NFA.
    - The final state of NFA1 makes an $\epsilon$-transition to the start state of NFA'.
- When the element is '.' : Take a pair of NFAs that accept regex1 and regex2 respectively, create another NFA' that accepts the regex1$\cdot$regex2. Add an $\epsilon$-transition from the final state of NFA1 to start of NFA2 which essentially combines the NFAs. Make the start of NFA' as the start of NFA1 and final state of NFA' as the final state of NFA2
- When the element is '+' :  Take a pair of NFAs that accept regex1 and regex2, create another NFA' that accepts the regex1+regex2 of the NFAs and create a start state and final state from which, it makes an $\epsilon$ -transition to the start states of both NFAs and makes an $\epsilon$-transition from both final states to the new final state

```python
for a in regg.exp:
        if a.isalnum() == False and a!=OPS['E']:
            if a == OPS['STAR']:
                nfa = stack.pop()
                stack.push(star_app(nfa))
            elif a == OPS['CONCAT']:
                nfa2 = stack.pop()
                nfa1 = stack.pop()
                stack.push(concat_app(nfa1, nfa2))
            elif a == OPS['UNION']:
                nfa2 = stack.pop()
								nfa1 = stack.pop()
                stack.push(union_app(nfa1, nfa2))
        else:
            trans = [(0, a, 1)]
            res = NFA(2, letters, trans, [0], [1])
            stack.push(res)
```

