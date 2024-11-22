from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow only your frontend's origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

class Node(BaseModel):
    id: str
    type: str

class Edge(BaseModel):
    source: str
    target: str

class Pipeline(BaseModel):
    nodes: List[Node]
    edges: List[Edge]

def is_dag(nodes: List[Node], edges: List[Edge]) -> bool:
    graph = {node.id: [] for node in nodes}
    for edge in edges:
        graph[edge.source].append(edge.target)

    visited = set()
    stack = set()

    def dfs(node):
        if node in stack:
            return False
        if node in visited:
            return True

        visited.add(node)
        stack.add(node)
        for neighbor in graph[node]:
            if not dfs(neighbor):
                return False
        stack.remove(node)
        return True

    return all(dfs(node.id) for node in nodes if node.id not in visited)

@app.post("/pipelines/parse")
def parse_pipeline(pipeline: Pipeline):
    nodes = pipeline.nodes
    edges = pipeline.edges
    num_nodes = len(nodes)
    num_edges = len(edges)
    dag_status = is_dag(nodes, edges)

    return {"num_nodes": num_nodes, "num_edges": num_edges, "is_dag": dag_status}

@app.get("/")
def read_root():
    return {"message": "Backend is working"}
