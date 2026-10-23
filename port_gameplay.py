from pathlib import Path
import re
root=Path(__file__).resolve().parent
for f in (root/'src/main/java').rglob('*.java'):
    s=f.read_text(encoding='utf-8')
    s=s.replace('InteractionResultHolder<ItemStack>', 'net.minecraft.world.InteractionResult')
    s=s.replace('import net.minecraft.world.InteractionResultHolder;','')
    s=re.sub(r'return InteractionResultHolder\.(success|pass|consume)\([^;]+;',lambda m:'return net.minecraft.world.InteractionResult.'+m[1].upper()+';',s)
    s=s.replace('return new InteractionResultHolder(InteractionResult.SUCCESS, playerIn.getItemInHand(handIn));','return InteractionResult.SUCCESS;')
    s=s.replace('FMLEnvironment.dist.', 'FMLEnvironment.getDist().')
    s=s.replace('Screen::hasShiftDown', 'net.minecraft.client.Minecraft.getInstance()::hasShiftDown')
    s=s.replace('getInventory().selected','getInventory().getSelectedSlot()')
    s=s.replace('BlockEvent.BreakEvent', 'net.neoforged.neoforge.event.level.block.BreakBlockEvent')
    s=s.replace('getBurnTime(RecipeType.SMELTING)', 'getBurnTime(RecipeType.SMELTING, com.buuz135.industrial.utils.IFAttachments.fuelValues())')
    s=s.replace('getDescription().copy()', 'getName().copy()')
    s=s.replace('super.getDescriptionId(stack)', 'super.getDescriptionId()')
    if '/recipe/' in f.as_posix():
        s=re.sub(r'assemble\(CraftingInput (\w+), HolderLookup.Provider \w+\)',r'assemble(CraftingInput \1)',s)
        s=s.replace('RecipeSerializer<?> getSerializer()', 'RecipeSerializer getSerializer()').replace('RecipeType<?> getType()', 'RecipeType getType()')
        s=s.replace('SizedIngredient.FLAT_CODEC','SizedIngredient.CODEC')
        s=s.replace('SizedIngredient.of(tag, 1)', 'new SizedIngredient(com.buuz135.industrial.compat.Ingredients.of(tag), 1)')
        s=s.replace('new TagEmptyCondition(recipe.isTag)', 'new TagEmptyCondition(net.minecraft.tags.TagKey.create(net.minecraft.core.registries.Registries.ITEM, recipe.isTag))')
    if f.name=='EntityData.java':
        s=s.replace('tag.putUUID(key, value)', 'tag.store(key, net.minecraft.core.UUIDUtil.CODEC, value)')
        s=s.replace('tag.putByteArray(key, value)', 'tag.putByteArray(key, com.google.common.primitives.Bytes.toArray(value))')
        s=s.replace('tag.putIntArray(key, value)', 'tag.putIntArray(key, value.stream().mapToInt(Integer::intValue).toArray())')
        s=s.replace('tag.putLongArray(key, value)', 'tag.putLongArray(key, value.stream().mapToLong(Long::longValue).toArray())')
    if f.name=='LaserDrillRarity.java':
        s=s.replace('buf.readJsonWithCodec(CODEC)', 'net.minecraft.network.codec.ByteBufCodecs.fromCodecWithRegistries(CODEC).decode(buf)')
        s=s.replace('buf.writeJsonWithCodec(CODEC, laserDrillRarity)', 'net.minecraft.network.codec.ByteBufCodecs.fromCodecWithRegistries(CODEC).encode(buf, laserDrillRarity)')
        s=s.replace('level.registryAccess().registry(Registries.DIMENSION_TYPE)', 'level.registryAccess().lookup(Registries.DIMENSION_TYPE)')
        s=s.replace('registry.get(dimensionTypeResourceKey).equals(dimensionType)', 'registry.get(dimensionTypeResourceKey).map(holder -> holder.value().equals(dimensionType)).orElse(false)')
    if f.name=='HydroponicBedTile.java':
        s=s.replace('IItemHandler output', 'net.neoforged.neoforge.transfer.ResourceHandler<net.neoforged.neoforge.transfer.item.ItemResource> output')
        s=s.replace('.getWater().isEmpty()', '.getWater().getFluid().isEmpty()')
        for fluid,cap in [('water','Water'),('ether','Ether')]:
            s=re.sub(r'com\.buuz135\.industrial\.compat\.MachineFluids.drainForced\('+fluid+r', \(\(HydroponicBedTile\) tile\)\.get'+cap+r'\(\).fill\([^;]+;', 'com.buuz135.industrial.compat.MachineFluids.move('+fluid+', ((HydroponicBedTile) tile).get'+cap+'(), difference);',s)
    if f.name=='ConveyorBlock.java':
        s=s.replace('import net.minecraft.world.level.block.state.properties.DirectionProperty;', '')
        s=s.replace('DirectionProperty FACING', 'net.minecraft.world.level.block.state.properties.EnumProperty<Direction> FACING')
    f.write_text(s,encoding='utf-8')
print('Recipe serialization, interaction results, fuel and plant-machine transfer migrated')
