
## Minimizing the DFA:

**Myhill Nerode Theorem** provides a necessary and sufficient condition for a language to be regular. It can also be used to find the minimal number of states in a DFA for a regular language.

To use the theorem, use the concept of graph traversal and DSU (for combining):

- First we traverse all the states by performing a BFS and only keep the reachable states in a variable

```python
while len(queue) > 0:
        curr = queue.pop(0)
        for ch in LETTERS:
            if ((curr, ch) in trans) and (trans[(curr, ch)] not in reaching_states):
                queue.append(trans[(curr, ch)])
                reaching_states.append(trans[(curr, ch)])
```

- Then we go to every pair of states (Qi,Qj)  given in the DFA and select the ones for which Qi belongs to the set of final states and Qj does not belong to the final states.
- For the remaining pairs, we go to each pair and select the pairs in which the pair of transition function from both states (($\delta$(Qi,A), $\delta$(Qj,A))  is selected for some alphabet A in the alphabet set.
- Now, we have the remaining pairs which have not been selected and these pairs are combined into a single state in the minimized DFA.
- Finally the start states, transition function and final states are updated:

```python
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
    FINAL = final_statesfor (curr, ch), nxt in trans.items():
        if curr not in STATES:
            continue
        if nxt not in STATES:
            continue
        
        flag = False

		#update transition
        for curr1, ch1, nxt1 in T_FN:
            srt_c = sorted(curr1)
            srt_dss = sorted(dsu.find(curr))
            if srt_c == srt_dss:
                if ch1 == ch:
                    flag = True
        if flag:
            continue
        T_FN.append([dsu.find(curr),ch,dsu.find(nxt)])
```