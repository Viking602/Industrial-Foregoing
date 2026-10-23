from pathlib import Path
import re
root=Path('.work/Industrial-Foregoing/src/main/java')
for p in root.rglob('*.java'):
 s=p.read_text()
 if p.name in ['FermentationStationTile.java','FluidSievingMachineTile.java','WashingFactoryTile.java','BigSidedFluidTankComponent.java']:
  s=s.replace('protected void onContentsChanged()', 'protected void onContentsChanged(int index, net.neoforged.neoforge.fluids.FluidStack previousContents)')
 if p.name in ['ItemInfinityLauncher.java','ItemInfinityTrident.java']:
  s=s.replace('public void releaseUsing(', 'public boolean releaseUsing(')
  a=s.index('    public boolean releaseUsing(');end=s.index('\n    }',a)
  body=s[a:end]
  body=body.replace('                playerentity.awardStat(Stats.ITEM_USED.get(this));','                playerentity.awardStat(Stats.ITEM_USED.get(this));')
  s=s[:a]+body+'\n        return entityLiving instanceof Player && this.getUseDuration(stack, entityLiving) - timeLeft >= 10;'+s[end:]
 s=s.replace('getCooldowns().addCooldown(this,', 'getCooldowns().addCooldown(stack,')
 if p.name=='ItemInfinityHammer.java':
  s=s.replace('new ResolvableProfile(gameProfile)', 'ResolvableProfile.createResolved(gameProfile)')
  s=s.replace('public boolean canAttackBlock(BlockState state, Level worldIn, BlockPos pos, Player player)', 'public boolean canDestroyBlock(ItemStack stack, BlockState state, Level worldIn, BlockPos pos, LivingEntity player)')
  s=s.replace('return !player.isCreative();', 'return !(player instanceof Player p && p.isCreative());')
  s=s.replace('public boolean hurtEnemy(', 'public void hurtEnemy(')
  a=s.index('    public void hurtEnemy(');end=s.index('\n    }',a);part=s[a:end].replace('        return true;','');s=s[:a]+part+s[end:]
 if p.name=='InfinityNukeEntity.java':
  s=s.replace('this.updateInWaterStateAndDoFluidPushing()', 'this.updateFluidInteraction()')
  idx=s.rfind('}');s=s[:idx]+'''    @Override
    public boolean hurtServer(net.minecraft.server.level.ServerLevel level, net.minecraft.world.damagesource.DamageSource source, float amount) {
        // Preserve the entity's original immunity to ordinary damage; it is retrieved through interaction.
        return false;
    }
'''+s[idx:]
 if p.name=='ItemInfinityDrill.java':s=s.replace('(Player) entityLiving, true, tempState.getFluidState()', '(Player) entityLiving, stack, true, tempState.getFluidState()')
 if p.name=='MobImprisonmentToolItem.java':s=s.replace('horse.getOwnerUUID() != null','horse.getOwnerReference() != null').replace('horse.getOwnerUUID().equals(player.getUUID())','horse.getOwnerReference().getUUID().equals(player.getUUID())')
 if p.name=='ItemConveyorUpgrade.java':
  s=s.replace('public String getDescriptionId(ItemStack stack)', 'public net.minecraft.network.chat.Component getName(ItemStack stack)')
  s=s.replace('return "conveyor.upgrade.error";', 'return net.minecraft.network.chat.Component.translatable("conveyor.upgrade.error");')
  s=s.replace('return String.format("conveyor.upgrade.%s.%s", BuiltInRegistries.ITEM.getKey(factory.getUpgradeItem()).getNamespace(), BuiltInRegistries.ITEM.getKey(factory.getUpgradeItem()).getPath());', 'return net.minecraft.network.chat.Component.translatable(String.format("conveyor.upgrade.%s.%s", BuiltInRegistries.ITEM.getKey(factory.getUpgradeItem()).getNamespace(), BuiltInRegistries.ITEM.getKey(factory.getUpgradeItem()).getPath()));')
 if p.name=='ItemInfinityBackpack.java':
  s=s.replace('CustomData customdata = (CustomData) stack.getOrDefault(DataComponents.BLOCK_ENTITY_DATA, CustomData.EMPTY);','var customdata = stack.get(DataComponents.BLOCK_ENTITY_DATA);').replace('if (!customdata.isEmpty())', 'if (customdata != null && blockentity != null && customdata.type() == blockentity.getType())').replace('blockentity.onlyOpCanSetNbt()', 'blockentity.getType().onlyOpCanSetNbt()')
 if p.name=='MilkStrawHandler.java':s=s.replace('import net.neoforged.neoforge.common.EffectCures;','').replace('player.removeEffectsCuredBy(EffectCures.MILK)', 'player.removeAllEffects()')
 if p.name=='InfinityLauncherProjectileEntity.java':s=s.replace('ClientboundGameEventPacket.ARROW_HIT_PLAYER','ClientboundGameEventPacket.PLAY_ARROW_HIT_SOUND')
 if p.name=='ColorUtils.java':s=s.replace('getUniqueFrames().count()', 'getUniqueFrames().size()')
 if p.name=='TransporterFluidType.java':
  s=s.replace('(CompoundTag) com.buuz135.industrial.compat.ItemNbt.saveOptional(stack, getLevel().registryAccess())', '(CompoundTag) FluidStack.CODEC.encodeStart(getLevel().registryAccess().createSerializationContext(net.minecraft.nbt.NbtOps.INSTANCE), stack).getOrThrow()')
  s=s.replace('FluidStack.parseOptional(getLevel().registryAccess(), compoundNBT)', 'FluidStack.CODEC.parse(getLevel().registryAccess().createSerializationContext(net.minecraft.nbt.NbtOps.INSTANCE), compoundNBT).result().orElse(FluidStack.EMPTY)')
 if p.name=='OreFluidInstance.java':
  s=s.replace('            @Override\n            public void initializeClient', '            public void initializeClient')
 if p.name in ['MeatFeedCurios.java','InfinityBackpackCurios.java']:
  s=s.replace('ModuleTool.MEAT_FEEDER.get().inventoryTick(stack, slotContext.entity().level(), slotContext.entity(), 0, false);', 'if (slotContext.entity().level() instanceof net.minecraft.server.level.ServerLevel serverLevel) ModuleTool.MEAT_FEEDER.get().inventoryTick(stack, serverLevel, slotContext.entity(), null);').replace('ModuleTool.INFINITY_BACKPACK.get().inventoryTick(stack, livingEntity.level(), livingEntity, 0, false);','if (livingEntity.level() instanceof net.minecraft.server.level.ServerLevel serverLevel) ModuleTool.INFINITY_BACKPACK.get().inventoryTick(stack, serverLevel, livingEntity, null);')
 p.write_text(s)
