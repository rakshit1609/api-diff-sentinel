import argparse
import json
from pathlib import Path
from .differ import compare_specs

def main():
    parser = argparse.ArgumentParser(description="API-Diff-Sentinel: Detect API breaking changes between OpenAPI specifications.")
    parser.add_argument("old_spec", help="Path to base/old openapi.json")
    parser.add_argument("new_spec", help="Path to head/new openapi.json")
    parser.add_argument("--json", action="store_true", help="Output JSON summary")
    
    args = parser.parse_args()
    old_data = json.loads(Path(args.old_spec).read_text(encoding="utf-8"))
    new_data = json.loads(Path(args.new_spec).read_text(encoding="utf-8"))
    
    diff = compare_specs(old_data, new_data)
    
    if args.json:
        print(json.dumps(diff, indent=2))
        return
        
    print("🔍 API-Diff-Sentinel Audit Report:")
    print(f"• Verdict: {'🚨 BREAKING CHANGES DETECTED' if diff['is_breaking'] else '✅ COMPATIBLE'}")
    print(f"• Breaking Changes:     {diff['breaking_changes_count']}")
    print(f"• Non-Breaking Changes: {diff['non_breaking_changes_count']}")
    
    if diff['breaking']:
        print("\n🚨 Breaking Changes:")
        for b in diff['breaking']:
            print(f"  {b}")
            
    if diff['non_breaking']:
        print("\n✨ Additions & Enhancements:")
        for nb in diff['non_breaking']:
            print(f"  {nb}")

if __name__ == "__main__":
    main()
