"""
Database management for storing compliance assessments
Uses SQLite for simplicity and portability
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

DATABASE_PATH = Path(__file__).parent / "compliance_assessments.db"


class AssessmentDB:
    """Manages storage and retrieval of compliance assessments"""

    def __init__(self, db_path: str = None):
        self.db_path = db_path or str(DATABASE_PATH)
        self._initialize_db()

    def _initialize_db(self):
        """Create the assessments table if it doesn't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS assessments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                amount REAL NOT NULL,
                currency TEXT DEFAULT 'USD',
                source_country TEXT NOT NULL,
                destination_country TEXT NOT NULL,
                purpose TEXT NOT NULL,
                counterparty_type TEXT NOT NULL,
                history_signals TEXT,
                risk_score INTEGER NOT NULL,
                risk_level TEXT NOT NULL,
                triggered_rules TEXT,
                rationale TEXT,
                checklist_items TEXT,
                ai_insights TEXT,
                full_response TEXT NOT NULL
            )
        """)

        conn.commit()
        conn.close()

    def save_assessment(
        self,
        transaction_data: Dict,
        assessment_result: Dict
    ) -> int:
        """
        Save a compliance assessment to the database
        
        Args:
            transaction_data: Input transaction details
            assessment_result: Risk assessment result from ComplianceEngine
            
        Returns:
            ID of the saved assessment
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Prepare data
        timestamp = datetime.utcnow().isoformat()
        
        cursor.execute("""
            INSERT INTO assessments (
                timestamp, amount, currency, source_country, destination_country,
                purpose, counterparty_type, history_signals, risk_score, risk_level,
                triggered_rules, rationale, checklist_items, ai_insights, full_response
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            timestamp,
            transaction_data.get('amount'),
            transaction_data.get('currency', 'USD'),
            transaction_data.get('source_country'),
            transaction_data.get('destination_country'),
            transaction_data.get('purpose'),
            transaction_data.get('counterparty_type'),
            transaction_data.get('history_signals', ''),
            assessment_result.get('risk_score'),
            assessment_result.get('risk_level'),
            json.dumps(assessment_result.get('triggered_rules', [])),
            assessment_result.get('rationale'),
            json.dumps(assessment_result.get('checklist_items', [])),
            json.dumps(assessment_result.get('ai_insights')) if assessment_result.get('ai_insights') else None,
            json.dumps(assessment_result)
        ))

        assessment_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return assessment_id

    def get_all_assessments(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """
        Retrieve all assessments from the database
        
        Args:
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of assessment dictionaries
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM assessments
            ORDER BY timestamp DESC
            LIMIT ? OFFSET ?
        """, (limit, offset))

        rows = cursor.fetchall()
        conn.close()

        assessments = []
        for row in rows:
            assessment = dict(row)
            # Parse JSON fields
            assessment['triggered_rules'] = json.loads(assessment['triggered_rules'])
            assessment['checklist_items'] = json.loads(assessment['checklist_items'])
            if assessment['ai_insights']:
                assessment['ai_insights'] = json.loads(assessment['ai_insights'])
            assessment['full_response'] = json.loads(assessment['full_response'])
            assessments.append(assessment)

        return assessments

    def get_assessment_by_id(self, assessment_id: int) -> Optional[Dict]:
        """
        Retrieve a single assessment by ID
        
        Args:
            assessment_id: ID of the assessment
            
        Returns:
            Assessment dictionary or None if not found
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM assessments WHERE id = ?", (assessment_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        assessment = dict(row)
        assessment['triggered_rules'] = json.loads(assessment['triggered_rules'])
        assessment['checklist_items'] = json.loads(assessment['checklist_items'])
        if assessment['ai_insights']:
            assessment['ai_insights'] = json.loads(assessment['ai_insights'])
        assessment['full_response'] = json.loads(assessment['full_response'])

        return assessment

    def get_statistics(self) -> Dict:
        """Get summary statistics of assessments"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Total assessments
        cursor.execute("SELECT COUNT(*) FROM assessments")
        total = cursor.fetchone()[0]

        # By risk level
        cursor.execute("""
            SELECT risk_level, COUNT(*) as count
            FROM assessments
            GROUP BY risk_level
        """)
        risk_breakdown = {row[0]: row[1] for row in cursor.fetchall()}

        # Average risk score
        cursor.execute("SELECT AVG(risk_score) FROM assessments")
        avg_score = cursor.fetchone()[0] or 0

        conn.close()

        return {
            'total_assessments': total,
            'risk_breakdown': risk_breakdown,
            'average_risk_score': round(avg_score, 2)
        }

    def clear_all(self):
        """Clear all assessments from database (for testing)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM assessments")
        conn.commit()
        conn.close()

