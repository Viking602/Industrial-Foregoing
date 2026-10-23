from pathlib import Path
import json,re,sys,collections
group=collections.defaultdict(list)
for e in json.loads(Path(sys.argv[1]).read_text(encoding='utf-8')):group[e['file']].append(e)
for f,errors in group.items():
 p=Path(f);lines=p.read_text(encoding='utf-8').splitlines()
 for e in errors:
  m=re.search(r'symbol:\s+(variable|method) (\w+)',e['detail'])
  if not m or m[2] not in ['input','output','inputFluid','inputFluid1','inputFluid2','outputFluid','handItem']:continue
  kind,name=m.groups();n=e['line']-1
  if kind=='method':lines[n]=re.sub(r'\b'+name+r'\(\)',name,lines[n])
  else:
   # Only the identifier marked by javac, so local variables stay intact.
   detail=e['detail'].splitlines();code=detail[1];caret=detail[2].find('^')
   match=re.search(r'\b'+name+r'\b',code[caret:])
   if not match:continue
   start=caret+match.start();end=start+len(name)
   # Handle repeated errors on the same source line using the original receiver.
   prefix=re.search(r'(\w+\.)?'+name+'$',code[:end])[0]
   lines[n]=re.sub(re.escape(prefix)+r'\b(?!\()',prefix+'()',lines[n])
 p.write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n')
