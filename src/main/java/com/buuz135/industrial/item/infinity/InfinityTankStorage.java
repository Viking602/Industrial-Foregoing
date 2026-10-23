package com.buuz135.industrial.item.infinity;

import com.buuz135.industrial.gui.component.ItemStackTankScreenAddon;
import com.buuz135.industrial.utils.IFAttachments;
import com.hrznstudio.titanium.api.IFactory;
import com.hrznstudio.titanium.api.client.IScreenAddon;
import com.hrznstudio.titanium.api.client.IScreenAddonProvider;
import com.hrznstudio.titanium.component.fluid.FluidTankComponent;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.world.item.ItemStack;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.api.distmarker.OnlyIn;
import net.neoforged.neoforge.fluids.FluidStack;
import net.neoforged.neoforge.fluids.capability.IFluidHandlerItem;
import net.neoforged.neoforge.fluids.capability.templates.FluidTank;
import org.jetbrains.annotations.NotNull;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.function.Predicate;

public class InfinityTankStorage implements IFluidHandlerItem, IScreenAddonProvider {


    private final ItemStack stack;
    private List<TankDefinition> tanks;
    private HashMap<String, FluidTank> tankMap;

    public InfinityTankStorage(ItemStack stack, TankDefinition... tanks) {
        this.stack = stack;
        this.tanks = List.of(tanks);
        this.tankMap = new HashMap<>();
        var component = stack.getOrDefault(IFAttachments.INFINITY_TANKS, new CompoundTag());
        for (TankDefinition tankDefinition : this.tanks) {
            var tank = new FluidTank(tankDefinition.capacity(), tankDefinition.filter());
            if (component.contains(tankDefinition.name())) {
                var data = component.getCompoundOrEmpty(tankDefinition.name());
                if (!data.contains("Fluid") && data.contains("id")) {
                    var wrapped = new CompoundTag();
                    wrapped.put("Fluid", data.copy());
                    data = wrapped;
                }
                tank = com.buuz135.industrial.compat.ValueNbt.load(tank, IFAttachments.registryAccess(), data);
            }
            tankMap.put(tankDefinition.name(), tank);
        }
    }

    public net.neoforged.neoforge.transfer.ResourceHandler<net.neoforged.neoforge.transfer.fluid.FluidResource> asNative(net.neoforged.neoforge.transfer.access.ItemAccess access) {
        var validItem = stack.getItem();
        return new net.neoforged.neoforge.transfer.ItemAccessResourceHandler<net.neoforged.neoforge.transfer.fluid.FluidResource>(access, tanks.size()) {
            private FluidStack fluid(net.neoforged.neoforge.transfer.item.ItemResource resource, int index) {
                return resource.is(validItem) ? new InfinityTankStorage(resource.toStack(), tanks.toArray(TankDefinition[]::new)).getFluidInTank(index) : FluidStack.EMPTY;
            }
            @Override protected net.neoforged.neoforge.transfer.fluid.FluidResource getResourceFrom(net.neoforged.neoforge.transfer.item.ItemResource resource, int index) {
                return net.neoforged.neoforge.transfer.fluid.FluidResource.of(fluid(resource, index));
            }
            @Override protected int getAmountFrom(net.neoforged.neoforge.transfer.item.ItemResource resource, int index) { return fluid(resource, index).getAmount(); }
            @Override protected int getCapacity(int index, net.neoforged.neoforge.transfer.fluid.FluidResource resource) { return itemAccess.getResource().is(validItem) ? tanks.get(index).capacity() : 0; }
            @Override public boolean isValid(int index, net.neoforged.neoforge.transfer.fluid.FluidResource resource) {
                return itemAccess.getResource().is(validItem) && tanks.get(index).filter().test(resource.toStack(1));
            }
            @Override protected net.neoforged.neoforge.transfer.item.ItemResource update(net.neoforged.neoforge.transfer.item.ItemResource resource, int index, net.neoforged.neoforge.transfer.fluid.FluidResource fluid, int amount) {
                var copy = resource.toStack();
                var storage = new InfinityTankStorage(copy, tanks.toArray(TankDefinition[]::new));
                storage.tankMap.get(tanks.get(index).name()).setFluid(fluid.toStack(amount));
                storage.save();
                return net.neoforged.neoforge.transfer.item.ItemResource.of(copy);
            }
            @Override public int insert(int index, net.neoforged.neoforge.transfer.fluid.FluidResource resource, int amount, net.neoforged.neoforge.transfer.transaction.TransactionContext transaction) {
                return tanks.get(index).insert() ? super.insert(index, resource, amount, transaction) : 0;
            }
            @Override public int extract(int index, net.neoforged.neoforge.transfer.fluid.FluidResource resource, int amount, net.neoforged.neoforge.transfer.transaction.TransactionContext transaction) {
                return tanks.get(index).extract() ? super.extract(index, resource, amount, transaction) : 0;
            }
        };
    }

    @Override
    public ItemStack getContainer() {
        return stack;
    }

    @Override
    public int getTanks() {
        return this.tanks.size();
    }

    @Override
    public FluidStack getFluidInTank(int i) {
        return this.tankMap.get(this.tanks.get(i).name()).getFluid();
    }

    @Override
    public int getTankCapacity(int i) {
        return tanks.get(i).capacity();
    }

    @Override
    public boolean isFluidValid(int i, FluidStack fluidStack) {
        return this.tankMap.get(this.tanks.get(i).name()).isFluidValid(fluidStack);
    }

    @Override
    public int fill(FluidStack fluidStack, FluidAction fluidAction) {
        for (TankDefinition tankDefinition : this.tanks) {
            if (!tankDefinition.insert()) continue;
            var tank = tankMap.get(tankDefinition.name());
            var filled = tank.fill(fluidStack, fluidAction);
            if (filled > 0) {
                if (fluidAction.execute()) {
                    save();
                }
                return filled;
            }
        }
        return 0;
    }

    @Override
    public FluidStack drain(FluidStack fluidStack, FluidAction fluidAction) {
        for (TankDefinition tankDefinition : this.tanks) {
            if (!tankDefinition.extract()) continue;
            var tank = tankMap.get(tankDefinition.name());
            var drained = tank.drain(fluidStack, fluidAction);
            if (!drained.isEmpty()) {
                if (fluidAction.execute()) {
                    save();
                }
                return drained;
            }
        }
        return FluidStack.EMPTY;
    }

    @Override
    public FluidStack drain(int i, FluidAction fluidAction) {
        for (TankDefinition tankDefinition : this.tanks) {
            if (!tankDefinition.extract()) continue;
            var tank = tankMap.get(tankDefinition.name());
            var drained = tank.drain(i, fluidAction);
            if (!drained.isEmpty()) {
                if (fluidAction.execute()) {
                    save();
                }
                return drained;
            }
        }
        return FluidStack.EMPTY;
    }

    public void save() {
        var component = new CompoundTag();
        for (TankDefinition tankDefinition : this.tanks) {
            var tank = tankMap.get(tankDefinition.name());
            component.put(tankDefinition.name(), com.buuz135.industrial.compat.ValueNbt.save(tank, IFAttachments.registryAccess()));
        }
        this.stack.set(IFAttachments.INFINITY_TANKS, component);
    }

    @Override
    public @NotNull List<IFactory<?>> getScreenAddons() {
        List<IFactory<?>> list = new ArrayList<>();
        for (int i = 0; i < this.tanks.size(); i++) {
            var tankDefinition = this.tanks.get(i);
            int finalI = i;
            list.add(() -> new ItemStackTankScreenAddon(tankDefinition.x, tankDefinition.y, this, finalI, tankDefinition.type, tankDefinition.definedFluidStack));
        }
        return list;
    }

    public record TankDefinition(String name, int capacity, int x, int y, Predicate<FluidStack> filter, boolean extract,
                                 boolean insert, FluidTankComponent.Type type, FluidStack definedFluidStack) {
    }
}
