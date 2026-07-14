#!/usr/bin/env python
import argparse, json
RISK={'filesystem':'Can read or write local files','network':'Can contact external services','shell':'Can execute local commands','browser':'Can operate a browser session','database':'Can query or mutate data stores'}
def story(manifest):
 tools=manifest.get('tools',[]); lines=['# MCP Permission Story','']
 for t in tools:
  caps=t.get('permissions') or t.get('capabilities') or []
  if isinstance(caps,str): caps=[caps]
  risks=[RISK.get(c,c) for c in caps]
  level='high' if any(c in caps for c in ['shell','filesystem','database']) else ('medium' if caps else 'low')
  lines.append(f"- **{t.get('name','unnamed')}** ({level}): {t.get('description','No description')}")
  if risks: lines.append('  - Permissions: '+ '; '.join(risks))
  else: lines.append('  - Permissions: none declared')
 return '\n'.join(lines)
def main(argv=None):
 ap=argparse.ArgumentParser(description='Turn an MCP tool manifest into a human-readable permission story for reviewers.')
 ap.add_argument('manifest_json'); a=ap.parse_args(argv)
 print(story(json.load(open(a.manifest_json,encoding='utf-8'))))
if __name__=='__main__': main()
