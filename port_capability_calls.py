from pathlib import Path
import re
root=Path('.work/Industrial-Foregoing/src/main/java')
helper='com.buuz135.industrial.compat.MachineCapabilities'
for p in root.rglob('*.java'):
 if 'compat' in p.parts or p.name=='ModuleTool.java': continue
 s=p.read_text()
 # Exact capability calls only, including nested receivers and block position arguments.
 token='.getCapability('
 matches=list(re.finditer(re.escape(token)+r'Capabilities\.(FluidHandler|ItemHandler|EnergyStorage)\.(ITEM|BLOCK)',s))
 for m in reversed(matches):
  start=m.start()-1; depth=0
  while start>=0:
   c=s[start]
   if c in ')]': depth+=1
   elif c in '([':
    if depth==0: break
    depth-=1
   elif depth==0 and not(c.isalnum() or c in '._$'): break
   start-=1
  start+=1; receiver=s[start:m.start()]; i=m.end(); depth=1
  while i<len(s):
   if s[i]=='(': depth+=1
   elif s[i]==')':
    depth-=1
    if not depth: break
   i+=1
  args=s[m.end():i]
  method={'FluidHandler':'fluids','ItemHandler':'items','EnergyStorage':'energy'}[m[1]]
  s=s[:start]+helper+'.'+method+'('+receiver+args+')'+s[i+1:]
 if p.name in ['ConveyorExtractionUpgrade.java','ConveyorInsertionUpgrade.java']:
  s=s.replace('Capabilities.ItemHandler','Capabilities.Item').replace('Capabilities.FluidHandler','Capabilities.Fluid')
  s=s.replace('Capabilities.Item.ENTITY_AUTOMATION).ifPresent','Capabilities.Item.ENTITY_AUTOMATION).map('+helper+'::items).ifPresent')
  s=s.replace('Capabilities.Fluid.ENTITY).ifPresent','Capabilities.Fluid.ENTITY).map('+helper+'::fluids).ifPresent')
 p.write_text(s)
