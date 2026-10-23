from pathlib import Path
import re
root=Path('.work/Industrial-Foregoing/src/main/java')
for p in root.rglob('*.java'):
 s=p.read_text()
 s=s.replace('import net.minecraft.world.item.EnchantedBookItem;','')
 s=s.replace('stack.getItem() instanceof EnchantedBookItem','stack.is(net.minecraft.world.item.Items.ENCHANTED_BOOK)')
 s=s.replace('.getType().is(','.getType().builtInRegistryHolder().is(')
 s=s.replace('experienceOrbEntity.value','experienceOrbEntity.getValue()')
 s=s.replace('.getMinBuildHeight()', '.getMinY()').replace('.getMaxBuildHeight()', '.getMaxY() + 1').replace('.isDay()', '.isBrightOutside()')
 s=s.replace('potion != Potions.WATER','potion != Potions.WATER.value()')
 s=s.replace('SizedIngredient.CODEC','SizedIngredient.NESTED_CODEC')
 s=s.replace('.getFoodProperties(null)', '.get(net.minecraft.core.component.DataComponents.FOOD)')
 s=s.replace('stack.getItem().getFoodProperties(stack, null)', 'stack.get(net.minecraft.core.component.DataComponents.FOOD)')
 s=s.replace('.getCraftingRemainingItem()', '.getCraftingRemainder()')
 s=re.sub(r'([\w.]+(?:\([^\n;]*?\))?)\.hasCraftingRemainingItem\(\)', r'!\1.getCraftingRemainder().isEmpty()', s)
 s=s.replace('InteractionResult.CONSUME_PARTIAL','InteractionResult.CONSUME')
 s=s.replace('InteractionResult.sidedSuccess(level.isClientSide())','InteractionResult.SUCCESS')
 if p.name in ['MobDuplicatorTile.java','WitherBuilderTile.java','InfinityTridentEntity.java','MechanicalDirtTile.java','MobImprisonmentToolItem.java']:
  s=s.replace('.moveTo(','.snapTo(')
 s=s.replace('EntityType.WITHER.create(level)', 'EntityType.WITHER.create(level, net.minecraft.world.entity.EntitySpawnReason.MOB_SUMMONED)')
 s=s.replace('EntityType.LIGHTNING_BOLT.create(this.level())', 'EntityType.LIGHTNING_BOLT.create(this.level(), net.minecraft.world.entity.EntitySpawnReason.TRIGGERED)')
 s=s.replace('type.create(world)', 'type.create(world, net.minecraft.world.entity.EntitySpawnReason.MOB_SUMMONED)')
 s=s.replace('spawnListEntry.type.create(level)', 'spawnListEntry.type().create(level, net.minecraft.world.entity.EntitySpawnReason.NATURAL)')
 s=s.replace('spawnListEntry.type,','spawnListEntry.type(),')
 s=s.replace('List<MobSpawnSettings.SpawnerData> spawnListEntries','var spawnListEntries').replace('.above()).unwrap();','.above()).unwrap().stream().map(net.minecraft.util.random.Weighted::value).toList();')
 s=s.replace('this.level.getCurrentDifficultyAt(', '((net.minecraft.server.level.ServerLevel) this.level).getCurrentDifficultyAt(')
 s=s.replace('level.getCurrentDifficultyAt(', '((net.minecraft.server.level.ServerLevel) level).getCurrentDifficultyAt(')
 s=s.replace('inputFirstCopy.getItem().isValidRepairItem(inputFirst, inputSecond)', 'inputFirstCopy.isValidRepairItem(inputSecond)')
 # NeoForge now exposes the same anvil compatibility hook on the enchantment helper.
 s=s.replace('inputFirstCopy.isBookEnchantable(inputSecond)', 'net.neoforged.neoforge.common.CommonHooks.isBookEnchantable(inputFirstCopy, inputSecond)')
 s=s.replace('.getItemInHand(hand).getResult()', '.getItemInHand(hand)')
 s=s.replace('super.use(context.getLevel(), context.getPlayer(), context.getHand()).getResult()', 'super.use(context.getLevel(), context.getPlayer(), context.getHand())')
 if 'displayClientMessage' in s:
  s=re.sub(r'\.displayClientMessage\(([^\n]+), true\)', r'.sendOverlayMessage(\1)',s)
 s=s.replace('this.spawnAtLocation(this.getPickupItem(), 0.1F)', 'this.spawnAtLocation((net.minecraft.server.level.ServerLevel) this.level(), this.getPickupItem(), 0.1F)')
 s=s.replace('player.spawnAtLocation(new ItemStack(Blocks.OBSIDIAN), player.getEyeHeight())', 'player.spawnAtLocation((net.minecraft.server.level.ServerLevel) player.level(), new ItemStack(Blocks.OBSIDIAN), player.getEyeHeight())')
 s=s.replace('if (target.hurt(damagesource, damageHit))','if (target.hurtOrSimulate(damagesource, damageHit))')
 s=s.replace('if (entity.hurt(damagesource, (float) i))','if (entity.hurtOrSimulate(damagesource, (float) i))')
 s=s.replace('net.minecraft.world.level.block.FungusBlock','net.minecraft.world.level.block.NetherFungusBlock').replace('@Mixin(FungusBlock.class)','@Mixin(NetherFungusBlock.class)')
 s=s.replace('BuiltInRegistries.ITEM.getTag(key)', 'BuiltInRegistries.ITEM.get(key)')
 s=s.replace('stack.getTags()', 'stack.getItemHolder().tags()')
 s=s.replace('chunk.setUnsaved(true)', 'chunk.markUnsaved()')
 s=s.replace('new ChunkPos(pos)', 'new ChunkPos(net.minecraft.core.SectionPos.blockToSectionCoord(pos.getX()), net.minecraft.core.SectionPos.blockToSectionCoord(pos.getZ()))')
 if p.name=='MachineCapabilities.java':
  s=s.replace('inventory.set(0, stack.copy())', 'inventory.set(0, ItemResource.of(stack), stack.getCount())').replace('inventory.getStack(0)', 'inventory.getResource(0).toStack(inventory.getAmountAsInt(0))')
 if p.name in ['IFCustomItem.java','IndustrialBlockItem.java','MachineFrameBlock.java','ItemConveyorUpgrade.java']:
  s=re.sub(r'@Override\s+(public String getCreatorModId)',r'\1',s)
 if 'proxy/network' in p.as_posix():
  if p.name in ['BackpackOpenMessage.java','ConveyorButtonInteractMessage.java','TransporterButtonInteractMessage.java']:
   s=s.replace('handleMessage(IPayloadContext', 'handleServerMessage(IPayloadContext')
  else:
   s=s.replace('protected void handleMessage(IPayloadContext', 'public void handleClientMessage(IPayloadContext')
   idx=s.rfind('}')
   s=s[:idx]+'    @Override protected void handleServerMessage(IPayloadContext context) {}\n'+s[idx:]
 if 'addon' in p.parts and 'verifyComponentsAfterLoad' in s:
  match=re.search(r'AugmentWrapper.setType\(stack, (\w+(?:\.\w+)?), (.*?)\);',s)
  t,a=match.groups();a=a.replace('this.tier','tier')
  s=s.replace('new Properties().stacksTo(16)', 'new Properties().stacksTo(16).component(AugmentWrapper.ATTACHMENT.get(), java.util.Map.of('+t+'.getType(), (float) ('+a+')))')
  s=re.sub(r'    @Override\n    public void verifyComponentsAfterLoad\(ItemStack stack\) \{.*?\n    \}\n', '',s,flags=re.S)
  s=s.replace('public String getDescriptionId()', 'public Component getName(ItemStack stack)')
  s=re.sub(r'return (Component.translatable\("item.industrialforegoing.addon"\).*?);',r'return Component.literal(\1);',s)
 s=s.replace('public void onCraftedBy(ItemStack stack, Level worldIn, Player playerIn)', 'public void onCraftedBy(ItemStack stack, Player playerIn)').replace('super.onCraftedBy(stack, worldIn, playerIn)', 'super.onCraftedBy(stack, playerIn)')
 s=s.replace('outputStack.getItem().onCraftedBy(outputStack, this.level, null)', 'outputStack.getItem().onCraftedPostProcess(outputStack, this.level)')
 if p.name=='HydroponicSimulationProcessorItem.java':
  s=s.replace('new Properties().stacksTo(1)', 'new Properties().stacksTo(1).component(IFAttachments.HYDROPONIC_SIMULATION_PROCESSOR.get(), new CompoundTag())')
  s=re.sub(r'    @Override\n    public void verifyComponentsAfterLoad\(ItemStack stack\) \{.*?\n    \}\n','',s,flags=re.S)
  s=s.replace('simulation.crop.getDescriptionId()', 'simulation.crop.getItem().getDescriptionId()').replace('stat.stack.getDescriptionId()', 'stat.stack.getItem().getDescriptionId()').replace('stat.getLong("Count")','stat.getLongOr("Count", 0L)')
 if p.name=='EntityData.java':
  s=s.replace('com.google.common.primitives.Bytes.toArray(value)', 'value').replace('value.stream().mapToInt(Integer::intValue).toArray()','value').replace('value.stream().mapToLong(Long::longValue).toArray()','value')
 if p.name=='IndustrialAreaWorkingTile.java':
  s=s.replace('new Vector3f(Math.abs(this.worldPosition.getX() % 255) / 256f, Math.abs(this.worldPosition.getY() % 255) / 256f, Math.abs(this.worldPosition.getZ() % 255) / 256f)', 'net.minecraft.util.ARGB.color(255, Math.abs(this.worldPosition.getX() % 255), Math.abs(this.worldPosition.getY() % 255), Math.abs(this.worldPosition.getZ() % 255))')
 p.write_text(s)
