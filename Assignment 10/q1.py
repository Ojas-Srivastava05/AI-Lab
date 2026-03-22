import math
import random

def load_data(filename):
    data = []
    with open(filename, 'r') as f:
        for line in f:
            if line.strip():
                x, y = map(float, line.strip().split(','))
                data.append((x, y))
    return data

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def assign_clusters(data, centers):
    labels = []
    for p in data:
        dist = [distance(p, c) for c in centers]
        labels.append(dist.index(min(dist)))
    return labels

def compute_ssd(data, centers, labels):
    ssd = 0
    ssd_per_cluster = []
    k = len(centers)
    for i in range(k):
        cluster_data = [data[j] for j in range(len(data)) if labels[j] == i]
        val = sum(distance(p, centers[i])**2 for p in cluster_data)
        ssd += val
        ssd_per_cluster.append(val)
    return ssd, ssd_per_cluster

def gradient_descent_update(cluster_data, current_center, alpha=0.001, epochs=50):
    if not cluster_data:
        return current_center
    cx, cy = current_center
    for _ in range(epochs):
        grad_x = sum(2 * (cx - p[0]) for p in cluster_data)
        grad_y = sum(2 * (cy - p[1]) for p in cluster_data)
        cx -= alpha * grad_x
        cy -= alpha * grad_y
    return (cx, cy)

def newton_raphson_update(cluster_data, current_center):
    if not cluster_data:
        return current_center
    n = len(cluster_data)
    cx, cy = current_center
    grad_x = sum(2 * (cx - p[0]) for p in cluster_data)
    grad_y = sum(2 * (cy - p[1]) for p in cluster_data)
    
    # Hessian is diag(2n, 2n)
    hessian_inv_x = 1.0 / (2 * n)
    hessian_inv_y = 1.0 / (2 * n)
    
    cx -= hessian_inv_x * grad_x
    cy -= hessian_inv_y * grad_y
    
    return (cx, cy)

def kmeans(data, k=3, method='nr', max_iters=100, init_centers=None):
    if init_centers is not None:
        centers = list(init_centers)
    else:
        random.seed(42)
        centers = random.sample(data, k)
        
    labels = [-1] * len(data)
    
    for _ in range(max_iters):
        new_labels = assign_clusters(data, centers)
        
        if labels == new_labels:
            break
        labels = new_labels
        
        for i in range(k):
            cluster_data = [data[j] for j in range(len(data)) if labels[j] == i]
            if cluster_data:
                if method == 'gd':
                    centers[i] = gradient_descent_update(cluster_data, centers[i])
                elif method == 'nr':
                    centers[i] = newton_raphson_update(cluster_data, centers[i])
                    
    return centers, labels


def main():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'cities.csv')
    data = load_data(file_path)
    k = 3
    
    random.seed(1337)
    init_centers = random.sample(data, k)
    
    print("--- Gradient Descent Method ---")
    centers_gd, labels_gd = kmeans(data, k=3, method='gd', max_iters=100, init_centers=init_centers)
    ssd_gd, ssd_clust_gd = compute_ssd(data, centers_gd, labels_gd)
    print("Cluster Centers:")
    for i, c in enumerate(centers_gd):
        print(f"Cluster {i+1}: ({c[0]:.4f}, {c[1]:.4f}) -> SSD: {ssd_clust_gd[i]:.4f}")
    print(f"Total SSD: {ssd_gd:.4f}\n")
    
    print("--- Newton Raphson Method ---")
    centers_nr, labels_nr = kmeans(data, k=3, method='nr', max_iters=100, init_centers=init_centers)
    ssd_nr, ssd_clust_nr = compute_ssd(data, centers_nr, labels_nr)
    print("Cluster Centers:")
    for i, c in enumerate(centers_nr):
        print(f"Cluster {i+1}: ({c[0]:.4f}, {c[1]:.4f}) -> SSD: {ssd_clust_nr[i]:.4f}")
    print(f"Total SSD: {ssd_nr:.4f}")

if __name__ == '__main__':
    main()
