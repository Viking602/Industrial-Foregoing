package com.buuz135.industrial.compat;

import net.minecraft.core.HolderLookup;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.nbt.NbtOps;
import net.minecraft.nbt.Tag;
import net.minecraft.world.item.ItemStack;

/** Registry-aware item persistence for inventory filters and machine state. */
public final class ItemNbt {
    private ItemNbt() {}
    public static Tag saveOptional(ItemStack stack, HolderLookup.Provider registries) {
        return ItemStack.OPTIONAL_CODEC.encodeStart(registries.createSerializationContext(NbtOps.INSTANCE), stack).getOrThrow();
    }
    public static ItemStack parseOptional(HolderLookup.Provider registries, CompoundTag tag) {
        return ItemStack.OPTIONAL_CODEC.parse(registries.createSerializationContext(NbtOps.INSTANCE), tag).resultOrPartial(
            error -> com.buuz135.industrial.IndustrialForegoing.LOGGER.warn("Cannot read stored item: {}", error)).orElse(ItemStack.EMPTY);
    }
}
