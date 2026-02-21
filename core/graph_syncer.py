import os
import logging
from neo4j import GraphDatabase

logger = logging.getLogger(__name__)

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://graph-db:7687")
NEO4J_USER = os.getenv("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

class GraphSyncer:
    def __init__(self):
        try:
            self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            self.driver = None

    def close(self):
        if self.driver:
            self.driver.close()

    def sync_entity(self, event_type: str, entity_type: str, entity_id: str, fields: dict):
        if not self.driver:
            logger.warning("Neo4j driver not initialized, skipping sync.")
            return

        logger.info(f"Syncing {entity_type} {entity_id} to Neo4j from event {event_type}")
        
        with self.driver.session() as session:
            if entity_type == "STORY":
                self._sync_story(session, entity_id, fields)
            elif entity_type == "EPIC":
                self._sync_epic(session, entity_id, fields)
            elif entity_type == "USER":
                self._sync_user(session, entity_id, fields)
            elif entity_type == "RISK":
                self._sync_risk(session, entity_id, fields)
            else:
                logger.warning(f"Unsupported entity type for graph sync: {entity_type}")

    def _sync_story(self, session, entity_id, fields):
        # Create or retrieve the Story node
        query = """
        MERGE (s:Task {id: $id})
        SET s.title = coalesce($title, s.title),
            s.status = coalesce($status, s.status),
            s.priority = coalesce($priority, s.priority),
            s.points = coalesce($points, s.points)
        """
        session.run(query, id=entity_id, title=fields.get("title"), status=fields.get("status"),
                    priority=fields.get("priority"), points=fields.get("points"))
        
        # Relationships: ASSIGNMENT
        if fields.get("assignee_id"):
            session.run("""
            MATCH (s:Task {id: $story_id})
            MERGE (u:User {id: $assignee_id})
            MERGE (u)-[:ASSIGNED_TO]->(s)
            """, story_id=entity_id, assignee_id=fields.get("assignee_id"))
            
        # Relationships: PART_OF
        if fields.get("epic_id"):
            session.run("""
            MATCH (s:Task {id: $story_id})
            MERGE (e:Epic {id: $epic_id})
            MERGE (s)-[:PART_OF]->(e)
            """, story_id=entity_id, epic_id=fields.get("epic_id"))

    def _sync_epic(self, session, entity_id, fields):
        query = """
        MERGE (e:Epic {id: $id})
        SET e.title = coalesce($title, e.title),
            e.status = coalesce($status, e.status),
            e.rag_status = coalesce($rag_status, e.rag_status)
        """
        session.run(query, id=entity_id, title=fields.get("title"), status=fields.get("status"), rag_status=fields.get("rag_status"))

    def _sync_user(self, session, entity_id, fields):
        query = """
        MERGE (u:User {id: $id})
        SET u.name = coalesce($name, u.name),
            u.email = coalesce($email, u.email),
            u.role = coalesce($role, u.role)
        """
        session.run(query, id=entity_id, name=fields.get("name"), email=fields.get("email"), role=fields.get("role"))

    def _sync_risk(self, session, entity_id, fields):
        query = """
        MERGE (r:Risk {id: $id})
        SET r.severity = coalesce($severity, r.severity),
            r.status = coalesce($status, r.status)
        """
        session.run(query, id=entity_id, severity=fields.get("severity"), status=fields.get("status"))
        
        if fields.get("story_id"):
            session.run("""
            MATCH (r:Risk {id: $risk_id})
            MERGE (s:Task {id: $story_id})
            MERGE (r)-[:IMPACTS]->(s)
            """, risk_id=entity_id, story_id=fields.get("story_id"))
