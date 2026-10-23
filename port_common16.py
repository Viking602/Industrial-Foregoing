from pathlib import Path
import re
root=Path('.work/Industrial-Foregoing/src/main/java/com/buuz135/industrial')
for p in (root/'block/generator/mycelial').glob('*.java'):
 s=p.read_text().replace('import net.minecraft.data.recipes.ShapedRecipeBuilder;', 'import com.hrznstudio.titanium.recipe.generator.TitaniumShapedRecipeBuilder;').replace('ShapedRecipeBuilder','TitaniumShapedRecipeBuilder').replace('TitaniumTitaniumShapedRecipeBuilder','TitaniumShapedRecipeBuilder')
 p.write_text(s)
p=root/'block/resourceproduction/tile/FluidLaserBaseTile.java';s=p.read_text().replace('new FluidStack(recipe.output.ingredient().fluids().findFirst().orElseThrow(),', 'new net.neoforged.neoforge.fluids.FluidStack(recipe.output.ingredient().fluids().getFirst(),');p.write_text(s)
p=root/'recipe/data/EntityData.java';s=p.read_text()
for typ,box,method in [('byte','Byte','Byte'),('int','Integer','Int'),('long','Long','Long')]:
 old=f'public TagBuilder put{method}Array(String key, List<{box}> value) {{\n            tag.put{method}Array(key, value);'
 new=f'public TagBuilder put{method}Array(String key, List<{box}> value) {{\n            {typ}[] array = new {typ}[value.size()];\n            for (int i = 0; i < array.length; i++) array[i] = value.get(i);\n            tag.put{method}Array(key, array);'
 assert old in s;s=s.replace(old,new)
p.write_text(s)
p=root/'block/resourceproduction/tile/ResourcefulFurnaceTile.java';s=p.read_text();a=s.index('        for (SmeltingRecipe recipe : this.recipes)');b=s.index('\n        return false;',a)
s=s[:a]+'''        for (int i = 0; i < this.recipes.length; i++) {
            SmeltingRecipe recipe = this.recipes[i];
            if (recipe != null && MachineItems.insertItem(output, recipe.assemble(new net.minecraft.world.item.crafting.SingleRecipeInput(input.getStackInSlot(i))), true).isEmpty())
                return true;
        }'''+s[b:]
a=s.index('                if (recipe != null &&',s.index('public Runnable onFinish'));b=s.index('\n            }\n        };',a)
s=s[:a]+'''                if (recipe != null) {
                    ItemStack result = recipe.assemble(new net.minecraft.world.item.crafting.SingleRecipeInput(input.getStackInSlot(i)));
                    if (!result.isEmpty() && MachineItems.insertItem(output, result, true).isEmpty()) {
                        input.setStackInSlot(i, ItemStack.EMPTY);
                        MachineItems.insertItem(output, result, false);
                        com.buuz135.industrial.compat.MachineFluids.fillForced(tank, new FluidStack(ModuleCore.ESSENCE.getSourceFluid().get(), (int) (recipe.experience() * 20)), IFluidHandler.FluidAction.EXECUTE);
                    }
                }'''+s[b:];p.write_text(s)
for name,defaults in [('Launcher',[('PLUNGER_ACTION','PlungerAction.RELEASE')]),('Hammer',[('INFINITY_HAMMER_BEHEADING','0')]),('Trident',[('INFINITY_TRIDENT_LOYALTY','0'),('INFINITY_TRIDENT_RIPTIDE','0'),('INFINITY_TRIDENT_CHANNELING','false')]),('Backpack',[])]:
 p=root/f'item/infinity/item/ItemInfinity{name}.java';s=p.read_text()
 s=re.sub(r'    @Override\n    public void verifyComponentsAfterLoad\(ItemStack stack\) \{.*?\n    \}\n','',s,flags=re.S)
 s=re.sub(r'    @Override\n    public boolean isEnchantable\(ItemStack stack\) \{.*?\n    \}\n','',s,flags=re.S)
 s=s.replace('new Properties().stacksTo(1)', 'new Properties().stacksTo(1)'+''.join(f'.component(IFAttachments.{key}.get(), {value})' for key,value in defaults),1)
 p.write_text(s)
for p in (root/'plugin/jei').rglob('*.java'):
 s=p.read_text().replace('implements IRecipeCategory<','implements com.buuz135.industrial.plugin.jei.MachineRecipeCategory<')
 s=s.replace('RecipeIngredientRole.CATALYST','RecipeIngredientRole.CRAFTING_STATION').replace('entityIngredient.tag().identifier()','entityIngredient.tag().location()').replace('recipe.inputFluid.ingredient().isEmpty()','recipe.inputFluid.ingredient().fluids().isEmpty()')
 s=s.replace('Arrays.asList(recipe.inputFluid.getFluids())','com.buuz135.industrial.compat.IngredientViews.fluids(recipe.inputFluid)').replace('Arrays.stream(recipe.output.getFluids()).toList()','com.buuz135.industrial.compat.IngredientViews.fluids(recipe.output)')
 s=s.replace('DyeItem.byColor(DyeColor.byId(this.dye))','(DyeItem) net.minecraft.core.registries.BuiltInRegistries.ITEM.getValue(net.minecraft.resources.Identifier.withDefaultNamespace(DyeColor.byId(this.dye).getName() + "_dye"))')
 s=re.sub(r'(public void draw\([^\n]+GuiGraphicsExtractor (\w+)[^\n]+\{)',lambda m:m[1]+'\n        getBackground().draw('+m[2]+', 0, 0);',s)
 s=s.replace('    @Override\n    public String getLegacyStringSubtypeInfo', '    public String getLegacyStringSubtypeInfo')
 s=s.replace('BuiltInRegistries.ITEM.getTagNames()', 'BuiltInRegistries.ITEM.getTags().map(net.minecraft.core.HolderSet.Named::key)')
 p.write_text(s)
