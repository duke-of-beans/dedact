"""
Database Loaders Module
Load processed data into PostgreSQL and Neo4j
"""

from pathlib import Path
from typing import List, Dict, Optional
import json


class PostgreSQLLoader:
    """Load data into PostgreSQL"""
    
    def __init__(self, connection_string: str):
        """
        Initialize PostgreSQL loader
        
        Args:
            connection_string: PostgreSQL connection string
        """
        self.connection_string = connection_string
        self.conn = None
    
    def connect(self):
        """Establish database connection"""
        try:
            import psycopg2
            self.conn = psycopg2.connect(self.connection_string)
        except ImportError:
            raise ImportError("psycopg2 not installed. Run: pip install psycopg2-binary")
    
    def load_documents(self, documents: List[Dict]) -> int:
        """Load documents into database"""
        if not self.conn:
            self.connect()
        
        cursor = self.conn.cursor()
        count = 0
        
        for doc in documents:
            cursor.execute("""
                INSERT INTO documents (id, path, hash, format, corpus)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, (doc['id'], doc['path'], doc['hash'], doc['format'], doc['corpus']))
            count += cursor.rowcount
        
        self.conn.commit()
        return count
    
    def load_redactions(self, redactions: List[Dict]) -> int:
        """Load redactions into database"""
        if not self.conn:
            self.connect()
        
        cursor = self.conn.cursor()
        count = 0
        
        for red in redactions:
            cursor.execute("""
                INSERT INTO redactions (id, document_id, page, bbox, type, confidence)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (red['id'], red['document_id'], red['page'], 
                  json.dumps(red['bbox']), red['type'], red['confidence']))
            count += cursor.rowcount
        
        self.conn.commit()
        return count
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()


class Neo4jLoader:
    """Load network graph into Neo4j"""
    
    def __init__(self, uri: str, user: str, password: str):
        """
        Initialize Neo4j loader
        
        Args:
            uri: Neo4j URI (e.g., bolt://localhost:7687)
            user: Username
            password: Password
        """
        self.uri = uri
        self.user = user
        self.password = password
        self.driver = None
    
    def connect(self):
        """Establish Neo4j connection"""
        try:
            from neo4j import GraphDatabase
            self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
        except ImportError:
            raise ImportError("neo4j not installed. Run: pip install neo4j")
    
    def load_graph(self, nodes: List[Dict], edges: List[Dict]) -> Dict[str, int]:
        """Load complete graph into Neo4j"""
        if not self.driver:
            self.connect()
        
        with self.driver.session() as session:
            # Create nodes
            node_count = session.execute_write(self._create_nodes, nodes)
            
            # Create relationships
            edge_count = session.execute_write(self._create_relationships, edges)
        
        return {'nodes': node_count, 'edges': edge_count}
    
    @staticmethod
    def _create_nodes(tx, nodes):
        """Create nodes in transaction"""
        query = """
        UNWIND $nodes AS node
        MERGE (n:Entity {id: node.id})
        SET n += node
        """
        result = tx.run(query, nodes=nodes)
        return result.consume().counters.nodes_created
    
    @staticmethod
    def _create_relationships(tx, edges):
        """Create relationships in transaction"""
        query = """
        UNWIND $edges AS edge
        MATCH (a:Entity {id: edge.from})
        MATCH (b:Entity {id: edge.to})
        MERGE (a)-[r:RELATED {type: edge.type}]->(b)
        SET r += edge
        """
        result = tx.run(query, edges=edges)
        return result.consume().counters.relationships_created
    
    def close(self):
        """Close Neo4j driver"""
        if self.driver:
            self.driver.close()
