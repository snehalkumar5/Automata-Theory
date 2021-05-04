
## Converting NFA to DFA:

When converting from NFA to DFA recognising the same language, the alphabets remain the same while the set of states and transition changes.

**Set of states:**

The number of states = 2^no of states of NFA:

```python
for i in range(dfa_num):
        subset = []
        for j in range(num_states):  
            ck = i & 1<<j          
            if ck:
                subset.append(stts[j])
         dfa_states.append(subset)
```

**Transition function:**

To make the new transition function for the equivalent DFA, we iterate through the alphabet and find the corresponding transition function in the NFA and add them to the DFA transition function if not present:

```python
for letter in LETTERS:
            dfa_transitions[(tuple(in_state), letter)] = set()
            for in_s in in_state:
                if (in_s, letter) in tuple(NFA_TRANS.keys()):
                    for next_s in NFA_TRANS[(in_s, letter)]:
                        dfa_transitions[(tuple(in_state), letter)].add(next_s)
    for key, value in dfa_transitions.items():
        temp_list = [ list(key[0]), key[1], list(value) ] 
        dfa_transition_function.append(list(temp_list))
```

**Final states:**

This will be the set of all states containing the final states

```python
for f_state in FINAL:
        for state in dfa_states:
            if f_state in state:
                dfa_final_states.append(state)
```
