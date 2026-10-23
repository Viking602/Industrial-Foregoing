package com.buuz135.industrial.compat;

import net.minecraft.core.HolderLookup;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.util.ProblemReporter;
import net.minecraft.world.level.storage.TagValueInput;
import net.minecraft.world.level.storage.TagValueOutput;
import net.neoforged.neoforge.common.util.ValueIOSerializable;

public final class ValueNbt {
    private ValueNbt() {}
    public static CompoundTag save(ValueIOSerializable value, HolderLookup.Provider registries) {
        var output = TagValueOutput.createWithContext(ProblemReporter.DISCARDING, registries);
        value.serialize(output);
        return output.buildResult();
    }
    public static <T extends ValueIOSerializable> T load(T value, HolderLookup.Provider registries, CompoundTag tag) {
        value.deserialize(TagValueInput.create(ProblemReporter.DISCARDING, registries, tag));
        return value;
    }
}
