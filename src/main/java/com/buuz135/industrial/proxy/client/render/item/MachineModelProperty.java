package com.buuz135.industrial.proxy.client.render.item;
import com.mojang.serialization.MapCodec;
import net.minecraft.client.multiplayer.ClientLevel;
import net.minecraft.client.renderer.item.properties.numeric.RangeSelectItemModelProperty;
import net.minecraft.world.entity.ItemOwner;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
public record MachineModelProperty(boolean cooldown) implements RangeSelectItemModelProperty {
    public static final MapCodec<MachineModelProperty> COOLDOWN = MapCodec.unit(new MachineModelProperty(true));
    public static final MapCodec<MachineModelProperty> STORED = MapCodec.unit(new MachineModelProperty(false));
    @Override public float get(ItemStack stack, ClientLevel level, ItemOwner owner, int seed) {
        if (cooldown) return owner instanceof Player player && player.getCooldowns().isOnCooldown(stack) ? 1 : 2;
        return stack.has(com.buuz135.industrial.utils.IFAttachments.SETTINGS_COPIER) ? 1 : 0;
    }
    @Override public MapCodec<MachineModelProperty> type() { return cooldown ? COOLDOWN : STORED; }
}
