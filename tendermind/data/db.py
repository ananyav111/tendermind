import sqlite3
import json
from typing import List, Optional, Dict, Any
from tendermind.models.tender import Tender, TenderRequirement, Corrigendum, RequirementCategory
from tendermind.models.company import CompanyProfile, BusinessCredential, BusinessDocument, DocumentStatus
from tendermind.models.bid import BidPackage, BidChecklistItem, GeneratedProposalSection, ChecklistItemStatus
from tendermind.models.mcp_types import AgentTraceEntry
from tendermind.data.sample_data import SAMPLE_COMPANY, SAMPLE_TENDERS

class TenderMindDB:
    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_tables()
        self._seed_data()
        self.traces: List[AgentTraceEntry] = []

    def _init_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS companies (
                company_id TEXT PRIMARY KEY,
                data TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tenders (
                tender_id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                department TEXT,
                category TEXT,
                location TEXT,
                estimated_value_inr REAL,
                submission_deadline TEXT,
                status TEXT,
                suitability_score INTEGER,
                data TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bid_packages (
                package_id TEXT PRIMARY KEY,
                tender_id TEXT NOT NULL,
                company_id TEXT NOT NULL,
                data TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                user_id TEXT,
                action TEXT NOT NULL,
                details TEXT
            )
        """)
        self.conn.commit()

    def _seed_data(self):
        # Insert company
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO companies (company_id, data) VALUES (?, ?)",
            (SAMPLE_COMPANY.company_id, SAMPLE_COMPANY.model_dump_json())
        )
        # Insert sample tenders
        for t in SAMPLE_TENDERS:
            cursor.execute("""
                INSERT OR REPLACE INTO tenders 
                (tender_id, title, department, category, location, estimated_value_inr, submission_deadline, status, suitability_score, data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                t.tender_id, t.title, t.department, t.category, t.location,
                t.estimated_value_inr, t.submission_deadline, t.status, t.suitability_score,
                t.model_dump_json()
            ))
        self.conn.commit()

    def get_company(self, company_id: str = "comp_nexus_01") -> Optional[CompanyProfile]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT data FROM companies WHERE company_id = ?", (company_id,))
        row = cursor.fetchone()
        if row:
            return CompanyProfile.model_validate_json(row["data"])
        return None

    def update_company(self, company: CompanyProfile):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO companies (company_id, data) VALUES (?, ?)",
            (company.company_id, company.model_dump_json())
        )
        self.conn.commit()

    def get_all_tenders(self) -> List[Tender]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT data FROM tenders ORDER BY suitability_score DESC")
        rows = cursor.fetchall()
        return [Tender.model_validate_json(r["data"]) for r in rows]

    def get_tender(self, tender_id: str) -> Optional[Tender]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT data FROM tenders WHERE tender_id = ?", (tender_id,))
        row = cursor.fetchone()
        if row:
            return Tender.model_validate_json(row["data"])
        return None

    def save_tender(self, tender: Tender):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO tenders 
            (tender_id, title, department, category, location, estimated_value_inr, submission_deadline, status, suitability_score, data)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            tender.tender_id, tender.title, tender.department, tender.category, tender.location,
            tender.estimated_value_inr, tender.submission_deadline, tender.status, tender.suitability_score,
            tender.model_dump_json()
        ))
        self.conn.commit()

    def search_tenders(self, query: Optional[str] = None, category: Optional[str] = None,
                       location: Optional[str] = None, max_value: Optional[float] = None) -> List[Tender]:
        all_tenders = self.get_all_tenders()
        results = []
        for t in all_tenders:
            if query and not (query.lower() in t.title.lower() or query.lower() in t.department.lower() or query.lower() in t.summary.lower()):
                continue
            if category and category.lower() != "all" and category.lower() not in t.category.lower():
                continue
            if location and location.lower() not in t.location.lower() and "pan-india" not in t.location.lower():
                continue
            if max_value and t.estimated_value_inr > max_value:
                continue
            results.append(t)
        return results

    def get_bid_package(self, package_id: str) -> Optional[BidPackage]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT data FROM bid_packages WHERE package_id = ?", (package_id,))
        row = cursor.fetchone()
        if row:
            return BidPackage.model_validate_json(row["data"])
        return None

    def get_bid_package_by_tender(self, tender_id: str, company_id: str) -> Optional[BidPackage]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT data FROM bid_packages WHERE tender_id = ? AND company_id = ?", (tender_id, company_id))
        row = cursor.fetchone()
        if row:
            return BidPackage.model_validate_json(row["data"])
        return None

    def save_bid_package(self, pkg: BidPackage):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO bid_packages (package_id, tender_id, company_id, data) VALUES (?, ?, ?, ?)",
            (pkg.package_id, pkg.tender_id, pkg.company_id, pkg.model_dump_json())
        )
        self.conn.commit()

    def add_trace(self, trace: AgentTraceEntry):
        self.traces.append(trace)

    def get_traces(self) -> List[AgentTraceEntry]:
        return list(reversed(self.traces))

    def log_audit(self, user_id: str, action: str, details: Dict[str, Any]):
        cursor = self.conn.cursor()
        from datetime import datetime
        now = datetime.now().isoformat()
        cursor.execute(
            "INSERT INTO audit_logs (timestamp, user_id, action, details) VALUES (?, ?, ?, ?)",
            (now, user_id, action, json.dumps(details))
        )
        self.conn.commit()

# Global database singleton
db = TenderMindDB()
