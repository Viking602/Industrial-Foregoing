from pathlib import Path
import re
for root in map(Path,['.work/Industrial-Foregoing/src/main/java','.work/IndustrialForegoingExtraUpgrades/src/main/java']):
 for p in root.rglob('*.java'):
  s=p.read_text(encoding='utf-8');n=s.replace('IFactory<? extends IScreenAddon>','IFactory<?>')
  n=re.sub(r'^(\s*)(.+)\.getStackInSlot\(([^()\n]*)\)\.shrink\((.*)\);$',r'\1com.buuz135.industrial.compat.MachineItems.shrink(\2, \3, \4);',n,flags=re.M)
  if n!=s:p.write_text(n,encoding='utf-8')
p=Path('.work/Industrial-Foregoing/src/main/java/com/buuz135/industrial/compat/MachineItems.java');s=p.read_text();s=s.replace('        if (inventory == null || stack.isEmpty()) return stack;','''        if (inventory == null || stack.isEmpty()) return stack;
        if (inventory instanceof com.hrznstudio.titanium.component.inventory.InventoryComponent<?> owned) return insertOwned(owned, stack, simulate);''')
s=s.replace('    public static ItemStack insertItem(ResourceHandler<ItemResource> inventory', '''    /** Machine-side insertion bypasses external automation filters, preserving stack limits. */
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
    public static ItemStack insertItem(ResourceHandler<ItemResource> inventory''')
p.write_text(s)
p=Path('.work/Industrial-Foregoing/src/main/java/com/buuz135/industrial/block/resourceproduction/tile/SporesRecreatorTile.java');p.write_text(p.read_text().replace('ItemHandlerUtil.getFirstItem(input).shrink(1);','com.buuz135.industrial.compat.MachineItems.consumeFirst(input, 1);'))
