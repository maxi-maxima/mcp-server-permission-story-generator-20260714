# mcp-server-permission-story-generator-20260714

Turns MCP tool manifests into plain-language permission stories for humans approving agent access.

## Pain point
Permission prompts and tool manifests are often too technical; reviewers miss what a tool can really do.

## Why now
MCP adoption is accelerating, and safer onboarding needs human-readable consent summaries.

## Install / run
No third-party packages are required. Python 3.10+ is enough.

```bash
python mcp-server-permission-story-generator-20260714.py --help
python mcp-server-permission-story-generator-20260714.py examples/mcp-manifest.json
```

## Example
```bash
python mcp-server-permission-story-generator-20260714.py examples/mcp-manifest.json
```

## Self-check
```bash
python -m unittest discover -s tests -v
```

## Roadmap
- Support live MCP introspection
- Diff two permission stories
- Add localized templates

## License
MIT
