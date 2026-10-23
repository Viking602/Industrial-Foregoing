from pathlib import Path
import re
root=Path(__file__).resolve().parent

def static_calls(s,method,owner):
    pattern=re.compile(r'\.'+method+r'\(')
    for match in reversed(list(pattern.finditer(s))):
        end=match.start(); start=end-1; depth=0
        while start>=0:
            c=s[start]
            if c in ')]': depth+=1
            elif c in '([':
                if depth==0: break
                depth-=1
            elif depth==0 and not (c.isalnum() or c in '._$'): break
            start-=1
        start+=1
        receiver=s[start:end]
        s=s[:start]+owner+'.'+method+'('+receiver+', '+s[match.end():]
    return s

for f in (root/'src/main/java').rglob('*.java'):
    if '/compat/' in f.as_posix(): continue
    s=f.read_text(encoding='utf-8')
    for method in ['fillForced','drainForced']:
        s=static_calls(s,method,'com.buuz135.industrial.compat.MachineFluids')
    s=s.replace('new SidedFluidTankComponent<','new com.buuz135.industrial.compat.MachineFluidTank<')
    if 'implements Recipe<CraftingInput>' in s:
        s=s.replace('implements Recipe<CraftingInput>','implements com.buuz135.industrial.compat.MachineRecipe')
        s=re.sub(r'assemble\(CraftingInput (\w+), HolderLookup.Provider \w+\)',r'assemble(CraftingInput \1)',s)
        s=s.replace('RecipeSerializer<?> getSerializer()', 'RecipeSerializer getSerializer()').replace('RecipeType<?> getType()', 'RecipeType getType()')
        s=re.sub(r'(public ItemStack assemble\(CraftingInput \w+\)\s*\{\s*)return null;',r'\1return ItemStack.EMPTY;',s)
    if '/recipe/' in f.as_posix():
        key='net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.RECIPE, rl)'
        s=s.replace('RecipeUnlockedTrigger.unlocked(rl)', 'RecipeUnlockedTrigger.unlocked('+key+')')
        s=s.replace('AdvancementRewards.Builder.recipe(rl)', 'AdvancementRewards.Builder.recipe('+key+')')
        s=s.replace('recipeOutput.accept(rl,', 'recipeOutput.accept('+key+',')
    s=s.replace('TagKey::location', 'TagKey::identifier')
    f.write_text(s,encoding='utf-8')
print('Machine recipe and fluid transaction adapters applied')
