from pathlib import Path
p=Path('.work/Industrial-Foregoing/src/main/java/com/buuz135/industrial/item/infinity/InfinityTankStorage.java')
s=p.read_text()
pos=s.index('    @Override\n    public ItemStack getContainer()')
s=s[:pos]+'''    public net.neoforged.neoforge.transfer.ResourceHandler<net.neoforged.neoforge.transfer.fluid.FluidResource> asNative(net.neoforged.neoforge.transfer.access.ItemAccess access) {
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

'''+s[pos:]
p.write_text(s)
p=Path('.work/Industrial-Foregoing/src/main/java/com/buuz135/industrial/utils/IFAttachments.java')
s=p.read_text().replace('import net.neoforged.neoforge.common.util.LogicalSidedProvider;','')
s=s.replace('LogicalSidedProvider.CLIENTWORLD.get(LogicalSide.CLIENT).orElseThrow()', 'ClientLevelAccess.level()')
pos=s.index('    public static class ComponentSupplier')
s=s[:pos]+'''    private static class ClientLevelAccess {
        static net.minecraft.client.multiplayer.ClientLevel level() {
            return java.util.Objects.requireNonNull(net.minecraft.client.Minecraft.getInstance().level, "No active client world");
        }
    }

'''+s[pos:]
p.write_text(s)
p=Path('.work/Industrial-Foregoing/src/main/java/com/buuz135/industrial/module/ModuleTool.java')
s=p.read_text()
import re
s=re.sub(r'new ItemStackHarness\(stack, null, \(IButtonHandler\) stack.getItem\(\), Capabilities.EnergyStorage.ITEM, Capabilities.FluidHandler.ITEM, CapabilityItemStackHolder.ITEMSTACK_HOLDER_CAPABILITY\)', 'new com.buuz135.industrial.compat.InfinityItemHarness(stack)',s)
for name in ['trident_entity','launcher_projectile_entity','infinity_nuke']:
 s=s.replace('.build("'+name+'")','.build(net.minecraft.resources.ResourceKey.create(Registries.ENTITY_TYPE, Identifier.fromNamespaceAndPath(Reference.MOD_ID, "'+name+'")))')
s=s.replace('BlockEntityType.Builder.of(((BasicTileBlock) INFINITY_BACKPACK_BLOCK.getBlock()).getTileEntityFactory(), new Block[]{INFINITY_BACKPACK_BLOCK.getBlock()}).build((Type) null)', 'new BlockEntityType<>(((BasicTileBlock) INFINITY_BACKPACK_BLOCK.getBlock()).getTileEntityFactory(), INFINITY_BACKPACK_BLOCK.getBlock())')
s=s.replace('Capabilities.EnergyStorage','Capabilities.Energy').replace('Capabilities.FluidHandler','Capabilities.Fluid').replace('Capabilities.ItemHandler','Capabilities.Item')
s=s.replace('return itemInfinity.getEnergyConstructor(o).create();','return new com.buuz135.industrial.compat.InfinityItemEnergy(unused);')
s=s.replace('return itemInfinity.getTankConstructor(o).create();','return itemInfinity.getTankConstructor(o).create().asNative(unused);')
s=s.replace('new FluidStack(ModuleCore.MEAT.getSourceFluid().get(), 1000))), MEAT_FEEDER.get());','new FluidStack(ModuleCore.MEAT.getSourceFluid().get(), 1000))).asNative(unused), MEAT_FEEDER.get());')
s=s.replace('tile.getBackpack().getCapability(Capabilities.Fluid.ITEM)','net.neoforged.neoforge.transfer.access.ItemAccess.forStack(tile.getBackpack()).getCapability(Capabilities.Fluid.ITEM)').replace('tile.getBackpack().getCapability(Capabilities.Energy.ITEM)','net.neoforged.neoforge.transfer.access.ItemAccess.forStack(tile.getBackpack()).getCapability(Capabilities.Energy.ITEM)')
p.write_text(s)
