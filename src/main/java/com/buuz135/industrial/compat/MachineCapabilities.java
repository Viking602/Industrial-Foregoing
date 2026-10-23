package com.buuz135.industrial.compat;

import com.buuz135.industrial.item.infinity.ItemInfinity;
import com.buuz135.industrial.item.infinity.InfinityTankStorage;
import com.buuz135.industrial.module.ModuleCore;
import com.buuz135.industrial.module.ModuleTool;
import com.hrznstudio.titanium.component.fluid.FluidTankComponent;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.neoforged.neoforge.capabilities.Capabilities;
import net.neoforged.neoforge.fluids.FluidStack;
import net.neoforged.neoforge.fluids.capability.IFluidHandler;
import net.neoforged.neoforge.fluids.capability.IFluidHandlerItem;
import net.neoforged.neoforge.items.IItemHandler;
import net.neoforged.neoforge.transfer.ResourceHandler;
import net.neoforged.neoforge.transfer.access.ItemAccess;
import net.neoforged.neoforge.transfer.energy.EnergyHandler;
import net.neoforged.neoforge.transfer.fluid.FluidResource;
import net.neoforged.neoforge.transfer.item.ItemResource;
import net.neoforged.neoforge.transfer.item.ItemStacksResourceHandler;
import net.neoforged.neoforge.transfer.transaction.Transaction;

/** Adapts remaining simulate/execute machine logic to the native transactional capabilities. */
public final class MachineCapabilities {
    private MachineCapabilities() {}
    public static IItemHandler items(Level level, BlockPos pos, Direction side) { return items(level.getCapability(Capabilities.Item.BLOCK, pos, side)); }
    public static IFluidHandler fluids(Level level, BlockPos pos, Direction side) { return fluids(level.getCapability(Capabilities.Fluid.BLOCK, pos, side)); }
    public static IItemHandler items(ResourceHandler<ItemResource> handler) {
        if (handler == null) return null;
        return new IItemHandler() {
            public int getSlots() { return handler.size(); }
            public ItemStack getStackInSlot(int slot) { return handler.getResource(slot).toStack(handler.getAmountAsInt(slot)); }
            public int getSlotLimit(int slot) { return handler.getCapacityAsInt(slot, ItemResource.EMPTY); }
            public boolean isItemValid(int slot, ItemStack stack) { return !stack.isEmpty() && handler.isValid(slot, ItemResource.of(stack)); }
            public ItemStack insertItem(int slot, ItemStack stack, boolean simulate) {
                if (stack.isEmpty()) return ItemStack.EMPTY;
                try (var tx = Transaction.openRoot()) {
                    int inserted = handler.insert(slot, ItemResource.of(stack), stack.getCount(), tx);
                    if (!simulate) tx.commit();
                    return stack.copyWithCount(stack.getCount() - inserted);
                }
            }
            public ItemStack extractItem(int slot, int amount, boolean simulate) {
                var resource = handler.getResource(slot);
                if (resource.isEmpty() || amount <= 0) return ItemStack.EMPTY;
                try (var tx = Transaction.openRoot()) {
                    int extracted = handler.extract(slot, resource, amount, tx);
                    if (!simulate) tx.commit();
                    return resource.toStack(extracted);
                }
            }
        };
    }
    public static IFluidHandler fluids(ResourceHandler<FluidResource> handler) { return handler == null ? null : new FluidView(handler); }
    public static IFluidHandlerItem fluids(ItemStack stack) {
        if (stack.isEmpty()) return null;
        if (stack.getItem() instanceof ItemInfinity item) return item.getTankConstructor(stack).create();
        if (stack.is(ModuleTool.MEAT_FEEDER.get())) return new InfinityTankStorage(stack, new InfinityTankStorage.TankDefinition("meat", 512_000, 0, 0,
                fluid -> fluid.is(ModuleCore.MEAT.getSourceFluid()), true, true, FluidTankComponent.Type.SMALL, new FluidStack(ModuleCore.MEAT.getSourceFluid().get(), 1000)));
        // Keep replacement containers (e.g. milk bucket -> bucket) accessible to the caller.
        var inventory = new ItemStacksResourceHandler(1);
        inventory.set(0, ItemResource.of(stack), stack.getCount());
        var access = ItemAccess.forHandlerIndexStrict(inventory, 0);
        var handler = access.getCapability(Capabilities.Fluid.ITEM);
        return handler == null ? null : new ItemFluidView(handler, inventory);
    }
    public static EnergyHandler energy(ItemStack stack) {
        if (stack.isEmpty()) return null;
        if (stack.getItem() instanceof ItemInfinity item) return item.getEnergyConstructor(stack).create();
        return ItemAccess.forStack(stack).getCapability(Capabilities.Energy.ITEM);
    }
    private static class FluidView implements IFluidHandler {
        protected final ResourceHandler<FluidResource> handler;
        FluidView(ResourceHandler<FluidResource> handler) { this.handler = handler; }
        public int getTanks() { return handler.size(); }
        public FluidStack getFluidInTank(int tank) { return handler.getResource(tank).toStack(handler.getAmountAsInt(tank)); }
        public int getTankCapacity(int tank) { return handler.getCapacityAsInt(tank, FluidResource.EMPTY); }
        public boolean isFluidValid(int tank, FluidStack stack) { return !stack.isEmpty() && handler.isValid(tank, FluidResource.of(stack)); }
        public int fill(FluidStack stack, FluidAction action) {
            if (stack.isEmpty()) return 0;
            try (var tx = Transaction.openRoot()) {
                int inserted = handler.insert(FluidResource.of(stack), stack.getAmount(), tx);
                if (action.execute()) tx.commit();
                return inserted;
            }
        }
        public FluidStack drain(FluidStack stack, FluidAction action) {
            if (stack.isEmpty()) return FluidStack.EMPTY;
            try (var tx = Transaction.openRoot()) {
                int extracted = handler.extract(FluidResource.of(stack), stack.getAmount(), tx);
                if (action.execute()) tx.commit();
                return stack.copyWithAmount(extracted);
            }
        }
        public FluidStack drain(int amount, FluidAction action) {
            if (amount <= 0) return FluidStack.EMPTY;
            for (int i = 0; i < handler.size(); i++) {
                var resource = handler.getResource(i);
                if (resource.isEmpty()) continue;
                var drained = drain(resource.toStack(amount), action);
                if (!drained.isEmpty()) return drained;
            }
            return FluidStack.EMPTY;
        }
    }
    private static final class ItemFluidView extends FluidView implements IFluidHandlerItem {
        private final ItemStacksResourceHandler inventory;
        ItemFluidView(ResourceHandler<FluidResource> handler, ItemStacksResourceHandler inventory) { super(handler); this.inventory = inventory; }
        public ItemStack getContainer() { return inventory.getResource(0).toStack(inventory.getAmountAsInt(0)); }
    }
}
