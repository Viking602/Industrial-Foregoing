import json,sys
from pathlib import Path
es=json.load(open(sys.argv[1]))
for e in es:
 if len(sys.argv)>2 and sys.argv[2] not in e['file']:continue
 if len(sys.argv)==2 and any(x in e['file'] for x in ['\\proxy\\client','\\entity\\client','\\plugin\\','\\ParticleVex.java','\\gui\\','\\ModuleTransportStorage.java','IndustrialForegoing.java']):continue
 lines=e['detail'].splitlines()
 print(Path(e['file']).name+':'+str(e['line'])+' '+e['message']+' | '+lines[1].strip()+' '+next((x.strip() for x in lines[2:] if 'symbol:' in x),''))
