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
    """Transform data according to mapping (renaming keys)."""
    if not mapping or not isinstance(payload.data, dict):
        return {"transformed": payload.data, "mapping_applied": False}
    
    transformed = {}
    for old_key, value in payload.data.items():
        new_key = mapping.get(old_key, old_key)
        transformed[new_key] = value
        
    return {"transformed": transformed, "mapping_applied": True}


# ========================
# FILTERING
# ========================

def _apply_filter(item: Dict, f: FilterConfig) -> bool:
    """Helper to apply a single filter to an item."""
    val = item.get(f.field)
    if val is None:
        return False
        
    op = f.operator.lower()
    if op == 'eq': return val == f.value
    if op == 'ne': return val != f.value
    if op == 'gt': return val > f.value
    if op == 'lt': return val < f.value
    if op == 'gte': return val >= f.value
    if op == 'lte': return val <= f.value
    if op == 'contains': return f.value in str(val)
    if op == 'regex': return bool(re.search(str(f.value), str(val)))
    
    return True


@router.post("/filter")
async def filter_data(data: List[Dict], filters: List[FilterConfig]):
    """Filter data based on provided conditions."""
    filtered = data
    for f in filters:
        filtered = [item for item in filtered if _apply_filter(item, f)]
        
    return {
        "filtered": filtered,
        "filters_applied": len(filters),
        "result_count": len(filtered),
        "original_count": len(data)
    }


# ========================
# VALIDATION
# =VERIFICATION_PLAN=======

@router.post("/validate")
async def validate_data(data: Dict, rules: List[ValidationRule]):
    """Validate data against rules."""
    errors = []
    for rule in rules:
        if rule.required and rule.field not in data:
            errors.append({"field": rule.field, "error": "Field is required"})
            continue
            
        if rule.field in data:
            val = data[rule.field]
            # Type checking
            if rule.type == 'string' and not isinstance(val, str):
                errors.append({"field": rule.field, "error": "Must be a string"})
            elif rule.type == 'number' and not isinstance(val, (int, float)):
                errors.append({"field": rule.field, "error": "Must be a number"})
            elif rule.type == 'boolean' and not isinstance(val, bool):
                errors.append({"field": rule.field, "error": "Must be a boolean"})
                
            # Length checking
            if isinstance(val, str):
                if rule.min_length and len(val) < rule.min_length:
                    errors.append({"field": rule.field, "error": f"Min length {rule.min_length}"})
                if rule.max_length and len(val) > rule.max_length:
                    errors.append({"field": rule.field, "error": f"Max length {rule.max_length}"})
    
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
    """Normalize data to standard format (lowercase keys, stripped strings)."""
    normalized = {}
    for key, value in data.items():
        new_key = key.lower().replace(" ", "_").strip()
        if isinstance(value, str):
            value = value.strip()
        elif isinstance(value, dict):
            # Recursively normalize nested dicts
            value = (await normalize_data(value))["normalized"]
        normalized[new_key] = value
    
    return {"normalized": normalized}


# ========================
# SANITIZATION
# ========================

@router.post("/sanitize")
async def sanitize_data(data: Dict):
    """Sanitize data to remove scripts and HTML tags."""
    sanitized = {}
    script_pattern = re.compile(r'<script.*?>.*?</script>', re.IGNORECASE | re.DOTALL)
    html_pattern = re.compile(r'<[^>]+>')
    
    for key, value in data.items():
        if isinstance(value, str):
            value = script_pattern.sub('', value)
            value = html_pattern.sub('', value)
        elif isinstance(value, dict):
            value = (await sanitize_data(value))["sanitized"]
        sanitized[key] = value
        
    return {"sanitized": sanitized}


# ========================
# POLYMORPHIC PROCESSOR
# ========================

@router.post("/process")
async def process_data(payload: DataPayload):
    """Process data with sequential operations."""
    operations = payload.operations or ["sanitize", "normalize"]
    current_data = payload.data
    
    applied = []
    for op in operations:
        if op == "normalize" and isinstance(current_data, dict):
            current_data = (await normalize_data(current_data))["normalized"]
            applied.append(op)
        elif op == "sanitize" and isinstance(current_data, dict):
            current_data = (await sanitize_data(current_data))["sanitized"]
            applied.append(op)
            
    return {
        "processed": current_data,
        "operations_requested": operations,
        "operations_applied": applied
    }
