package com.buuz135.industrial.compat;

import com.buuz135.industrial.item.infinity.InfinityTier;
import com.buuz135.industrial.utils.IFAttachments;
import net.minecraft.world.item.Item;
import net.neoforged.neoforge.transfer.TransferPreconditions;
import net.neoforged.neoforge.transfer.access.ItemAccess;
import net.neoforged.neoforge.transfer.energy.EnergyHandler;
import net.neoforged.neoforge.transfer.transaction.TransactionContext;

/** Long-valued energy stored on the item in its actual inventory location. */
public final class InfinityItemEnergy implements EnergyHandler {
    private final ItemAccess access;
    private final Item item;
    public InfinityItemEnergy(ItemAccess access) {
        this.access = access;
        this.item = access.getResource().getItem();
    }
    private boolean valid() { return access.getAmount() == 1 && access.getResource().is(item); }
    @Override public long getAmountAsLong() {
        return valid() ? Math.clamp(access.getResource().getOrDefault(IFAttachments.INFINITY_ITEM_POWER.get(), 0L), 0L, getCapacityAsLong()) : 0;
    }
    @Override public long getCapacityAsLong() { return valid() ? InfinityTier.ARTIFACT.getPowerNeeded() : 0; }
    @Override public int insert(int amount, TransactionContext transaction) {
        TransferPreconditions.checkNonNegative(amount);
        if (!valid() || !access.getResource().getOrDefault(IFAttachments.INFINITY_ITEM_CAN_CHARGE.get(), true)) return 0;
        long stored = getAmountAsLong();
        int moved = (int) Math.min(amount, getCapacityAsLong() - stored);
        return moved == 0 ? 0 : moved * access.exchange(access.getResource().with(IFAttachments.INFINITY_ITEM_POWER.get(), stored + moved), 1, transaction);
    }
    @Override public int extract(int amount, TransactionContext transaction) {
        TransferPreconditions.checkNonNegative(amount);
        if (!valid()) return 0;
        long stored = getAmountAsLong();
        int moved = (int) Math.min(amount, stored);
        return moved == 0 ? 0 : moved * access.exchange(access.getResource().with(IFAttachments.INFINITY_ITEM_POWER.get(), stored - moved), 1, transaction);
    }
}
