
raw
Readme · MD
# Multiparameter Persistence Expressivity
 
A short exploration into the expressivity of multiparameter persistence, inspired by [*On the Expressivity of Persistent Homology in Graph Learning*](https://arxiv.org/abs/2302.09826) by Ballester and Rieck.
 
> **Note:** This is still a work in progress and as such slightly awkward to run.
 
---
 
## Usage
 
**Rips + Degree bifiltration:**
```bash
python -m tests.execute_tests
```
 
**Laplacian + Forman–Ricci bifiltration:**
 
Delete the arguments in `execute_tests.py` and run as above.
 
**Hardware limitations:**
 
If resources are constrained, limit `max_dim` to `2` or even `1` when computing a Rips filtration.
 
---
 
## Repository Structure
 
The `external/` folder contains two non-original GitHub repositories, both referenced below.
 
---
 
## TODO
 
- [ ] Add filters
- [ ] Make script executable
- [ ] Simplify and/or rethink how arguments are passed
---
 
## References
 
- Ballester, R. and Rieck, B. *On the Expressivity of Persistent Homology in Graph Learning*. arXiv:2302.09826 (2023). https://arxiv.org/abs/2302.09826
- PH_Expressivity GitHub: https://github.com/aidos-lab/PH_expressivity/blob/main/src/ph/filtrations.py
- BREC GitHub: https://github.com/GraphPKU/BREC
 
