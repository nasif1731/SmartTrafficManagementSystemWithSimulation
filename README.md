
# Smart Traffic Management System 🚦

**Python-Based Traffic Optimization and Simulation Using Graph Theory, Dynamic Programming & Pygame**

---

## 📌 Overview

The **Smart Traffic Management System** models and optimizes city-wide traffic flow using graph-based algorithms and real-time simulations. This system helps demonstrate how intelligent routing strategies and traffic light optimization can mitigate congestion and improve vehicle movement—even in the presence of accidents.

### 🔧 Built With:

* **Python**
* **NetworkX** (Graph modeling)
* **Dynamic Programming** (Traffic light optimization)
* **Dijkstra’s Algorithm** (Routing)
* **Pygame** (Traffic simulation)

---

## ⚙️ Features

### 🧠 Intelligent Core

* **Graph-Based City Model**: Roads as undirected edges; intersections as nodes.
* **Shortest Path Routing**: Dijkstra’s algorithm for optimal vehicle paths.
* **Traffic Light Optimization**: Dynamic programming allocates green timings based on inflow.

### 🚗 Vehicle Routing Strategies

1. **Greedy** – Routes vehicles independently (updates congestion post-routing).
2. **Coordinated** – Routes all vehicles together to balance congestion.
3. **Optimized** – Dynamically adjusts edge weights based on usage.

### 💥 Real-Time Simulation

* **Accident Simulation**: Random edge blockage and rerouting.
* **Traffic Visualization**:
  * Vehicles (animated)
  * Traffic lights (red/green)
  * Congestion (line color intensity)
  * Accidents (red circles)

---

## 📂 File Structure

```
Smart_Traffic_Management_System/
│
├── Smart_Traffic_Management_System.ipynb   # Analysis + optimization notebook
├── main_simulation_strategic_paths_cleaned.py  # Pygame-based simulator
├── data/
│   ├── city_map.json                       # Nodes & edges
│   ├── traffic_data_case1.csv              # Light traffic
│   ├── traffic_data_case2.csv              # Jam on B–D
│   └── traffic_data_case3.csv              # Multiple congestions

```

---

## 🚀 Getting Started

### 🔨 Installation

```bash
pip install networkx matplotlib pandas pygame
```

### 📈 Run Notebook (Analysis & Timings)

```bash
jupyter notebook Smart_Traffic_Management_System.ipynb
```

Notebook functionalities:

* Load and visualize traffic graphs
* Analyze different traffic scenarios
* Compute shortest paths (Dijkstra)
* Generate green light durations (Dynamic Programming)

### 🕹️ Run Simulation (Visualization)

```bash
python main_simulation_strategic_paths_cleaned.py
```

Simulates traffic flow between points A, C, and E to destination F under various strategies.

---

## 🎮 Controls (During Simulation)

| Key        | Action                                    |
| ---------- | ----------------------------------------- |
| `Spacebar` | Cycle between routing strategies          |
| `A`        | Trigger a random accident (road blockage) |
| `X`        | Close simulation                          |

---

## 🧬 How It Works

* **Graph Construction**: Builds undirected graph using traffic multipliers from `.csv`.
* **Routing**: Dijkstra’s algorithm determines least congested paths.
* **Green Light Optimization**: Dynamic programming assigns optimal green durations per node.
* **Simulation Loop**:
  * Vehicles animate along their paths
  * Congestion adjusts per strategy
  * Accidents force re-routing in real-time

---

## 🧪 Example Scenarios

| Case   | Description              |
| ------ | ------------------------ |
| Case 1 | Light Traffic            |
| Case 2 | Traffic Jam on B–D      |
| Case 3 | Multiple Congested Roads |

---

## 📈 Visualization Insights

* **Intersections**: Orange nodes
* **Roads**: Colored lines (intensity = congestion)
* **Traffic Lights**: Red/Green dots
* **Vehicles**: Moving animated dots
* **Accidents**: Red-circled blocked roads

---

## 🚧 Future Improvements

* Synchronize traffic light states using optimized timings
* Use directed graphs for one-way traffic modeling
* Add support for time-varying traffic patterns
* Integrate traffic flow analytics dashboard

---
