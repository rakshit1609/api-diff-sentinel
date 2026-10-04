import json
from typing import Dict, Any, List

def compare_specs(old_spec: Dict[str, Any], new_spec: Dict[str, Any]) -> Dict[str, Any]:
    breaking = []
    non_breaking = []
    
    old_paths = old_spec.get("paths", {})
    new_paths = new_spec.get("paths", {})
    
    # 1. Check for removed endpoints
    for path, methods in old_paths.items():
        if path not in new_paths:
            breaking.append(f"❌ Removed endpoint: `{path}`")
            continue
        for m in methods:
            if m.lower() not in ["get", "post", "put", "delete", "patch"]:
                continue
            if m not in new_paths[path]:
                breaking.append(f"❌ Removed method: `{m.upper()} {path}`")
                
    # 2. Check for added endpoints & methods
    for path, methods in new_paths.items():
        if path not in old_paths:
            non_breaking.append(f"✨ Added new endpoint: `{path}`")
            continue
        for m in methods:
            if m.lower() not in ["get", "post", "put", "delete", "patch"]:
                continue
            if m not in old_paths[path]:
                non_breaking.append(f"✨ Added new method: `{m.upper()} {path}`")
            else:
                # Compare parameters
                old_params = {p.get("name"): p for p in old_paths[path][m].get("parameters", [])}
                new_params = {p.get("name"): p for p in new_paths[path][m].get("parameters", [])}
                
                # Check for removed parameters
                for pname in old_params:
                    if pname not in new_params:
                        breaking.append(f"⚠️ Removed parameter `{pname}` from `{m.upper()} {path}`")
                        
                # Check for new required parameters
                for pname, pobj in new_params.items():
                    if pname not in old_params and pobj.get("required"):
                        breaking.append(f"❌ Added new required parameter `{pname}` to `{m.upper()} {path}` (Breaking)")
                    elif pname not in old_params:
                        non_breaking.append(f"✨ Added optional parameter `{pname}` to `{m.upper()} {path}`")
                        
    return {
        "is_breaking": len(breaking) > 0,
        "breaking_changes_count": len(breaking),
        "non_breaking_changes_count": len(non_breaking),
        "breaking": breaking,
        "non_breaking": non_breaking
    }
