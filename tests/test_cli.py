import unittest, tempfile, json, subprocess, sys, os
class T(unittest.TestCase):
 def test_story(self):
  p=tempfile.mktemp(); json.dump({'tools':[{'name':'run','description':'run command','permissions':['shell']}]},open(p,'w'))
  out=subprocess.check_output([sys.executable,'mcp-server-permission-story-generator-20260714.py',p],text=True)
  self.assertIn('Can execute local commands',out); self.assertIn('high',out)
