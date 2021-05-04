
## Converting DFA to Regex:

To convert to regex, we use the concept of Generalised Nondeterministic Finite Automaton(GNFA). First, we convert the given DFA to the GNFA, then we reduce the states of the GNFA to get the regex.

In a GNFA, there a single accept state from which it has arrows to all other states but not incoming from them. Also from each state (excluding the start and accept), there is arrow to other states and itself which includes $\phi$ is no transition present.

After forming the GNFA, we reduce the states by removing them. Through the removal process, we combine the states and create the regex by altering the arrows that transitions between the states. Finally we get our regex when we remove all the states excluding the start and finish state.

```python
for rip in interstate:
        new_trans = {}
        preds = get_preds(rip, trans)
        sucs = get_sucs(rip, trans)
        for i in preds:
            for j in sucs:
                tmp_trans[i][j] = reduce_trans(i, rip, j, trans)
        
        # remove state
        for i, nxt in tmp_trans.items():
            if i != rip:
                new_trans[i] = {}
                for j, exp in nxt.items():
                    if j != rip:
                        new_trans[i][j] = exp
             else:
                continue
REGEX = trans[gnfa_start][gnfa_final]
```