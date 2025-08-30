# Jugs Game Search — BFS vs IDS

This project solves instances of the classic **water jugs** problem using two uninformed search algorithms:
- **BFS (Breadth‑First Search)**
- **IDS (Iterative Deepening Depth‑First Search)**

It also reports basic metrics so you can compare the algorithms on the same instance.

---

## Quick PEAS (Problem Formulation)

- **Performance (P):** Minimize number of actions to reach the target water distribution (shortest path).
- **Environment (E):** Finite, fully observable vector of jug fill levels with fixed capacities.
- **Actuators (A):** Pour from jug *i* → jug *j* until the source is empty or the destination is full.
- **Sensors (S):** Exact amounts of water in each jug.

**Model components**
- **Initial state:** vector of current amounts (e.g., `[8,0,0]`).
- **Actions:** all ordered pairs `(i, j)` with `i != j` (pour i→j).
- **Transition model:** applies the pour; respects capacity and emptiness.
- **Goal test:** `state == goal` vector.
- **Path cost:** unit cost per action (path length).

---

## Files

- `search_core.py` — main program (BFS + IDS + metrics).
- `README.md` — this file.

No external libraries are required (standard library only).

---

## Requirements

- Python 3.9+ (should also work on 3.8, but tested on 3.9+)
- Runs on Linux/macOS/Windows

---

## Running

From the repository root:

```bash
python3 search_core.py
```

You’ll be prompted to select a case:

- **Case 1**  
  - Start: `[8,0,0]`  
  - Capacities: `[8,5,3]`  
  - Goal: `[4,4,0]`

- **Case 2**  
  - Start: `[1,3,5]`  
  - Capacities: `[3,5,8]`  
  - Goal: `[0,5,4]`

### Non‑interactive run (Linux/macOS)
```bash
echo 1 | python3 search_core.py    # runs Case 1
echo 2 | python3 search_core.py    # runs Case 2
```

### Non‑interactive run (Windows PowerShell)
```powershell
"1" | python .\search_core.py
"2" | python .\search_core.py
```

---

## What the output means

- **“BFS/IDFS Path”**: the sequence of `(state, action)` pairs from start to goal. The first action is labeled `"Start"`.
- **RESULTS metrics** (reported for each algorithm):
  - **Generated** — number of nodes generated (expansions + enqueues/pushes after duplicate filtering *within* each search run).
  - **Depth** — depth of the goal node.
  - **Cost** — path length (same as depth here; unit actions).
  - **Max Size** — maximum size of the frontier (queue for BFS, stack for IDS).

> **Note on duplicates:**  
> BFS and each depth‑limited DFS pass keep a `visited` set and avoid re‑adding already‑seen states in that pass. IDS restarts with increasing depth limits, so states can be revisited across iterations (expected behavior of IDS).

---

## Example (Case 1)

One sample run produced:

| Case | Algorithm | Nodes Generated | Depth | Path Cost | Max Frontier Size |
|------|-----------|-----------------|-------|-----------|-------------------|
| 1    | BFS       | 16              | 7     | 7         | 3                 |
| 1    | IDS       | 57              | 7     | 7         | 3                 |

Interpretation: both find an optimal (length‑7) solution; BFS generates fewer nodes on this instance because the solution is near the top of the tree, while IDS pays the typical re‑exploration cost across depth limits.

---

## Reproducing / Adding New Cases

To add a new case, edit `main()` in `search_core.py` and create a new initial node and goal:
```python
init = Node(state=[start amounts], cap=[capacities])
goal = [target amounts]
bfs_path = bfsSearch(init, goal)
ids_path = IDFS_Caller(init, goal)
```

Keep capacities and amounts as non‑negative integers, and make sure each amount is ≤ its capacity.

---

## Known limitations / notes

- Global counters (e.g., `BFSGenerated`, `IDFSGenerated`) are shared per run; they’re reset only when the program starts. If you wire more than two cases into a single run, reset those variables before each run or create per‑run counters.
- IDS duplicate detection resets on each new depth limit by design; therefore, it typically generates more nodes than BFS when solutions are shallow.

---

## Citation / Acknowledgment

This implementation is for an AI assignment (Water Jugs domain) comparing BFS and IDS using a graph‑search variant with per‑run duplicate detection.
