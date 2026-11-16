from datetime import UTC, datetime
from enum import Enum
from uuid import UUID, uuid4

from sqlalchemy import BigInteger, CheckConstraint, Null
from sqlmodel import Field, SQLModel


class ScanStatus(str, Enum):
    Pending = "pending"
    Processing = "processing"
    Completed = "completed"
    Failed = "failed"


class ScanJobStatus(str, Enum):
    Queued = "queued"
    Running = "running"
    Done = "done"
    Failed = "failed"


class DocumentStatus(str, Enum):
    Uploaded = "uploaded"
    Scanned = "scanned"
    Redacted = "redacted"


class PiiValidator(str, Enum):
    Regex = "regex"
    Ocr = "ocr"
    Ner = "ner"


class PiiSeverity(str, Enum):
    Low = "low"
    Medium = "medium"
    High = "high"


class DetectionAction(str, Enum):
    Redact = "redact"
    Ignore = "ignore"
    Pending = "pending"


class RedactionMode(str, Enum):
    Blackout = "blackout"
    Mask = "mask"
    Remove = "remove"


class Scans(SQLModel, table=True):
    id: UUID = Field(primary_key=True, default_factory=uuid4)
    user_id: UUID = Field(primary_key=True, foreign_key="user.id")
    status: ScanStatus | None = ScanStatus.Pending
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class ScanResults(SQLModel, table=True):
    id: UUID = Field(primary_key=True, default_factory=uuid4)
    user_id: UUID = Field(primary_key=True, foreign_key="user.id")
    pii_count: int = Field(
        default=0, sa_column_args=[CheckConstraint("pii_count >= 0")]
    )
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class Documents(SQLModel, table=True):
    id: UUID = Field(primary_key=True, default_factory=uuid4)
    user_id: UUID = Field(primary_key=True, foreign_key="user.id")
    filename: str
    mime_type: str
    size_bytes: int = Field(
        sa_column_args=[CheckConstraint("size_bytes >= 0")], sa_type=BigInteger
    )
    sha256: str = Field(
        sa_column_args=[CheckConstraint("(length(sha256) = 64)")], sa_type=BigInteger
    )
    storage_key: str | None = None
    status: DocumentStatus | None = DocumentStatus.Uploaded
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column_kwargs={"onupdate": lambda: datetime.now(UTC)},
    )


class PiiTypes(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    code: str = Field(unique=True)
    text: str
    name: str
    validator: PiiValidator | None = PiiValidator.Regex
    severity: PiiSeverity | None = PiiSeverity.Medium
    enabled: bool | None = True


class ScanPolicies(SQLModel, table=True):
    id: UUID = Field(primary_key=True, default_factory=uuid4)
    user_id: UUID = Field(primary_key=True, foreign_key="user.id")
    name: str = Field(sa_column_args=[CheckConstraint("(length(name)>0)")])
    min_confidence: float | None = Field(
        default=0.7,
        sa_column_args=[CheckConstraint("min_confidence >=0 and min_confidence <=1 ")],
    )


class PolicyPiiTypes(SQLModel, table=True):
    id: UUID = Field(foreign_key="ScanPolicies.id")
    pii_type_id: UUID = Field(foreign_key="PiiTypes.id")


class ScanJobs(SQLModel, table=True):
    id: UUID = Field(primary_key=True, default_factory=uuid4)
    document_id: UUID = Field(foreign_key="Documents.id")
    policy_id: UUID = Field(foreign_key="ScanPolicies.id")
    status: ScanJobStatus | Null = ScanJobStatus.Queued
    pii_count: int = Field(
        default=0, sa_column_args=[CheckConstraint("pii_count >= 0")]
    )
    started_at: datetime | None = None
    finished_at: datetime | None = None
    error: str | None = None


class Detections(SQLModel, table=True):
    id: UUID = Field(primary_key=True, default_factory=uuid4)
    scan_job_id: UUID = Field(foreign_key="ScanJobs.id")
    pii_type_id: int = Field(foreign_key="PiiTypes.id")
    page_no: int = Field(default=Null, sa_column_args=[CheckConstraint("page_no >= 1")])
    bbox: dict[str, int] | None = None
    masked_value: str | None = None
    value_hash: str | None = None
    confidence: float | None = Field(
        sa_column_args=[CheckConstraint("min_confidence >=0 and min_confidence <=1 ")],
    )
    source: PiiValidator | None = PiiValidator.Regex
    action: DetectionAction | None = DetectionAction.Pending


class Redactions(SQLModel, table=True):
    id: UUID = Field(primary_key=True, default_factory=uuid4)
    scan_job_id: UUID = Field(foreign_key="ScanJobs.id")
    mode: RedactionMode
    output_storage_key: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class AuditLogs(SQLModel, table=True):
    id: UUID = Field(primary_key=True, default_factory=uuid4)
    user_id: UUID = Field(primary_key=True, foreign_key="user.id")
    action: str | None = None
    entity: str | None = None
    entity_id: UUID | None = None
    ip: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
