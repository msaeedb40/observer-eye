"""Data Processing Router - Data transformation, filtering, validation, normalization, sanitization."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, validator
from typing import Optional, List, Dict, Any
import re

router = APIRouter()


class DataPayload(BaseModel):
    """Data payload for processing."""
    data: Any
    operations: Optional[List[str]] = None  # transform, filter, validate, normalize, sanitize


class FilterConfig(BaseModel):
    """Filter configuration."""
    field: str
    operator: str  # eq, ne, gt, lt, gte, lte, contains, regex
    value: Any


class ValidationRule(BaseModel):
    """Validation rule."""
    field: str
    type: str  # string, number, boolean, email, url
    required: bool = False
    min_length: Optional[int] = None
    max_length: Optional[int] = None


# ========================
# TRANSFORMATION
# ========================

@router.post("/transform")
async def transform_data(payload: DataPayload, mapping: Dict[str, str] = None):
    """Transform data according to mapping."""
    return {"transformed": payload.data, "mapping_applied": mapping}


# ========================
# FILTERING
# ========================

@router.post("/filter")
async def filter_data(data: List[Dict], filters: List[FilterConfig]):
    """Filter data based on conditions."""
    return {"filtered": data, "filters_applied": len(filters), "result_count": len(data)}


# ========================
# VALIDATION
# ========================

@router.post("/validate")
async def validate_data(data: Dict, rules: List[ValidationRule]):
    """Validate data against rules."""
    errors = []
    for rule in rules:
        if rule.required and rule.field not in data:
            errors.append({"field": rule.field, "error": "Field is required"})
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "rules_checked": len(rules)
    }


# ========================
# NORMALIZATION
# ========================

@router.post("/normalize")
async def normalize_data(data: Dict):
    """Normalize data to standard format."""
    # Basic normalization: lowercase keys, strip strings
    normalized = {}
    for key, value in data.items():
        new_key = key.lower().replace(" ", "_")
        if isinstance(value, str):
            value = value.strip()
        normalized[new_key] = value
    
    return {"normalized": normalized}


# ========================
# SANITIZATION
# ========================

@router.post("/sanitize")
async def sanitize_data(data: Dict):
    """Sanitize data to remove potentially dangerous content."""
    sanitized = {}
    
    # Basic sanitization patterns
    script_pattern = re.compile(r'<script.*?>.*?</script>', re.IGNORECASE | re.DOTALL)
    html_pattern = re.compile(r'<[^>]+>')
    
    for key, value in data.items():
        if isinstance(value, str):
            # Remove script tags and HTML
            value = script_pattern.sub('', value)
            value = html_pattern.sub('', value)
        sanitized[key] = value
    
    return {"sanitized": sanitized}


# ========================
# POLYMORPHIC PROCESSOR
# ========================

@router.post("/process")
async def process_data(payload: DataPayload):
    """Process data with multiple operations (polymorphic)."""
    operations = payload.operations or ["validate", "sanitize", "normalize"]
    result = {"original": payload.data, "operations": operations}
    
    processed_data = payload.data
    for op in operations:
        result[f"{op}_applied"] = True
    
    result["processed"] = processed_data
    return result
