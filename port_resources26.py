from pathlib import Path
import json,zipfile,collections
roots=[Path('.work/Industrial-Foregoing'),Path('.work/IndustrialForegoingExtraUpgrades')]
def write(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def ing(d):
 if isinstance(d,str):return d
 if isinstance(d,list):
  vals=[ing(v) for v in d]
  if all(isinstance(v,str) and not v.startswith('#') for v in vals):return vals
  return {'neoforge:type':'neoforge:compound','children':vals}
 if 'item' in d:return d['item']
 if 'tag' in d:return '#'+d['tag']
 return d

def condition(d):
 if isinstance(d,list):return [condition(x) for x in d]
 if not isinstance(d,dict):return d
 if d.get('type')=='neoforge:item_exists':return {'type':'neoforge:registered','value':d['item']}
 return {k:condition(v) for k,v in d.items()}
for root in roots:
 count=0
 for directory in ['main','generated']:
  res=root/f'src/{directory}/resources'
  for p in res.glob('data/*/recipe/**/*.json'):
   d=condition(json.loads(p.read_text(encoding='utf-8')));t=d['type']
   if 'key' in d:d['key']={k:ing(v) for k,v in d['key'].items()}
   for k in ['ingredients','inputs']:
    if k in d:d[k]=[ing(x) for x in d[k]]
   if 'ingredient' in d:d['ingredient']=ing(d['ingredient'])
   if 'catalyst' in d:d['catalyst']=ing(d['catalyst'])
   if t in ['industrialforegoing:crusher','industrialforegoing:fluid_extractor']:d['input']=ing(d['input'])
   if t=='industrialforegoing:crusher':d['output']=ing(d['output'])
   if t=='industrialforegoing:dissolution_chamber':
    d['input']=[ing(x) for x in d['input']]
    v=d['inputFluid'];d['inputFluid']={'ingredient':v.get('ingredient',v.get('fluid','#'+v.get('tag',''))),'amount':v['amount']}
   if t=='industrialforegoing:laser_drill_fluid':
    v=d['output'];d['output']={'ingredient':v.get('ingredient',v.get('fluid','#'+v.get('tag',''))),'amount':v['amount']}
   if t=='industrialforegoing:laser_drill_ore':
    v=d['output'];d['output']={'ingredient':v.get('ingredient',ing(v)),'count':v.get('count',1)}
   write(p,d);count+=1
  # Advance conditions use the same registered condition replacement, while item predicates stay item predicates.
  for p in res.glob('data/*/advancement/**/*.json'):
   d=json.loads(p.read_text());nd=condition(d)
   if nd!=d:write(p,nd)
  for p in res.glob('assets/*/models/item/**/*.json'):
   d=json.loads(p.read_text());ns=p.relative_to(res).parts[1];path=p.relative_to(res/f'assets/{ns}/models/item').with_suffix('').as_posix()
   model={'type':'minecraft:model','model':f'{ns}:item/{path}'}
   # Original tint indices are preserved; every material gets an explicit source.
   if ns=='industrialforegoing' and (path.startswith('infinity_') or path=='mob_imprisonment_tool'):
    model['tints']=[{'type':'industrialforegoing:machine','index':i} for i in range(4)]
   if d.get('loader')=='neoforge:fluid_container':
    fluid=d['fluid'].replace('industrialforegoing:ether','industrialforegoing:ether_gas') if d['fluid']=='industrialforegoing:ether' else d['fluid']
    model={'type':'neoforge:fluid_container','fluid':fluid,'textures':{'base':'minecraft:item/bucket','fluid':'neoforge:item/mask/bucket_fluid','cover':'neoforge:item/mask/bucket_cover'}}
    # The removed loader must not be parsed as a cuboid model.
    write(p,{'parent':'minecraft:item/generated','textures':{'layer0':'minecraft:item/bucket'}})
   if d.get('overrides'):
    props={next(iter(o['predicate'])) for o in d['overrides']};assert len(props)==1
    model={'type':'minecraft:range_dispatch','property':next(iter(props)),'fallback':model,'entries':[{'threshold':next(iter(o['predicate'].values())),'model':{'type':'minecraft:model','model':o['model']}} for o in d['overrides']]}
    d.pop('overrides');write(p,d)
   if path=='hydroponic_simulation_processor':model={'type':'industrialforegoing:hydroponic_processor'}
   write(res/f'assets/{ns}/items/{path}.json',{'model':model})
 # Same pack carries both data and assets, whose format versions differ.
 write(root/'src/main/resources/pack.mcmeta',{'pack':{'description':root.name+' for Minecraft 26.1.2','min_format':82,'max_format':101}})
 print(root.name,'recipes migrated',count)
# NeoForge built-in bucket mask names are checked from the actual runtime dependency below.
for p in Path('.work/Industrial-Foregoing/build/moddev/artifacts').glob('*.jar'):
 with zipfile.ZipFile(p) as z:
  if 'version.json' in z.namelist():print('GAME VERSION',json.loads(z.read('version.json')).get('pack_version'))
  masks=[n for n in z.namelist() if ('bucket' in n and 'mask' in n) or n.endswith('items/bucket.json')]
  if masks:print(p.name,masks)
