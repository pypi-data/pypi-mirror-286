import Vertex from './vertex';

export interface EdgeProps {
    source: string;
    target: string;
}

interface Vertices {
    [id: string]: Vertex;
}

interface Adj {
    [id: string]: Set<string>;
}

class Graph {
    nVerts = 0;
    vertices: Vertices = {};
    adj: Adj = {};
    isUpdate!: boolean;

    addVertex(id: string, x?: number, y?: number) {
        this.vertices[id] = new Vertex(id, x, y);
        ++this.nVerts;
        return id;
    }

    deleteVertex(id: string) {
        delete this.vertices[id];
        --this.nVerts;
        return id;
    }

    addEdge(u: string, v: string) {
        this.adj[u] = this.adj[u] || new Set();
        this.adj[u].add(v);
        this.vertices[u].edgeNum++;
        this.adj[v] = this.adj[v] || new Set();
        this.adj[v].add(u);
        this.vertices[v].edgeNum++;
    }

    deleteEdge(u: string, v: string) {
        this.removeAdj(u, v);
        this.removeAdj(v, u);
    }

    removeAdj(a: string, b: string) {
        if (!this.adj[a]) return;
        this.adj[a].delete(b);
        if (!this.vertices[a]) return;
        this.vertices[a].edgeNum--;
    }

    getVertex(id: string) {
        return this.vertices[id];
    }

    getSize() {
        return this.nVerts;
    }

    getDegree(v: string) {
        return this.adj[v].size;
    }

    forEachVertex(callback: (vertex?: Vertex, idx?: string) => void): void {
        for (let i in this.vertices) {
            if (this.vertices.hasOwnProperty(i)) {
                callback(this.vertices[i], i);
            }
        }
    }

    forEachEdge(callback: (v?: Vertex, u?: Vertex) => void): void {
        this.forEachVertex((v, i) => {
            if (!this.adj[i!]) return;
            this.adj[i!].forEach(n => callback(v, this.vertices[n]));
        });
    }

    constructor(vertices: Array<Vertex> = [], edges: Array<EdgeProps> = []) {
        for (let i = 0; i < vertices.length; ++i) {
            this.addVertex(`${vertices[i].id}`);
        }

        for (let i = 0; i < edges.length; ++i) {
            this.addEdge(edges[i].source, edges[i].target);
        }
    }
}

export default Graph;
