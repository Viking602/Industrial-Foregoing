from pathlib import Path
import sys,re,collections,json
p=Path(sys.argv[1]); text=p.read_text(encoding='utf-8',errors='replace').split('FAILURE:')[0]
errors=[]
for block in re.split(r'(?=(?:D:\\.*?\.java):\d+: (?:错误|error):)',text):
    m=re.match(r'(D:\\.*?\.java):(\d+): (?:错误|error): ([^\n]+)',block)
    if m: errors.append({'file':m[1], 'line':int(m[2]), 'message':m[3], 'detail':block})
p.with_suffix('.errors.json').write_text(json.dumps(errors,ensure_ascii=False,indent=2),encoding='utf-8')
print('Errors:',len(errors))
if len(sys.argv)>2:
    selected=[e for e in errors if sys.argv[2] in e['file'] or sys.argv[2] in e['message']]
    for e in selected[:int(sys.argv[3]) if len(sys.argv)>3 else 30]: print(e['detail'])
else:
    print('Files:',collections.Counter(Path(e['file']).name for e in errors).most_common(30))
    print('Categories:',collections.Counter(e['message'] for e in errors).most_common(35))
    symbols=collections.Counter(re.search(r'符号:\s+([^\n]+)',e['detail'])[1] for e in errors if re.search(r'符号:\s+([^\n]+)',e['detail']))
    print('Symbols:',symbols.most_common(60))
