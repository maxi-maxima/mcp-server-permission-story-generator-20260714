# mcp-server-permission-story-generator-20260714

把 MCP 工具清单转换成人类能看懂的权限说明，帮助审批 agent 访问。

## 解决的痛点
权限提示和 tool manifest 往往太技术化，审批者看不出工具真实能力。

## 为什么现在值得做
MCP 正在加速普及，安全接入需要更易懂的授权说明。

## 安装 / 运行
不需要第三方依赖，Python 3.10+ 即可。

```bash
python mcp-server-permission-story-generator-20260714.py --help
python mcp-server-permission-story-generator-20260714.py examples/mcp-manifest.json
```

## 示例
```bash
python mcp-server-permission-story-generator-20260714.py examples/mcp-manifest.json
python mcp-server-permission-story-generator-20260714.py examples/mcp-manifest.json --min-level medium
python mcp-server-permission-story-generator-20260714.py examples/mcp-manifest.json --format json-summary
```

`--min-level` 可只输出中/高风险工具，方便快速审批；`--format json-summary` 会输出按风险等级和权限聚合的 JSON，便于仪表盘或 CI 检查。
工具现在同时支持 `permissions` 和 MCP 常见的 `capabilities` 数组。

## 自检
```bash
python -m unittest discover -s tests -v
```

## 路线图
- 支持实时 MCP introspection
- 对比两份权限故事
- 增加多语言模板

## License
MIT
