from pathlib import Path
p=Path('.work/Industrial-Foregoing/src/main/java/com/buuz135/industrial/worlddata/BackpackDataManager.java')
s=p.read_text().replace('implements IItemHandler, INBTSerializable<CompoundTag>', 'implements IItemHandler, INBTSerializable<CompoundTag>, net.neoforged.neoforge.transfer.ResourceHandler<net.neoforged.neoforge.transfer.item.ItemResource>')
s=s.replace('new Factory<>(BackpackDataManager::new, (compoundTag, provider) -> BackpackDataManager.load(provider, compoundTag)), NAME', 'TYPE')
s=s.replace('    @Override\n    public CompoundTag save', '    public CompoundTag save')
s=s.replace('    public static final String NAME = "IFBackpack";', '''    public static final String NAME = "IFBackpack";
    public static final net.minecraft.world.level.saveddata.SavedDataType<BackpackDataManager> TYPE = new net.minecraft.world.level.saveddata.SavedDataType<>(
            net.minecraft.resources.Identifier.fromNamespaceAndPath("industrialforegoing", "backpacks"),
            level -> new BackpackDataManager(),
            level -> CompoundTag.CODEC.xmap(tag -> load(level.registryAccess(), tag), data -> data.save(new CompoundTag(), level.registryAccess())));''')
pos=s.index('        public BackpackItemHandler(BackpackDataManager manager)')
s=s[:pos]+'''        private record SlotSnapshot(ItemStack stack, int amount, boolean voidItems, boolean refillItems) {}
        private final net.neoforged.neoforge.transfer.transaction.SnapshotJournal<List<SlotSnapshot>> journal = new net.neoforged.neoforge.transfer.transaction.SnapshotJournal<>() {
            @Override protected List<SlotSnapshot> createSnapshot() {
                return definitionList.stream().map(d -> new SlotSnapshot(d.stack.copy(), d.amount, d.voidItems, d.refillItems)).toList();
            }
            @Override protected void revertToSnapshot(List<SlotSnapshot> snapshot) {
                for (int i = 0; i < snapshot.size(); i++) {
                    var before = snapshot.get(i);
                    var current = definitionList.get(i);
                    current.stack = before.stack();
                    current.amount = before.amount();
                    current.voidItems = before.voidItems();
                    current.refillItems = before.refillItems();
                }
            }
            @Override protected void onRootCommit(List<SlotSnapshot> snapshot) { markDirty(); }
        };
        @Override public int size() { return getSlots(); }
        @Override public net.neoforged.neoforge.transfer.item.ItemResource getResource(int index) {
            return definitionList.get(index).amount == 0 ? net.neoforged.neoforge.transfer.item.ItemResource.EMPTY : net.neoforged.neoforge.transfer.item.ItemResource.of(definitionList.get(index).stack);
        }
        @Override public long getAmountAsLong(int index) { return definitionList.get(index).amount; }
        @Override public long getCapacityAsLong(int index, net.neoforged.neoforge.transfer.item.ItemResource resource) {
            return resource.isEmpty() || isValid(index, resource) ? maxAmount : 0;
        }
        @Override public boolean isValid(int index, net.neoforged.neoforge.transfer.item.ItemResource resource) { return isItemValid(index, resource.toStack()); }
        @Override public int insert(int index, net.neoforged.neoforge.transfer.item.ItemResource resource, int amount, net.neoforged.neoforge.transfer.transaction.TransactionContext transaction) {
            net.neoforged.neoforge.transfer.TransferPreconditions.checkNonEmptyNonNegative(resource, amount);
            if (!isValid(index, resource) || amount == 0) return 0;
            var slot = definitionList.get(index);
            int accepted = slot.voidItems ? amount : (int) Math.min(amount, Math.max(0L, (long) maxAmount - slot.amount));
            if (accepted > 0) {
                journal.updateSnapshots(transaction);
                slot.stack = resource.toStack();
                slot.amount = (int) Math.min(maxAmount, (long) slot.amount + accepted);
            }
            return accepted;
        }
        @Override public int extract(int index, net.neoforged.neoforge.transfer.item.ItemResource resource, int amount, net.neoforged.neoforge.transfer.transaction.TransactionContext transaction) {
            net.neoforged.neoforge.transfer.TransferPreconditions.checkNonEmptyNonNegative(resource, amount);
            if (!resource.equals(getResource(index))) return 0;
            var slot = definitionList.get(index);
            int extracted = Math.min(amount, slot.amount);
            if (extracted > 0) { journal.updateSnapshots(transaction); slot.amount -= extracted; }
            return extracted;
        }

'''+s[pos:]
s=s.replace('if (dataManager != null) dataManager.setDirty();','if (dataManager != null && !journal.isInTransaction()) dataManager.setDirty();')
s=s.replace('Math.min(maxAmount - definition.getAmount(), stack.getCount())','(int) Math.min(Math.max(0L, (long) maxAmount - definition.getAmount()), stack.getCount())')
s=s.replace('Math.min(definition.getAmount() + inserted, maxAmount)','(int) Math.min((long) definition.getAmount() + inserted, maxAmount)')
p.write_text(s)
