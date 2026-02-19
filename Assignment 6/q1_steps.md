# Step-by-Step Execution of Search Algorithms

This document details the step-by-step decision-making process for both Greedy Best-First Search and A* Search as implemented in `q1.py`.

## Problem Overview

*   **Start City**: Chicago
*   **Goal City**: Boston
*   **Heuristic ($h$)**: Straight-line distance to Boston.

---

## 1. Greedy Best-First Search (GBFS)

**Strategy**: Always expand the node with the lowest heuristic value $h(n)$. It does not consider the path cost $g(n)$.

| Step | Current Node | Neighbors (Heuristic Values) | Decision | Reason |
| :--- | :--- | :--- | :--- | :--- |
| **1** | **Chicago** ($h=860$) | Detroit ($h=610$)<br>Cleveland ($h=550$)<br>Indianapolis ($h=780$) | Choose **Cleveland** | Lowest $h$ value (550). |
| **2** | **Cleveland** ($h=550$) | Chicago (visited)<br>Detroit (visited)<br>Buffalo ($h=400$)<br>Columbus ($h=640$)<br>Pittsburgh ($h=470$) | Choose **Buffalo** | Lowest $h$ value (400) among unvisited neighbors. |
| **3** | **Buffalo** ($h=400$) | Detroit (visited)<br>Cleveland (visited)<br>Syracuse ($h=260$)<br>Pittsburgh ($h=470$) | Choose **Syracuse** | Lowest $h$ value (260). |
| **4** | **Syracuse** ($h=260$) | Buffalo (visited)<br>Boston ($h=0$)<br>Philadelphia ($h=270$) | Choose **Boston** | Lowest $h$ value (0). |
| **5** | **Boston** | - | **Goal Reached** | $h=0$. |

**Final Path**: Chicago $\rightarrow$ Cleveland $\rightarrow$ Buffalo $\rightarrow$ Syracuse $\rightarrow$ Boston
**Total Explorations**: 5

---

## 2. A* Search

**Strategy**: Expand the node with the lowest $f(n) = g(n) + h(n)$, where $g(n)$ is the cost from the start node and $h(n)$ is the heuristic.

| Step | Current Node | Neighbors ($g + h = f$) | Frontier (Queue) Status | Decision |
| :--- | :--- | :--- | :--- | :--- |
| **1** | **Chicago** | Detroit ($283+610=893$)<br>Cleveland ($345+550=895$)<br>Indianapolis ($182+780=962$) | `[Detroit(893), Cleveland(895), Indianapolis(962)]` | Pop **Detroit** ($f=893$) |
| **2** | **Detroit** | Chicago (visited)<br>Cleveland ($283+169+550=1002$)<br>Buffalo ($283+256+400=939$) | `[Cleveland(895), Buffalo(939), Indianapolis(962)]` <br>*(Note: Detroit path to Cleveland is worse than direct, so Cleveland stays 895)* | Pop **Cleveland** ($f=895$) |
| **3** | **Cleveland** | Chicago (visited)<br>Detroit (visited)<br>Buffalo ($345+189+400=934$)<br>Columbus ($345+144+640=1129$)<br>Pittsburgh ($345+134+470=949$) | `[Buffalo(934), Buffalo(939), Pittsburgh(949), Indianapolis(962), Columbus(1129)]` | Pop **Buffalo** ($f=934$) |
| **4** | **Buffalo** (via Cleveland) | Detroit (visited)<br>Cleveland (visited)<br>Syracuse ($534+150+260=944$)<br>Pittsburgh ($534+215+470=1219$) | `[Buffalo(939), Syracuse(944), Pittsburgh(949), Indianapolis(962), ...]` | Pop **Buffalo** ($f=939$) |
| **5** | **Buffalo** (via Detroit) | *Already explored better path via Cleveland.* | `[Syracuse(944), Pittsburgh(949), Indianapolis(962), ...]` | *(Skipped/Redundant)* <br> Pop **Syracuse** ($f=944$) |
| **6** | **Syracuse** | Buffalo (visited)<br>Boston ($684+312+0=996$)<br>Philadelphia ($684+253+270=1207$) | `[Pittsburgh(949), Indianapolis(962), Boston(996), ...]` | Pop **Pittsburgh** ($f=949$) |
| **7** | **Pittsburgh** | Cleveland (visited)<br>Buffalo (visited)<br>Columbus ($479+185+640=1304$)<br>Philadelphia ($479+305+270=1054$)<br>Baltimore ($479+247+360=1086$) | `[Indianapolis(962), Boston(996), Philadelphia(1054), ...]` | Pop **Indianapolis** ($f=962$) |
| **8** | **Indianapolis** | Chicago (visited)<br>Columbus ($182+176+640=998$) | `[Boston(996), Columbus(998), Philadelphia(1054), ...]` | Pop **Boston** ($f=996$) |
| **9** | **Boston** | - | **Goal Reached** | Target Found. |

**Final Path**: Chicago $\rightarrow$ Cleveland $\rightarrow$ Buffalo $\rightarrow$ Syracuse $\rightarrow$ Boston
**Total Explorations**: 9

> **Note**: A* explored more nodes (Detroit, Pittsburgh, Indianapolis) because their $f$-values were lower than the cost to reach Boston at that moment ($f < 996$). This cautiousness guarantees the shortest path.
