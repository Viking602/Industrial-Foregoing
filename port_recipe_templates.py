from pathlib import Path
import re
roots=[Path(__file__).parent/'src/main/java',Path(__file__).parent.parent/'IndustrialForegoingExtraUpgrades/src/main/java']
for root in roots:
 for p in root.rglob('*Recipe.java'):
  if '/recipe/' not in p.as_posix() or '/provider/' in p.as_posix(): continue
  s=p.read_text(encoding='utf-8')
  fields=re.findall(r'public (?:final )?((?:Optional<)?(?:ItemStack|FluidStack)>?) (\w+);',s)
  if not fields or 'CODEC' not in s:continue
  cls=p.stem
  ctor=re.search(r'public '+cls+r'\(([^)]*)\)\s*\{([^{}]*)\}',s)
  # Skip empty constructor when it precedes the codec constructor.
  if ctor and not ctor.group(1):ctor=re.search(r'public '+cls+r'\(([^)]+)\)\s*\{([^{}]*)\}',s)
  assert ctor,(p,'ctor')
  params=ctor.group(1);body=ctor.group(2)
  templateparams=re.sub(r'\b(ItemStack|FluidStack)\b',r'\1Template',params)
  args=[part.strip().split()[-1] for part in params.split(',')]
  factory='('+', '.join(args)+') -> new '+cls+'('+', '.join(args)+', true)'
  s=s.replace(cls+'::new',factory)
  s=s.replace('ItemStack.CODEC','ItemStackTemplate.CODEC').replace('FluidStack.CODEC','FluidStackTemplate.CODEC')
  s=s.replace('import net.minecraft.world.item.ItemStack;', 'import net.minecraft.world.item.ItemStack;\nimport net.minecraft.world.item.ItemStackTemplate;')
  s=s.replace('import net.neoforged.neoforge.fluids.FluidStack;', 'import net.neoforged.neoforge.fluids.FluidStack;\nimport net.neoforged.neoforge.fluids.FluidStackTemplate;')
  nativebody=body
  for typ,name in fields:
   base='FluidStack' if 'FluidStack' in typ else 'ItemStack'
   templ=typ.replace(base,base+'Template')
   s=re.sub(r'public (?:final )?'+re.escape(typ)+r' '+name+r';', 'private '+templ+' '+name+'Template;',s)
   # Codec reads templates; regular callers instantiate only after component binding.
   s=s.replace('o.'+name+';', 'o.'+name+'Template;').replace('o.'+name+')','o.'+name+'Template)')
   original='this.'+name+' = '+name+';'
   convert=name+'.map('+base+'Template::fromNonEmptyStack)' if typ.startswith('Optional') else base+'Template.fromNonEmptyStack('+name+')'
   s=s.replace(original,'this.'+name+'Template = '+convert+';')
   nativebody=nativebody.replace(original,'this.'+name+'Template = '+name+';')
   value=name+'Template.map('+base+'Template::create)' if typ.startswith('Optional') else name+'Template.create()'
   s=s[:-2]+'\n    public '+typ+' '+name+'() { return '+value+'; }\n}\n' if s.endswith('}\n') else s
  s=s.rstrip()[:-1]+'\n    private '+cls+'('+templateparams+', boolean templates) {'+nativebody+'    }\n}\n'
  p.write_text(s,encoding='utf-8',newline='\n')
  print(cls,[f[1] for f in fields])

# Call sites whose receiver is explicitly a recipe. Remaining sites are checked by javac.
for root in roots:
 for p in root.rglob('*.java'):
  s=p.read_text(encoding='utf-8');old=s
  s=re.sub(r'\b(\w*[Rr]ecipe)\.(outputFluid|inputFluid1|inputFluid2|inputFluid|handItem)\b(?!\s*\()',r'\1.\2()',s)
  # output/input may also be ingredients, so defer those ambiguous names to javac.
  if s!=old:p.write_text(s,encoding='utf-8',newline='\n')
