from pathlib import Path
from collections import defaultdict, Counter
import re

root = Path(__file__).resolve().parent
work = root.parent
api = work/'devtools/api-sources'
index = defaultdict(list)
for f in api.rglob('*.java'):
    index[f.stem].append(str(f.relative_to(api).with_suffix('')).replace('\\','.'))
renames = {'GuiGraphics':'GuiGraphicsExtractor', 'ItemInteractionResult':'InteractionResult', 'MobSpawnType':'EntitySpawnReason', 'FastColor.ARGB32':'ARGB', 'FastColor.ABGR32':'ABGR', 'net.minecraft.advancements.critereon':'net.minecraft.advancements.criterion', 'net.neoforged.neoforge.common.util.INBTSerializable':'com.hrznstudio.titanium.nbthandler.INBTSerializable'}
for repo in [root, work/'IndustrialForegoingExtraUpgrades']:
    for f in (repo/'src').rglob('*.java'):
        s = f.read_text(encoding='utf-8')
        for a,b in renames.items():
            s = re.sub(r'\b'+re.escape(a)+r'\b', b, s)
        s = s.replace('import net.minecraft.util.FastColor;', 'import net.minecraft.util.ARGB;')
        s = s.replace('import net.minecraft.MethodsReturnNonnullByDefault;\n','').replace('@MethodsReturnNonnullByDefault','')
        s = s.replace('InteractionResult.PASS_TO_DEFAULT_BLOCK_INTERACTION','InteractionResult.TRY_WITH_EMPTY_HAND').replace('InteractionResult.SKIP_DEFAULT_BLOCK_INTERACTION','InteractionResult.PASS')
        s = re.sub(r'\.isClientSide\b(?!\s*\()', '.isClientSide()', s)
        s = s.replace('.location()', '.identifier()')
        s = s.replace('.getOrCreateTag()', '.getOrCreateTag()')
        def remap(m):
            name=m[1]; simple=name.rsplit('.',1)[-1]
            if name.startswith(('net.minecraft.', 'net.neoforged.')) and not (api/(name.replace('.','/')+'.java')).exists() and len(index[simple])==1:
                return 'import '+index[simple][0]+';'
            return m[0]
        s = re.sub(r'import ([\w.]+);', remap, s)
        if '/generator/mycelial/' in f.as_posix() or f.name=='MycelialGeneratorTile.java':
            s=s.replace('INBTSerializable<CompoundTag>', 'Object')
        f.write_text(s,encoding='utf-8')

# Only change NBT getters that javac has identified as incompatible Optional results.
log=(root/'compile-01.log').read_text(encoding='utf-8',errors='replace').split('FAILURE:')[0]
errors=re.split(r'(?=D:\\.*?\.java:\d+: 错误:)',log)
defaults={'Byte':'(byte) 0','Short':'(short) 0','Int':'0','Long':'0L','Float':'0F','Double':'0D','Boolean':'false','String':'""'}
byfile=defaultdict(list)
for e in errors:
    m=re.match(r'(D:\\.*?\.java):(\d+): 错误:',e)
    if m: byfile[Path(m[1])].append((int(m[2])-1,e))
for f,es in byfile.items():
    lines=f.read_text(encoding='utf-8').splitlines(keepends=True)
    for n,e in es:
        if 'Optional' not in e: continue
        for typ,default in defaults.items():
            lines[n]=re.sub(r'\.get'+typ+r'\(("[^"]*"|\w+)\)',lambda m:'.get'+typ+'Or('+m[1]+', '+default+')',lines[n])
    f.write_text(''.join(lines),encoding='utf-8')
print('API names and compiler-confirmed NBT defaults migrated')
