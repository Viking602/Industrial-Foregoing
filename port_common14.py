from pathlib import Path
import re,json
root=Path('.work/Industrial-Foregoing/src/main/java')
for p in root.rglob('*.java'):
 s=p.read_text().replace('TagKey::identifier','TagKey::location')
 s=re.sub(r'@Override\s+(public String getCreatorModId)',r'\1',s)
 s=s.replace('onTreeGrow(BlockState state, LevelReader level,', 'onTreeGrow(BlockState state, net.minecraft.world.level.WorldGenLevel level,')
 s=s.replace('((net.minecraft.server.level.ServerLevel) this.level).getRecipeManager()', 'this.level.getServer().getRecipeManager()')
 s=s.replace('EntityType.BUILT_IN_REGISTRY', 'EntityType.BUILT_IN_REGISTRY')
 s=s.replace('public boolean onEntitySwing(ItemStack stack, LivingEntity entity)', 'public boolean onEntitySwing(ItemStack stack, LivingEntity entity, InteractionHand hand)')
 s=s.replace('getName().copy().withStyle', 'Component.translatable(getDescriptionId()).withStyle')
 s=s.replace('getInventory().items', 'getInventory().getNonEquipmentItems()')
 if p.name in ['InfinityNukeEntity.java','InfinityTridentEntity.java']:
  s=re.sub(r'compound.store\("(Original|Trident)", net.minecraft.nbt.Tag.CODEC, com.buuz135.industrial.compat.ItemNbt.saveOptional\((.*?), (.*?)\)\);',r'compound.store("\1", ItemStack.OPTIONAL_CODEC, \2);',s)
 if p.name=='MobCrusherTile.java':
  s=s.replace('this.level.getServer().reloadableRegistries().getLootTable(entity.getLootTable().orElse(net.minecraft.world.level.storage.loot.BuiltInLootTables.EMPTY))', 'entity.getLootTable().map(this.level.getServer().reloadableRegistries()::getLootTable).orElse(LootTable.EMPTY)')
 if p.name in ['FluidExtractorBlock.java','WaterCondensatorBlock.java']:
  s=s.replace('    @Override\n    public void appendHoverText', '    public void appendHoverText').replace('        super.appendHoverText(stack, context, tooltipComponents, tooltipFlag);\n','')
 if p.name=='IndustrialBlockItem.java':
  idx=s.rfind('}')
  s=s[:idx]+'''    @Override
    public void appendHoverText(ItemStack stack, Item.TooltipContext context, net.minecraft.world.item.component.TooltipDisplay display, java.util.function.Consumer<Component> tooltip, net.minecraft.world.item.TooltipFlag flag) {
        super.appendHoverText(stack, context, display, tooltip, flag);
        if (getBlock() instanceof com.buuz135.industrial.block.core.FluidExtractorBlock || getBlock() instanceof com.buuz135.industrial.block.resourceproduction.WaterCondensatorBlock) {
            tooltip.accept(Component.translatable("text.industrialforegoing.tooltip.power_optional").withStyle(net.minecraft.ChatFormatting.GOLD));
        }
    }
'''+s[idx:]
 if p.name=='MycelialGeneratorBlock.java':
  s=s.replace('public void onRemove(BlockState state, Level worldIn, BlockPos pos, BlockState newState, boolean isMoving)', 'public void affectNeighborsAfterRemoval(BlockState state, net.minecraft.server.level.ServerLevel worldIn, BlockPos pos, boolean isMoving)').replace('super.onRemove(state, worldIn, pos, newState, isMoving)', 'super.affectNeighborsAfterRemoval(state, worldIn, pos, isMoving)').replace('ShapedRecipeBuilder recipe =', 'var recipe =')
 if p.name=='DyeMixerTile.java':s=s.replace('DyeItem.byColor(DyeColor.byId(dye))','dyeItem(DyeColor.byId(dye))').replace('DyeItem.byColor(DyeColor.byId(this.dye))','dyeItem(DyeColor.byId(this.dye))');idx=s.rfind('}');s=s[:idx]+'''    private static net.minecraft.world.item.Item dyeItem(DyeColor color) {
        return net.minecraft.core.registries.BuiltInRegistries.ITEM.getValue(net.minecraft.resources.Identifier.withDefaultNamespace(color.getName() + "_dye"));
    }
'''+s[idx:]
 if p.name=='FluidLaserBaseTile.java':s=s.replace('recipe.output.getFluids().getFirst().copy()', 'new FluidStack(recipe.output.ingredient().fluids().findFirst().orElseThrow(), recipe.output.amount())')
 if p.name=='MechanicalDirtTile.java':
  lines=s.splitlines();lines=[('                        com.buuz135.industrial.compat.MachineFluids.move(meat, ((MechanicalDirtTile) tile).getMeat(), difference);' if 'getMeat().fill(' in line else line) for line in lines];s='\n'.join(lines)+'\n'
 if p.name=='OreLaserBaseTile.java':s=s.replace('WeightedRandom.getRandomItem(this.level.getRandom(), items.stream().map(i -> new net.minecraft.util.random.Weighted<>(i.getStack(), i.getWeight())).toList()).orElse(ItemStack.EMPTY)', 'WeightedRandom.getRandomItem(this.level.getRandom(), items, ItemStackWeightedItem::getWeight).map(ItemStackWeightedItem::getStack).orElse(ItemStack.EMPTY)')
 if p.name=='EntityData.java':
  for method,conversion in [('Byte','com.google.common.primitives.Bytes.toArray(value)'),('Int','value.stream().mapToInt(Integer::intValue).toArray()'),('Long','value.stream().mapToLong(Long::longValue).toArray()')]:
   pattern=r'(public void put'+method+r'Array\(String key, List<.*?> value\) \{\s*tag.put'+method+r'Array\(key, )value'
   s=re.sub(pattern,lambda m:m[1]+conversion,s)
 if p.name=='ResourcefulFurnaceTile.java':
  s=s.replace('recipe.assemble(new net.minecraft.world.item.crafting.SingleRecipeInput(input.getStackInSlot(slot)))','recipe.result().create()')
 if p.name in ['ConveyorBlock.java','InfinityBackpackBlock.java','TransporterBlock.java']:
  s=re.sub(r'getCloneItemStack\(BlockState state, HitResult target, LevelReader (world|level), BlockPos pos, Player player\)',r'getCloneItemStack(LevelReader \1, BlockPos pos, BlockState state, boolean includeData, Player player)',s)
  s=s.replace('if (target instanceof DistanceRayTraceResult)', 'if (player != null)').replace('if (target instanceof BlockHitResult)', 'if (player != null)')
  s=s.replace('super.getCloneItemStack(state, target, world, pos, player)', 'super.getCloneItemStack(world, pos, state, includeData, player)')
  s=s.replace('BlockPos fromPos, boolean p_220069_6_', 'net.minecraft.world.level.redstone.Orientation fromPos, boolean p_220069_6_')
  s=s.replace('((DyeItem) handStack.getItem()).getDyeColor()', 'handStack.getOrDefault(net.minecraft.core.component.DataComponents.DYE, net.minecraft.world.item.DyeColor.WHITE)')
  s=s.replace('entityInside(BlockState state, Level worldIn, BlockPos pos, Entity entityIn)', 'entityInside(BlockState state, Level worldIn, BlockPos pos, Entity entityIn, net.minecraft.world.entity.InsideBlockEffectApplier effectApplier, boolean precise)').replace('super.entityInside(state, worldIn, pos, entityIn)', 'super.entityInside(state, worldIn, pos, entityIn, effectApplier, precise)')
 if p.name=='ConveyorTile.java':
  s=s.replace('tank.writeToNBT(com.buuz135.industrial.utils.IFAttachments.registryAccess(), new CompoundTag())','com.buuz135.industrial.compat.ValueNbt.save(tank, com.buuz135.industrial.utils.IFAttachments.registryAccess())').replace('this.tank.readFromNBT(compound.lookup(), compound.read("Tank", CompoundTag.CODEC).orElseGet(CompoundTag::new))','com.buuz135.industrial.compat.ValueNbt.load(this.tank, compound.lookup(), compound.read("Tank", CompoundTag.CODEC).orElseGet(CompoundTag::new))')
 if p.name=='InfinityTankStorage.java':
  s=s.replace('tank.readFromNBT(IFAttachments.registryAccess(), component.getCompoundOrEmpty(tankDefinition.name()))','com.buuz135.industrial.compat.ValueNbt.load(tank, IFAttachments.registryAccess(), component.getCompoundOrEmpty(tankDefinition.name()))').replace('tank.writeToNBT(IFAttachments.registryAccess(), component.getCompoundOrEmpty(tankDefinition.name()))', 'com.buuz135.industrial.compat.ValueNbt.save(tank, IFAttachments.registryAccess())')
 if p.name=='ItemInfinity.java':
  s=s.replace('super(name, group, builder);','super(name, group, builder.enchantable(50).component(IFAttachments.INFINITY_ITEM_POWER.get(), 0L).component(IFAttachments.INFINITY_ITEM_SPECIAL.get(), false).component(IFAttachments.INFINITY_ITEM_SELECTED_TIER.get(), InfinityTier.POOR).component(IFAttachments.INFINITY_ITEM_CAN_CHARGE.get(), true));')
  s=re.sub(r'    @Override\n    public void verifyComponentsAfterLoad\(ItemStack stack\) \{.*?\n    \}\n','',s,flags=re.S)
  for name in ['isEnchantable','getEnchantmentValue']:
   s=re.sub(r'    @Override\n    public (boolean|int) '+name+r'\([^)]*\) \{.*?\n    \}\n','',s,flags=re.S)
 if p.name=='OreFluid.java':s=s.replace('FluidState state, Level level, BlockPos pos','FluidState state, net.minecraft.server.level.ServerLevel level, BlockPos pos').replace('canConvertToSource(Level p_256009_)','canConvertToSource(net.minecraft.server.level.ServerLevel p_256009_)')
 if p.name=='PumpkinMelonPlantRecollectable.java':s=s.replace('blockState.getBlock().getCloneItemStack(world, pos, blockState)', 'blockState.getCloneItemStack(world, pos, false)')
 p.write_text(s)
