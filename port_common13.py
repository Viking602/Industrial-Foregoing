from pathlib import Path
import re
root=Path('.work/Industrial-Foregoing/src/main/java')
# Load the call rewriter without executing its original migration pass.
code=Path('.work/Industrial-Foregoing/port_recipes_fluids.py').read_text().split('for f in (root/')[0]
ns={};exec(code.replace('root=Path(__file__).resolve().parent',''),ns); calls=ns['static_calls']
for p in root.rglob('*.java'):
 s=p.read_text()
 if 'compat' not in p.parts:
  s=calls(s,'saveWithoutId','com.buuz135.industrial.compat.EntityNbt')
  s=calls(s,'getCraftingRemainder','com.buuz135.industrial.compat.MachineItems').replace('getCraftingRemainder(itemstack, )','getCraftingRemainder(itemstack)').replace(', )', ')')
 s=s.replace('net.neoforged.neoforge.common.CommonHooks.isBookEnchantable(inputFirstCopy, inputSecond)', 'net.minecraft.world.item.enchantment.EnchantmentHelper.canStoreEnchantments(inputFirstCopy)')
 s=s.replace('getLootTable(entity.getLootTable())', 'getLootTable(entity.getLootTable().orElse(net.minecraft.world.level.storage.loot.BuiltInLootTables.EMPTY))')
 s=s.replace('stack.getItemHolder().tags()', 'stack.typeHolder().tags()')
 s=s.replace('entity.load(nbt)', 'com.buuz135.industrial.compat.EntityNbt.load(entity, nbt)')
 if p.name=='MachineItems.java':
  pos=s.index('    private MachineItems') if '    private MachineItems' in s else s.index('{')+1
  s=s[:pos]+'''    public static net.minecraft.world.item.ItemStack getCraftingRemainder(net.minecraft.world.item.ItemStack stack) {
        var remainder = stack.getCraftingRemainder();
        return remainder == null ? net.minecraft.world.item.ItemStack.EMPTY : remainder.create();
    }
'''+s[pos:]
 if p.name=='ItemStackWeightedItem.java':
  s=s.replace('import net.minecraft.util.random.Weight;', '').replace('import net.minecraft.util.random.WeightedEntry;','').replace(' implements WeightedEntry','').replace('Weight weight','int weight').replace('Weight.of(itemWeightIn)','itemWeightIn').replace('    @Override\n','').replace('public Weight getWeight','public int getWeight')
 if p.name=='OreLaserBaseTile.java':
  s=s.replace('WeightedRandom.getRandomItem(this.level.getRandom(), items).get().getStack()', 'WeightedRandom.getRandomItem(this.level.getRandom(), items.stream().map(i -> new net.minecraft.util.random.Weighted<>(i.getStack(), i.getWeight())).toList()).orElse(ItemStack.EMPTY)')
  s=s.replace('recipe.output.getItems()', 'recipe.output.ingredient().items().map(holder -> new ItemStack(holder, recipe.output.count())).toArray(ItemStack[]::new)')
 if p.name=='FluidLaserBaseTile.java':
  s=s.replace('recipe.output.getFluids()[0].copy()', 'recipe.output.getFluids().getFirst().copy()')
 if p.name=='LatexProcessingUnitTile.java':
  s=s.replace('latex.drain(AMOUNT_LATEX, IFluidHandler.FluidAction.EXECUTE)', 'com.buuz135.industrial.compat.MachineFluids.drainForced(latex, AMOUNT_LATEX, IFluidHandler.FluidAction.EXECUTE)').replace('water.drain(AMOUNT_WATER, IFluidHandler.FluidAction.EXECUTE)', 'com.buuz135.industrial.compat.MachineFluids.drainForced(water, AMOUNT_WATER, IFluidHandler.FluidAction.EXECUTE)')
 if p.name=='StoneWorkGenerateRecipe.java': s=s.replace('canIncrease(FluidTank fluidTank, FluidTank fluidTank2)', 'canIncrease(FluidTankComponent fluidTank, FluidTankComponent fluidTank2)')
 if p.name=='ResourcefulFurnaceTile.java':
  s=s.replace('furnaceRecipe.getIngredients().get(0)', 'furnaceRecipe.input()').replace('recipe.getResultItem(this.level.registryAccess()).copy()', 'recipe.assemble(new net.minecraft.world.item.crafting.SingleRecipeInput(input.getStackInSlot(slot)))').replace('recipe.getExperience()', 'recipe.experience()')
 if p.name=='MaterialStoneWorkFactoryTile.java':
  s=s.replace('recipe.getResultItem(world1.registryAccess())', 'recipe.assemble(new net.minecraft.world.item.crafting.SingleRecipeInput(itemStack))')
  s=s.replace('this.level.getRecipeManager().getAllRecipesFor(', '((net.minecraft.server.level.ServerLevel) this.level).getRecipeManager().recipeMap().byType(')
  s=s.replace('List<RecipeHolder<StoneWorkGenerateRecipe>> recipes', 'var recipes').replace('map(RecipeHolder::id)', 'map(holder -> holder.id().identifier())')
 if p.name in ['FermentationStationTile.java','FluidCollectorTile.java']:
  s=s.replace('this.catalyst.isEmpty()', 'this.catalyst.getFluid().isEmpty()').replace('tank.isEmpty()', 'tank.getFluid().isEmpty()')
 if p.name=='IMachineSettings.java':s=s.replace('stack.save(registryAccess)', 'com.buuz135.industrial.compat.ItemNbt.saveOptional(stack, registryAccess)')
 if p.name=='FungusBlockMixin.java':s=s.replace('@Local(name = "blockstate") BlockState blockstate','@Local(name = "belowState") BlockState blockstate')
 if p.name in ['ItemInfinityBackpack.java','MeatFeederItem.java']:
  s=s.replace('public void inventoryTick(ItemStack stack, Level worldIn, Entity entityIn, int itemSlot, boolean isSelected)', 'public void inventoryTick(ItemStack stack, net.minecraft.server.level.ServerLevel worldIn, Entity entityIn, net.minecraft.world.entity.EquipmentSlot equipmentSlot)')
  s=s.replace('super.inventoryTick(stack, worldIn, entityIn, itemSlot, isSelected)', 'super.inventoryTick(stack, worldIn, entityIn, equipmentSlot)')
 if p.name=='MycelialDataManager.java':
  s=s.replace('new Factory<MycelialDataManager>(MycelialDataManager::new, (compoundTag, provider) -> MycelialDataManager.load(provider, compoundTag)), NAME', 'new net.minecraft.world.level.saveddata.SavedDataType<>(net.minecraft.resources.Identifier.fromNamespaceAndPath("industrialforegoing", "mycelial"), level -> new MycelialDataManager(), level -> CompoundTag.CODEC.xmap(tag -> load(level.registryAccess(), tag), data2 -> data2.save(new CompoundTag(), level.registryAccess())))')
  s=s.replace('    @Override\n    public CompoundTag save', '    public CompoundTag save')
 if p.name in ['InfinityNukeEntity.java','InfinityTridentEntity.java','InfinityLauncherProjectileEntity.java']:
  s=s.replace('readAdditionalSaveData(CompoundTag compound)', 'readAdditionalSaveData(net.minecraft.world.level.storage.ValueInput compound)').replace('addAdditionalSaveData(CompoundTag compound)', 'addAdditionalSaveData(net.minecraft.world.level.storage.ValueOutput compound)')
  s=s.replace('compound.getCompoundOrEmpty("Original")', 'compound.read("Original", CompoundTag.CODEC).orElseGet(CompoundTag::new)').replace('compound.getCompoundOrEmpty("Trident")', 'compound.read("Trident", CompoundTag.CODEC).orElseGet(CompoundTag::new)')
  s=s.replace('compound.contains("Trident", 10)', 'compound.read("Trident", CompoundTag.CODEC).isPresent()')
  s=s.replace('compound.put("Original",', 'compound.store("Original", net.minecraft.nbt.Tag.CODEC,').replace('compound.put("Trident",', 'compound.store("Trident", net.minecraft.nbt.Tag.CODEC,')
  s=s.replace('interact(Player player, InteractionHand hand)', 'interact(Player player, InteractionHand hand, net.minecraft.world.phys.Vec3 location)').replace('super.interact(player, hand)', 'super.interact(player, hand, location)')
 p.write_text(s)
# Use actual recipe matching and output assembly, including custom crafting results.
p=root/'com/buuz135/industrial/utils/CraftingUtils.java'
s=p.read_text(); a=s.index('    private static final Map'); b=s.index('    public static ItemStack getCrushOutput')
s=s[:a]+'''    public static ItemStack findOutput(int size, ItemStack input, Level world) {
        if (input.getCount() < size * size) return ItemStack.EMPTY;
        var craftingInput = CraftingInput.of(size, size, java.util.Collections.nCopies(size * size, input.copyWithCount(1)));
        for (CraftingRecipe recipe : RecipeUtil.getRecipes(world, RecipeType.CRAFTING)) {
            if (recipe.matches(craftingInput, world)) return recipe.assemble(craftingInput);
        }
        return ItemStack.EMPTY;
    }

'''+s[b:];p.write_text(s)
