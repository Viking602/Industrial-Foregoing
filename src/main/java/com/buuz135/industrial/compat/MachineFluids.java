package com.buuz135.industrial.compat;

import com.hrznstudio.titanium.component.fluid.FluidTankComponent;
import net.neoforged.neoforge.fluids.FluidStack;
import net.neoforged.neoforge.fluids.capability.IFluidHandler.FluidAction;
import net.neoforged.neoforge.transfer.fluid.FluidResource;
import net.neoforged.neoforge.transfer.transaction.Transaction;

/** Internal machine operations bypass side permissions while preserving transaction semantics. */
public final class MachineFluids {
    private MachineFluids() {}
    public static int fillForced(FluidTankComponent<?> tank, FluidStack stack, FluidAction action) {
        if (stack.isEmpty()) return 0;
        try (var transaction = Transaction.openRoot()) {
            int inserted = tank.insertForced(FluidResource.of(stack), stack.getAmount(), transaction);
            if (action.execute()) transaction.commit();
            return inserted;
        }
    }
    public static FluidStack drainForced(FluidTankComponent<?> tank, int amount, FluidAction action) {
        if (amount <= 0 || tank.getFluid().isEmpty()) return FluidStack.EMPTY;
        FluidResource fluid = tank.getResource(0);
        try (var transaction = Transaction.openRoot()) {
            int extracted = tank.extractForced(fluid, amount, transaction);
            if (action.execute()) transaction.commit();
            return fluid.toStack(extracted);
        }
    }
    public static FluidStack drainForced(FluidTankComponent<?> tank, FluidStack stack, FluidAction action) {
        return FluidResource.of(stack).equals(tank.getResource(0)) ? drainForced(tank, stack.getAmount(), action) : FluidStack.EMPTY;
    }
    public static int move(FluidTankComponent<?> source, FluidTankComponent<?> destination, int amount) {
        if (amount <= 0 || source.getFluid().isEmpty()) return 0;
        FluidResource fluid = source.getResource(0);
        try (var transaction = Transaction.openRoot()) {
            int available = source.extractForced(fluid, amount, transaction);
            int inserted = destination.insert(fluid, available, transaction);
            if (inserted < available && source.insertForced(fluid, available - inserted, transaction) != available - inserted) {
                return 0; // Closing without commit restores both tanks.
            }
            transaction.commit();
            return inserted;
        }
    }
}
