# -*- coding: utf-8 -*-
"""
Practica - 3 Algoritmo de Dijkstra
Jayden Hammond Caballero - 22310235
"""
# =============================================================================
# #f5 Para ejecutar
# =============================================================================
# Simulador de rutas de entrega con el Algoritmo de Dijkstra
# Empresa de mensajería en una ciudad

import heapq
import matplotlib.pyplot as plt
import networkx as nx

# MAPA
barrios = {
    'Centro': {'Norte': 2, 'Este': 4},
    'Norte': {'Centro': 2, 'Oeste': 5, 'Parque': 10},
    'Este': {'Centro': 4, 'Parque': 3},
    'Oeste': {'Norte': 5, 'Parque': 2},
    'Parque': {'Este': 3, 'Oeste': 2, 'Terminal': 6},
    'Terminal': {}
}

# ALGORITMO
def dijkstra(mapa, inicio):
    distancias = {lugar: float('inf') for lugar in mapa}
    distancias[inicio] = 0
    anteriores = {lugar: None for lugar in mapa}
    cola = [(0, inicio)]
    pasos = []

    while cola:
        distancia_actual, actual = heapq.heappop(cola)
        pasos.append((actual, dict(distancias)))

        for vecino, peso in mapa[actual].items():
            nueva_distancia = distancia_actual + peso
            if nueva_distancia < distancias[vecino]:
                distancias[vecino] = nueva_distancia
                anteriores[vecino] = actual
                heapq.heappush(cola, (nueva_distancia, vecino))

    return distancias, anteriores, pasos

# PASOS
def mostrar_pasos(pasos):
    for i, (actual, dist) in enumerate(pasos):
        print(f"Paso {i + 1}: Domicilio '{actual}'")
        for lugar, d in dist.items():
            print(f"  Distancia desde INICIO a {lugar}: {d}")
        print()

# GRAFICAR
def graficar_mapa(mapa, anteriores):
    G = nx.DiGraph()
    pos = nx.spring_layout(mapa, seed=5)

    for lugar, conexiones in mapa.items():
        for destino, peso in conexiones.items():
            G.add_edge(lugar, destino, weight=peso)

    nx.draw_networkx_nodes(G, pos, node_size=800, node_color='lightgreen')
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos, edge_color='gray', arrowsize=20)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'))

    # Rutas óptimas
    rutas = [(prev, lugar) for lugar, prev in anteriores.items() if prev]
    nx.draw_networkx_edges(G, pos, edgelist=rutas, width=3, edge_color='red', arrows=True)

    plt.title("Shortcut - Empresa de Mensajería")
    plt.axis('off')
    plt.show()

# RESULTADOS
if __name__ == "__main__":
    origen = 'Centro'
    distancias, anteriores, pasos = dijkstra(barrios, origen)

    print(f"\n Simulación de Ruta de Entrega desde el barrio '{origen}'\n")
    mostrar_pasos(pasos)

    print(" Distancias mínimas desde el inicio:")
    for lugar, d in distancias.items():
        print(f"  {origen} → {lugar}: {d} km")

    graficar_mapa(barrios, anteriores)
