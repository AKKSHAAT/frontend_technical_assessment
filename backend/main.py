from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

class NodeData(BaseModel):
    id: str
    type: str
    position: Dict[str, float] 
    data: Dict[str, Any]
    width: float
    height: float

class EdgeData(BaseModel):
    id: str
    source: str
    target: str
    type: str

class PipelineData(BaseModel):
    nodes: List[NodeData]
    edges: List[EdgeData]


# Function to build adjacency list
def adjacency_dist(nodes, edges):
    adj_list = {node.id: [] for node in nodes}
    for edge in edges:
        adj_list[edge.source].append(edge.target)
    return adj_list
# like this
# {
#   "A": ["B", "C"],
#   "B": ["C"],
#   "C": []
# }


# Function to check if the graph is a DAG
def is_dag(adj_list):
    visited = set()
    recursion_stack = set()

    def dfs(node):
        if node in recursion_stack:  # Cycle detected
            return False
        if node in visited:  # Already checked this node
            return True
        
        visited.add(node)
        recursion_stack.add(node)

        for neighbor in adj_list.get(node, []):
            if not dfs(neighbor):
                return False

        recursion_stack.remove(node)
        return True
    
    for node in adj_list:
        if node not in visited:
            if not dfs(node):
                return False
    return True


@app.get('/')
def read_root():
    return {'Ping': 'Pong'}

@app.post('/pipelines/parse')
def parse_pipeline(pipeline_data: PipelineData):
    nodes = pipeline_data.nodes
    edges = pipeline_data.edges
    
    num_nodes = len(nodes)
    num_edges = len(edges)
    
    adj_list = adjacency_dist(nodes, edges)
    dag_status = is_dag(adj_list)

    print(f" num_nodes: {num_nodes}\n num_edges: {num_edges}\n is_dag {dag_status}")

    return {
        'num_nodes': num_nodes,
        'num_edges': num_edges,
        'is_dag': dag_status
    }
    # uvicorn main:app --reload
