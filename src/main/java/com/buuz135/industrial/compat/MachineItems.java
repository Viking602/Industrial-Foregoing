package com.buuz135.industrial.compat;

import net.minecraft.world.item.ItemStack;
import net.neoforged.neoforge.transfer.ResourceHandler;
import net.neoforged.neoforge.transfer.ResourceHandlerUtil;
import net.neoforged.neoforge.transfer.item.ItemResource;
import net.neoforged.neoforge.transfer.transaction.Transaction;

/** Preserves the remainder-stack contract while using the new resource transfer API. */
public class MachineItems extends net.neoforged.neoforge.items.ItemHandlerHelper {    public static net.minecraft.world.item.ItemStack getCraftingRemainder(net.minecraft.world.item.ItemStack stack) {
        var remainder = stack.getCraftingRemainder();
        return remainder == null ? net.minecraft.world.item.ItemStack.EMPTY : remainder.create();
    }

    /** Machine-side insertion bypasses external automation filters, preserving stack limits. */
    private static ItemStack insertOwned(com.hrznstudio.titanium.component.inventory.InventoryComponent<?> inventory, ItemStack stack, boolean simulate) {
        int remaining = stack.getCount();
        var resource = ItemResource.of(stack);
        for (int pass = 0; pass < 2; pass++) for (int slot = 0; slot < inventory.size() && remaining > 0; slot++) {
            var existing = inventory.getResource(slot);
            if (pass == 0 ? existing.isEmpty() || !existing.equals(resource) : !existing.isEmpty()) continue;
            int amount = inventory.getAmountAsInt(slot);
            int limit = Math.min(inventory.getSlotLimit(slot), stack.getMaxStackSize());
            int moved = Math.min(remaining, Math.max(0, limit - amount));
            if (moved > 0) {
                if (!simulate) inventory.set(slot, resource, amount + moved);
                remaining -= moved;
            }
        }
        return stack.copyWithCount(remaining);
    }
    public static void shrink(ResourceHandler<ItemResource> inventory, int slot, int amount) {
        if (amount < 0) throw new IllegalArgumentException("Negative consumption");
        var resource = inventory.getResource(slot);
        if (inventory instanceof net.neoforged.neoforge.transfer.item.ItemStacksResourceHandler owned) {
            owned.set(slot, resource, Math.max(0, inventory.getAmountAsInt(slot) - amount));
        } else if (!resource.isEmpty()) {
            try (var tx = Transaction.openRoot()) { inventory.extract(slot, resource, amount, tx); tx.commit(); }
        }
    }
    public static void shrink(net.neoforged.neoforge.items.IItemHandler inventory, int slot, int amount) {
        var stack = inventory.getStackInSlot(slot).copy();
        stack.shrink(amount);
        if (inventory instanceof net.neoforged.neoforge.items.IItemHandlerModifiable owned) owned.setStackInSlot(slot, stack);
        else inventory.extractItem(slot, amount, false);
    }
    public static void consumeFirst(ResourceHandler<ItemResource> inventory, int amount) {
        for (int slot = 0; slot < inventory.size(); slot++) if (!inventory.getResource(slot).isEmpty()) { shrink(inventory, slot, amount); return; }
    }
    public static ItemStack insertItem(ResourceHandler<ItemResource> inventory, ItemStack stack, boolean simulate) {
        if (inventory == null || stack.isEmpty()) return stack;
        if (inventory instanceof com.hrznstudio.titanium.component.inventory.InventoryComponent<?> owned) return insertOwned(owned, stack, simulate);
        try (var transaction = Transaction.openRoot()) {
            int inserted = inventory.insert(ItemResource.of(stack), stack.getCount(), transaction);
            if (!simulate) transaction.commit();
            return stack.copyWithCount(stack.getCount() - inserted);
        }
    }
    public static ItemStack insertItemStacked(ResourceHandler<ItemResource> inventory, ItemStack stack, boolean simulate) {
        if (inventory == null || stack.isEmpty()) return stack;
        if (inventory instanceof com.hrznstudio.titanium.component.inventory.InventoryComponent<?> owned) return insertOwned(owned, stack, simulate);
        try (var transaction = Transaction.openRoot()) {
            int inserted = ResourceHandlerUtil.insertStacking(inventory, ItemResource.of(stack), stack.getCount(), transaction);
            if (!simulate) transaction.commit();
            return stack.copyWithCount(stack.getCount() - inserted);
        }
    }
}
