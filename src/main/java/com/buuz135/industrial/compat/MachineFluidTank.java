package com.buuz135.industrial.compat;

import com.hrznstudio.titanium.component.IComponentHarness;
import com.hrznstudio.titanium.component.fluid.SidedFluidTankComponent;
import net.minecraft.world.item.DyeColor;
import net.neoforged.neoforge.fluids.FluidStack;
import net.neoforged.neoforge.transfer.fluid.FluidResource;
import java.util.function.Predicate;

/** A Titanium tank with the per-machine fluid validation used by IF recipes. */
public class MachineFluidTank<T extends IComponentHarness> extends SidedFluidTankComponent<T> {
    private Predicate<FluidStack> validator = stack -> true;
    public MachineFluidTank(String name, int capacity, int x, int y, int sideIndex) { super(name, capacity, x, y, sideIndex); }
    public MachineFluidTank<T> setValidator(Predicate<FluidStack> validator) { this.validator = validator; return this; }
    @Override public boolean isValid(int index, FluidResource resource) { return super.isValid(index, resource) && validator.test(resource.toStack(1)); }
    @Override public MachineFluidTank<T> setColor(DyeColor color) { super.setColor(color); return this; }
    @Override public MachineFluidTank<T> setColor(int color) { super.setColor(color); return this; }
    @Override public MachineFluidTank<T> setTankAction(Action action) { super.setTankAction(action); return this; }
    @Override public MachineFluidTank<T> setTankType(Type type) { super.setTankType(type); return this; }
    @Override public MachineFluidTank<T> setComponentHarness(T harness) { super.setComponentHarness(harness); return this; }
    @Override public MachineFluidTank<T> setOnContentChange(Runnable action) { super.setOnContentChange(action); return this; }
    @Override public MachineFluidTank<T> disableFacingAddon() { super.disableFacingAddon(); return this; }
    @Override public MachineFluidTank<T> setFacingHandlerPos(int x, int y) { super.setFacingHandlerPos(x, y); return this; }
    @Override public MachineFluidTank<T> setValidFaceModes(FaceMode... modes) { super.setValidFaceModes(modes); return this; }
}
