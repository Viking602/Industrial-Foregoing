from pathlib import Path
import re,ast
root=Path(__file__).resolve().parent
tree=ast.parse((root/'port_recipes_fluids.py').read_text())
fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef))
exec(compile(ast.Module(body=[fn],type_ignores=[]),'<helper>','exec'))
for f in (root/'src/main/java').rglob('*.java'):
    if '/compat/' in f.as_posix(): continue
    s=f.read_text(encoding='utf-8')
    s=s.replace('.getCompound(','.getCompoundOrEmpty(')
    s=s.replace('Sizedcom.buuz135.industrial.compat.Ingredients','SizedIngredient').replace('Entitycom.buuz135.industrial.compat.Ingredients','EntityIngredient')
    s=s.replace('List<IFactory<? extends IScreenAddon>>','List<IFactory<?>>')
    for method in ['receiveEnergy','extractEnergy']:
        s=static_calls(s,method,'com.buuz135.industrial.compat.MachineEnergy')
    if '/generator/mycelial/' in f.as_posix() or f.name=='MycelialGeneratorTile.java':
        s=s.replace('Object[]', 'net.neoforged.neoforge.common.util.ValueIOSerializable[]')
        s=s.replace('new INBTSerializable[', 'new net.neoforged.neoforge.common.util.ValueIOSerializable[')
    if f.name=='DissolutionChamberRecipe.java':
        s=s.replace('import net.neoforged.neoforge.common.conditions.ItemExistsCondition;', 'import net.neoforged.neoforge.common.conditions.RegisteredCondition;')
        s=s.replace('new ItemExistsCondition(BuiltInRegistries.ITEM.getKey(recipe.output.get().getItem()))','new RegisteredCondition<>(BuiltInRegistries.ITEM.getResourceKey(recipe.output.get().getItem()).orElseThrow())')
    if f.name=='LaserDrillFluidRecipe.java':
        s=s.replace('ModFluids.OIL.get()', 'net.minecraft.core.registries.BuiltInRegistries.FLUID.getValue(Identifier.fromNamespaceAndPath("pneumaticcraft", "oil"))')
    f.write_text(s,encoding='utf-8')

for name in ['ConveyorTile','TransporterTile','MycelialGeneratorTile']:
    f=next((root/'src/main/java').rglob(name+'.java')); s=f.read_text()
    for method,tagtype in [('saveAdditional','ValueOutput'),('loadAdditional','ValueInput')]:
        pattern=re.compile(r'(protected|public) void '+method+r'\(CompoundTag (\w+), HolderLookup.Provider provider\) \{')
        m=pattern.search(s)
        if not m: continue
        namevar=m[2]; start=m.end(); end=start; depth=1
        while depth:
            if s[end]=='{':depth+=1
            elif s[end]=='}':depth-=1
            end+=1
        body=s[start:end-1]
        body=body.replace('super.'+method+'('+namevar+', provider)', 'super.'+method+'('+namevar+')')
        provider='com.buuz135.industrial.utils.IFAttachments.registryAccess()' if tagtype=='ValueOutput' else namevar+'.lookup()'
        body=re.sub(r'\bprovider\b',provider,body)
        if tagtype=='ValueOutput':
            body=re.sub(r'\b'+namevar+r'\.put\(("[^"]*"), ',namevar+r'.store(\1, CompoundTag.CODEC, ',body)
            body=re.sub(r'compoundTag.put\("input_" \+ i, this.inputs\[i\].serializeNBT\([\s\S]*?\)\);', 'this.inputs[i].serialize(compoundTag.child("input_" + i));',body)
        else:
            body=re.sub(r'\b'+namevar+r'\.contains\(("[^"]*")\)',namevar+r'.child(\1).isPresent()',body)
            body=re.sub(r'\b'+namevar+r'\.getCompoundOrEmpty\(("[^"]*")\)',namevar+r'.read(\1, CompoundTag.CODEC).orElseGet(CompoundTag::new)',body)
            body=re.sub(r'this.inputs\[i\].deserializeNBT\([^;]+;', 'this.inputs[i].deserialize(compound.childOrEmpty("input_" + i));',body)
        s=s[:m.start()]+m[1]+' void '+method+'(net.minecraft.world.level.storage.'+tagtype+' '+namevar+') {'+body+'}'+s[end:]
    if name=='ConveyorTile':
        s=s.replace('        CompoundTag compoundTag = new CompoundTag();\n        saveAdditional(compoundTag, this.level.registryAccess());\n        this.loadAdditional(compoundTag, this.level.registryAccess()); //read\n','')
    f.write_text(s)
print('Machine energy calls and block persistence migrated')
