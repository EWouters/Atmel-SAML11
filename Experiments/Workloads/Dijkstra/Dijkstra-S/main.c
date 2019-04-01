#include <atmel_start.h>

//#define DEBUG_PRINT

#ifdef DEBUG_PRINT
#include <stdio.h>
#endif // DEBUG_PRINT

#include <stdlib.h>
#include <limits.h>

typedef struct {
	uint8_t vertex;
	uint8_t weight;
} edge_t;

typedef struct {
	edge_t **edges;
	uint8_t edges_len;
	uint8_t edges_size;
	int dist;
	uint8_t prev;
	uint8_t visited;
} vertex_t;

typedef struct {
	vertex_t **vertices;
	uint8_t vertices_len;
	uint8_t vertices_size;
} graph_t;

typedef struct {
	uint8_t *data;
	uint8_t *prio;
	uint8_t *index;
	uint8_t len;
	uint8_t size;
} heap_t;

void add_vertex (graph_t *g, uint8_t i) {
	if (g->vertices_size < i + 1) {
		uint8_t size = g->vertices_size * 2 > i ? g->vertices_size * 2 : i + 4;
		g->vertices = realloc(g->vertices, size * sizeof (vertex_t *));
		for (uint8_t j = g->vertices_size; j < size; j++)
		g->vertices[j] = NULL;
		g->vertices_size = size;
	}
	if (!g->vertices[i]) {
		g->vertices[i] = calloc(1, sizeof (vertex_t));
		g->vertices_len++;
	}
}

void add_edge (graph_t *g, uint8_t a, uint8_t b, uint8_t w) {
	add_vertex(g, a);
	add_vertex(g, b);
	vertex_t *v = g->vertices[a];
	if (v->edges_len >= v->edges_size) {
		v->edges_size = v->edges_size ? v->edges_size * 2 : 4;
		v->edges = realloc(v->edges, v->edges_size * sizeof (edge_t *));
	}
	edge_t *e = calloc(1, sizeof (edge_t));
	e->vertex = b;
	e->weight = w;
	v->edges[v->edges_len++] = e;
}

heap_t *create_heap (uint8_t n) {
	heap_t *h = calloc(1, sizeof (heap_t));
	h->data = calloc(n + 1, sizeof (uint8_t));
	h->prio = calloc(n + 1, sizeof (uint8_t));
	h->index = calloc(n, sizeof (uint8_t));
	return h;
}

void push_heap (heap_t *h, uint8_t v, uint8_t p) {
	uint8_t i = h->index[v] == 0 ? ++h->len : h->index[v];
	uint8_t j = i / 2;
	while (i > 1) {
		if (h->prio[j] < p)
		break;
		h->data[i] = h->data[j];
		h->prio[i] = h->prio[j];
		h->index[h->data[i]] = i;
		i = j;
		j = j / 2;
	}
	h->data[i] = v;
	h->prio[i] = p;
	h->index[v] = i;
}

uint8_t min (heap_t *h, uint8_t i, uint8_t j, uint8_t k) {
	uint8_t m = i;
	if (j <= h->len && h->prio[j] < h->prio[m])
	m = j;
	if (k <= h->len && h->prio[k] < h->prio[m])
	m = k;
	return m;
}

uint8_t pop_heap (heap_t *h) {
	uint8_t v = h->data[1];
	uint8_t i = 1;
	while (1) {
		uint8_t j = min(h, h->len, 2 * i, 2 * i + 1);
		if (j == h->len)
		break;
		h->data[i] = h->data[j];
		h->prio[i] = h->prio[j];
		h->index[h->data[i]] = i;
		i = j;
	}
	h->data[i] = h->data[h->len];
	h->prio[i] = h->prio[h->len];
	h->index[h->data[i]] = i;
	h->len--;
	return v;
}

void dijkstra (graph_t *g, uint8_t a, uint8_t b) {
	uint8_t i, j;
	for (i = 0; i < g->vertices_len; i++) {
		vertex_t *v = g->vertices[i];
		v->dist = INT_MAX;
		v->prev = 0;
		v->visited = 0;
	}
	vertex_t *v = g->vertices[a];
	v->dist = 0;
	heap_t *h = create_heap(g->vertices_len);
	push_heap(h, a, v->dist);
	while (h->len) {
		i = pop_heap(h);
		if (i == b)
		break;
		v = g->vertices[i];
		v->visited = 1;
		for (j = 0; j < v->edges_len; j++) {
			edge_t *e = v->edges[j];
			vertex_t *u = g->vertices[e->vertex];
			if (!u->visited && v->dist + e->weight <= u->dist) {
				u->prev = i;
				u->dist = v->dist + e->weight;
				push_heap(h, e->vertex, u->dist);
			}
		}
	}
}

#ifdef DEBUG_PRINT
void print_path (graph_t *g, uint8_t i) {
	uint8_t n;
	vertex_t *v, *u;
	v = g->vertices[i];
	if (v->dist == INT_MAX) {
		printf("no path\n");
		return;
	}
	for (n = 1, u = v; u->dist; u = g->vertices[u->prev], n++)
	;
	printf("length: %d hops: %d, path: %d", v->dist, n-1, i);
	for (u = v; u->dist; u = g->vertices[u->prev])
	printf("<-%d",u->prev);
}
#endif // DEBUG_PRINT

int main (void) {
	graph_t *g = calloc(1, sizeof (graph_t));
	add_edge(g, 36, 21, 147);
	add_edge(g, 38, 21, 176);
	add_edge(g, 26, 22, 223);
	add_edge(g, 9, 27, 163);
	add_edge(g, 10, 39, 249);
	add_edge(g, 11, 33, 53);
	add_edge(g, 39, 5, 98);
	add_edge(g, 20, 12, 171);
	add_edge(g, 16, 38, 214);
	add_edge(g, 0, 13, 206);
	add_edge(g, 21, 9, 105);
	add_edge(g, 0, 34, 178);
	add_edge(g, 14, 0, 92);
	add_edge(g, 12, 23, 80);
	add_edge(g, 1, 6, 191);
	add_edge(g, 34, 7, 107);
	add_edge(g, 38, 25, 188);
	add_edge(g, 6, 31, 129);
	add_edge(g, 22, 13, 181);
	add_edge(g, 7, 24, 21);
	add_edge(g, 18, 31, 254);
	add_edge(g, 15, 6, 30);
	add_edge(g, 19, 23, 159);
	add_edge(g, 16, 7, 141);
	add_edge(g, 34, 25, 198);
	add_edge(g, 38, 29, 101);
	add_edge(g, 16, 11, 41);
	add_edge(g, 10, 14, 3);
	add_edge(g, 21, 11, 67);
	add_edge(g, 1, 30, 137);
	add_edge(g, 4, 9, 179);
	add_edge(g, 1, 8, 163);
	add_edge(g, 34, 6, 122);
	add_edge(g, 19, 15, 86);
	add_edge(g, 32, 11, 219);
	add_edge(g, 27, 21, 25);
	add_edge(g, 14, 25, 105);
	add_edge(g, 31, 17, 55);
	add_edge(g, 17, 1, 242);
	add_edge(g, 8, 14, 251);
	add_edge(g, 22, 24, 46);
	add_edge(g, 38, 36, 113);
	add_edge(g, 15, 24, 56);
	add_edge(g, 23, 5, 90);
	add_edge(g, 27, 24, 73);
	add_edge(g, 10, 34, 26);
	add_edge(g, 27, 31, 227);
	add_edge(g, 37, 23, 91);
	add_edge(g, 5, 3, 66);
	add_edge(g, 32, 28, 110);
	add_edge(g, 8, 2, 80);
	add_edge(g, 19, 35, 214);
	add_edge(g, 6, 8, 152);
	add_edge(g, 29, 22, 199);
	add_edge(g, 16, 26, 203);
	add_edge(g, 32, 35, 173);
	add_edge(g, 38, 8, 135);
	add_edge(g, 29, 17, 76);
	add_edge(g, 11, 26, 219);
	add_edge(g, 16, 36, 152);
	add_edge(g, 20, 10, 87);
	add_edge(g, 19, 24, 134);
	add_edge(g, 14, 34, 96);
	add_edge(g, 8, 30, 11);
	add_edge(g, 0, 25, 5);
	add_edge(g, 35, 9, 58);
	add_edge(g, 35, 8, 202);
	add_edge(g, 35, 10, 58);
	add_edge(g, 19, 5, 107);
	add_edge(g, 18, 38, 151);
	add_edge(g, 18, 11, 176);
	add_edge(g, 27, 16, 42);
	add_edge(g, 37, 32, 126);
	add_edge(g, 34, 37, 106);
	add_edge(g, 18, 5, 91);
	add_edge(g, 30, 38, 95);
	add_edge(g, 19, 1, 122);
	add_edge(g, 39, 24, 218);
	add_edge(g, 17, 28, 24);
	add_edge(g, 24, 30, 186);
	add_edge(g, 24, 6, 150);
	add_edge(g, 25, 15, 5);
	add_edge(g, 27, 14, 5);
	add_edge(g, 33, 1, 28);
	add_edge(g, 12, 25, 98);
	add_edge(g, 22, 26, 70);
	add_edge(g, 10, 35, 210);
	add_edge(g, 36, 14, 188);
	add_edge(g, 38, 19, 254);
	add_edge(g, 38, 1, 242);
	
	START_MEASURE(DGI_GPIO2);
	dijkstra(g, 0, 39);
	STOP_MEASURE(DGI_GPIO2);
	
	#ifdef DEBUG_PRINT
	print_path(g, 39);
	#endif // DEBUG_PRINT
	
	END_MEASUREMENT;
	
	return 0;
}
