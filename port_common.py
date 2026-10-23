from pathlib import Path
import re,json

root=Path(__file__).resolve().parent
work=root.parent
errors=json.loads((root/'compile-02.errors.json').read_text(encoding='utf-8'))
byfile={}
for e in errors: byfile.setdefault(Path(e['file']),[]).append(e)
for f,es in byfile.items():
    lines=f.read_text(encoding='utf-8').splitlines(keepends=True)
    # The compiler identifies these calls as NBT getters returning Optional in 26.1.
    for n in {e['line']-1 for e in es if 'Optional' in e['detail']}:
        for typ,val in {'Byte':'(byte)0','Short':'(short)0','Int':'0','Long':'0L','Float':'0F','Double':'0D','Boolean':'false','String':'""'}.items():
            lines[n]=re.sub(r'\.get'+typ+r'\(("[^"]*"|\w+)\)',lambda m:'.get'+typ+'Or('+m[1]+', '+val+')',lines[n])
        lines[n]=re.sub(r'\.getCompound\(("[^"]*"|\w+)\)',r'.getCompoundOrEmpty(\1)',lines[n])
    f.write_text(''.join(lines),encoding='utf-8')

for repo in [root,work/'IndustrialForegoingExtraUpgrades']:
    for f in (repo/'src').rglob('*.java'):
        s=f.read_text(encoding='utf-8')
        s=s.replace('net.minecraft.world.item.UseAnim','net.minecraft.world.item.ItemUseAnimation')
        s=re.sub(r'\bUseAnim\b','ItemUseAnimation',s)
        s=s.replace('.getCommandSenderWorld()', '.level()').replace('.getNormal()', '.getUnitVec3i()')
        s=s.replace('.getAllKeys()', '.keySet()').replace('.registryOrThrow(', '.lookupOrThrow(')
        s=re.sub(r'\.random\b(?!\()', '.getRandom()', s)
        s=s.replace('MobEffects.MOVEMENT_SLOWDOWN','MobEffects.SLOWNESS').replace('MobEffects.MOVEMENT_SPEED','MobEffects.SPEED')
        s=s.replace('MobEffects.DIG_SPEED','MobEffects.HASTE').replace('MobEffects.DAMAGE_BOOST','MobEffects.STRENGTH')
        s=s.replace('MobEffects.CONFUSION','MobEffects.NAUSEA')
        s=s.replace('new CodecRecipeSerializer<>(', 'CodecRecipeSerializer.create(')
        s=s.replace('SizedFluidIngredient.FLAT_CODEC','SizedFluidIngredient.CODEC')
        s=s.replace('SizedFluidIngredient.of(inputFluid)','SizedFluidIngredient.of(inputFluid.getFluid(), inputFluid.getAmount())')
        s=s.replace('.getItems()', '.items().map(net.minecraft.world.item.ItemStack::new).toArray(net.minecraft.world.item.ItemStack[]::new)') if 'Ingredient' in s else s
        s=s.replace('Screen.hasShiftDown()', 'net.minecraft.client.Minecraft.getInstance().hasShiftDown()')
        s=s.replace('Screen.hasControlDown()', 'net.minecraft.client.Minecraft.getInstance().hasControlDown()')
        s=s.replace('Screen.hasAltDown()', 'net.minecraft.client.Minecraft.getInstance().hasAltDown()')
        s=s.replace('Ingredient.of(', 'com.buuz135.industrial.compat.Ingredients.of(') if repo==root else s
        f.write_text(s,encoding='utf-8')

# Runtime resources remain included. Old data generators need a separate API migration.
p=root/'build.gradle'; s=p.read_text()
s += '''
sourceSets.main.java {
    exclude 'com/buuz135/industrial/plugin/emi/**'
    exclude 'com/buuz135/industrial/utils/data/**'
    exclude 'com/buuz135/industrial/recipe/provider/**'
}
tasks.withType(JavaCompile).configureEach {
    options.fork = true
    options.forkOptions.jvmArgs += ['-Duser.language=en', '-Duser.country=US', '-Dfile.encoding=UTF-8']
}
'''
s=s.replace('    compileOnly "dev.emi:emi-neoforge:1.1.12+1.21:api"','')
p.write_text(s)
p=root/'src/main/java/com/buuz135/industrial/IndustrialForegoing.java'; s=p.read_text()
s=re.sub(r'import com\.buuz135\.industrial\.(?:utils\.data|recipe\.provider)\.[^;]+;\n','',s)
a=s.index('    @Override\n    public void addDataProvider('); b=s.index('    @Override\n    protected void initModules()',a)
s=s[:a]+s[b:]; p.write_text(s)
print('Common API migration applied')
