package com.buuz135.industrial.compat;

import com.buuz135.industrial.item.infinity.ItemInfinity;
import com.hrznstudio.titanium.api.IFactory;
import com.hrznstudio.titanium.capability.CapabilityItemStackHolder;
import com.hrznstudio.titanium.itemstack.ItemStackHarness;
import com.hrznstudio.titanium.network.IButtonHandler;
import net.minecraft.world.item.ItemStack;
import java.util.List;

/** Titanium's generic harness accepts context-free capabilities; item transfers need ItemAccess. */
public final class InfinityItemHarness extends ItemStackHarness {
    private final ItemStack stack;
    public InfinityItemHarness(ItemStack stack) {
        super(stack, null, (IButtonHandler) stack.getItem(), CapabilityItemStackHolder.ITEMSTACK_HOLDER_CAPABILITY);
        this.stack = stack;
    }
    @Override public List<IFactory<?>> getScreenAddons() {
        var addons = super.getScreenAddons();
        if (stack.getItem() instanceof ItemInfinity item) {
            addons.addAll(item.getEnergyConstructor(stack).create().getScreenAddons());
            addons.addAll(item.getTankConstructor(stack).create().getScreenAddons());
        }
        return addons;
    }
}
