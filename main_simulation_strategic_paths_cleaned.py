
import pygame
import json
import pandas as pd
import networkx as nx
import heapq
import time
import random

# === CONFIG ===
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 700
NODE_RADIUS = 15
VEHICLE_RADIUS = 8
FPS = 60

with open('data/city_map.json', 'r') as f:
    city_data = json.load(f)

NODES = city_data['nodes']
EDGES = city_data['edges']

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Smart Traffic System — Strategy Visualizer")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

node_positions = {
    'A': (100, 300), 'B': (250, 200), 'C': (250, 400),
    'D': (450, 300), 'E': (650, 200), 'F': (650, 400)
}

# === Core Logic Functions ===
accident_edge = None 
def build_graph(case_csv):
    traffic_df = pd.read_csv(case_csv)
    traffic_map = dict(zip(traffic_df['road'], traffic_df['traffic_multiplier']))
    G = nx.Graph()
    G.add_nodes_from(NODES)
    for edge in EDGES:
        u = edge['from']
        v = edge['to']
        if (u, v) == accident_edge or (v, u) == accident_edge:
            continue  # Block accident edge
        v = edge['to']
        base_cost = edge['base_cost']
        road = f"{u}-{v}" if f"{u}-{v}" in traffic_map else f"{v}-{u}"
        multiplier = traffic_map.get(road, 1.0)
        total_cost = base_cost * multiplier
        G.add_edge(u, v,
                   weight=total_cost,
                   base_cost=base_cost,
                   multiplier=multiplier)
    return G

def dijkstra_manual(G, start, end):
    dist = {node: float('inf') for node in G.nodes}
    prev = {node: None for node in G.nodes}
    dist[start] = 0
    heap = [(0, start)]
    while heap:
        current_cost, node = heapq.heappop(heap)
        for neighbor in G.neighbors(node):
            path_cost = current_cost + G[node][neighbor]['weight']
            if path_cost < dist[neighbor]:
                dist[neighbor] = path_cost
                prev[neighbor] = node
                heapq.heappush(heap, (path_cost, neighbor))
    path = []
    current = end
    while current:
        path.insert(0, current)
        current = prev[current]
    return path, dist[end] if path[0] == start else ([], float('inf'))

def update_congestion(G, vehicle_paths, step=0.3, max_multiplier=3.0):
    for vehicle in vehicle_paths:
        path = vehicle['path']
        if not path:
            continue
        for i in range(len(path)-1):
            u, v = path[i], path[i+1]
            edge = G[u][v]
            new_mult = min(edge['multiplier'] + step, max_multiplier)
            edge['multiplier'] = new_mult
            edge['weight'] = edge['base_cost'] * new_mult

def simulate_vehicle(path, color, label):
    for i in range(len(path) - 1):
        start_pos = node_positions[path[i]]
        end_pos = node_positions[path[i+1]]
        for step in range(20):
            x = start_pos[0] + (end_pos[0] - start_pos[0]) * step / 20
            y = start_pos[1] + (end_pos[1] - start_pos[1]) * step / 20
            screen.fill((255, 255, 255))
            draw_graph(G)
            draw_traffic_lights(G)
            pygame.draw.circle(screen, color, (int(x), int(y)), VEHICLE_RADIUS)
            render_text(f"{label}: {' → '.join(path)}", (50, 20))
            pygame.display.flip()
            clock.tick(FPS // 2)

def render_text(text, pos):
    txt_surface = font.render(text, True, (0, 0, 0))
    screen.blit(txt_surface, pos)


def draw_traffic_lights(G):
    for node in G.nodes:
        incoming = list(G.neighbors(node))
        if not incoming:
            continue
        green = random.choice(incoming) 
        for neighbor in incoming:
            pos = node_positions[node]
            dx, dy = node_positions[neighbor][0] - pos[0], node_positions[neighbor][1] - pos[1]
            norm = (dx**2 + dy**2) ** 0.5
            if norm == 0: continue
            dx, dy = dx / norm * 10, dy / norm * 10
            color = (0, 255, 0) if neighbor == green else (255, 0, 0)
            pygame.draw.circle(screen, color, (int(pos[0] + dx), int(pos[1] + dy)), 5)

def simulate_random_accident(G):
    global accident_edge
    all_edges = list(G.edges())
    if not all_edges:
        return
    accident_edge = random.choice(all_edges)
    print(f"🚨 Accident occurred on road: {accident_edge}")

def draw_accident(G):
    if not accident_edge:
        return
    u, v = accident_edge
    if not G.has_edge(u, v):
        mid_x = (node_positions[u][0] + node_positions[v][0]) // 2
        mid_y = (node_positions[u][1] + node_positions[v][1]) // 2
        pygame.draw.circle(screen, (255, 0, 0), (mid_x, mid_y), 10)


def draw_graph(G):
    draw_traffic_lights(G)
    draw_accident(G)
    for u, v in G.edges():
        mult = G[u][v]['multiplier']
        color = (200 - int(mult*50), 200 - int(mult*50), 200)
        pygame.draw.line(screen, color, node_positions[u], node_positions[v], 3)
    for node, (x, y) in node_positions.items():
        pygame.draw.circle(screen, (255, 165, 0), (x, y), NODE_RADIUS)
        text = font.render(node, True, (0, 0, 0))
        screen.blit(text, (x - 10, y - 10))


def greedy_vehicle_routing(G, start_nodes, end_node, step=0.3, max_multiplier=3.0):
    results = []
    for start in start_nodes:
        path, cost = dijkstra_manual(G, start, end_node)
        results.append({"vehicle": f"{start}→{end_node}", "path": path, "cost": cost})
        if path:
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                edge = G[u][v]
                edge['multiplier'] = min(edge['multiplier'] + step, max_multiplier)
                edge['weight'] = edge['base_cost'] * edge['multiplier']
    return results

def coordinated_vehicle_routing(G, start_nodes, end_node, step=0.3, max_multiplier=3.0):
    results = []
    usage = {}
    for start in start_nodes:
        path, cost = dijkstra_manual(G, start, end_node)
        results.append({"vehicle": f"{start}→{end_node}", "path": path, "cost": cost})
        if path:
            for i in range(len(path) - 1):
                key = tuple(sorted((path[i], path[i + 1])))
                usage[key] = usage.get(key, 0) + 1
    for (u, v), count in usage.items():
        edge = G[u][v]
        edge['multiplier'] = min(edge['multiplier'] + step * count, max_multiplier)
        edge['weight'] = edge['base_cost'] * edge['multiplier']
    return results

def optimized_vehicle_routing(G, start_nodes, end_node, step=0.3, max_multiplier=3.0):
    edge_usage = {}
    results = []
    for start in start_nodes:
        for u, v in G.edges():
            usage = edge_usage.get(tuple(sorted((u, v))), 0)
            multiplier = min(1.0 + step * usage, max_multiplier)
            G[u][v]['weight'] = G[u][v]['base_cost'] * multiplier
        path, cost = dijkstra_manual(G, start, end_node)
        results.append({"vehicle": f"{start}→{end_node}", "path": path, "cost": cost})
        if path:
            for i in range(len(path) - 1):
                key = tuple(sorted((path[i], path[i + 1])))
                edge_usage[key] = edge_usage.get(key, 0) + 1
    return results

def route_vehicles(G, strategy_name):
    starts = ["A", "C", "E"]
    if strategy_name == "Greedy Strategy":
        return greedy_vehicle_routing(G, starts, "F")
    elif strategy_name == "Coordinated Strategy":
        return coordinated_vehicle_routing(G, starts, "F")
    elif strategy_name == "Optimized Strategy":
        return optimized_vehicle_routing(G, starts, "F")
    else:
        return []

    vehicle_starts = ["A", "C", "E"]
    vehicle_paths = []
    for start in vehicle_starts:
        path, cost = dijkstra_manual(G, start, "F")
        vehicle_paths.append({"vehicle": f"{start}→F", "path": path, "cost": cost})
    strategy_fn(G, vehicle_paths)
    return vehicle_paths

# === Strategy Definitions ===
def greedy(G, paths): update_congestion(G, paths, step=0.3)
def coordinated(G, paths): update_congestion(G, paths, step=0.5)
def optimized(G, paths): update_congestion(G, paths, step=0.7)

strategies = [
    ("Greedy Strategy", greedy),
    ("Coordinated Strategy", coordinated),
    ("Optimized Strategy", optimized)
]

# === Main Loop ===
case_csv = 'data/traffic_data_case1.csv'
running = True
strategy_index = 0

while running:
    G = build_graph(case_csv)
    strategy_name, strategy_fn = strategies[strategy_index]
    vehicle_paths = route_vehicles(G,strategy_name)

    for path_info, color in zip(vehicle_paths, [(255, 0, 0), (0, 0, 255), (0, 128, 0)]):
        simulate_vehicle(path_info['path'], color, path_info['vehicle'])

    screen.fill((255, 255, 255))
    draw_graph(G)
    draw_traffic_lights(G)
    render_text(f"Strategy: {strategy_name}", (300, 20))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                waiting = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    strategy_index = (strategy_index + 1) % len(strategies)
                    waiting = False
                elif event.key == pygame.K_a:
                    simulate_random_accident(G)
                    G = build_graph(case_csv)
                    vehicle_paths = route_vehicles(G, strategy_name)
                    for path_info, color in zip(vehicle_paths, [(255, 0, 0), (0, 0, 255), (0, 128, 0)]):
                        simulate_vehicle(path_info['path'], color, path_info['vehicle'])
                    screen.fill((255, 255, 255))
                    draw_graph(G)
                    draw_traffic_lights(G)
                    render_text(f"Strategy: {strategy_name} (Accident)", (250, 20))
                    pygame.display.flip()

pygame.quit()

