from pathlib import Path

root = Path(__file__).parent / 'src/main/java/com/buuz135/industrial'
extra = Path(__file__).parent.parent / 'IndustrialForegoingExtraUpgrades/src/main/java'
M = 'com.buuz135.industrial.compat.MachineItems'

def edit(name, fn):
    files = list(root.rglob(name)) + list(extra.rglob(name))
    assert len(files) == 1, (name, files)
    p = files[0]
    old = p.read_text(encoding='utf-8')
    new = fn(old)
    assert new != old, name
    p.write_text(new, encoding='utf-8', newline='\n')

for name in ['OreLaserBaseTile', 'FluidLaserBaseTile']:
    def isolate(s, name=name):
        start = s.index('        this.addGuiAddonFactory', s.index('public void initClient()'))
        end = s.index('\n    @Override\n    public void handleButtonMessage', start)
        body = s[start:end].removesuffix('    }\n')
        body = body.replace('this.', name + '.this.')
        return s[:start] + '        new ClientUi().setup();\n    }\n\n    private final class ClientUi {\n        private void setup() {\n' + '\n'.join('    ' + line for line in body.splitlines()) + '\n        }\n    }\n' + s[end:]
    edit(name + '.java', isolate)

def feeder(s):
    s = s.replace('getFeedingItem(firstParent)', 'consumeFeedingItem(firstParent)').replace('getFeedingItem(secondParent)', 'consumeFeedingItem(secondParent)')
    s = s.replace('                    stack.shrink(1);\n', '')
    pos = s.index('    private ItemStack getFeedingItem')
    return s[:pos] + '''    private ItemStack consumeFeedingItem(Animal entity) {
        for (int slot = 0; slot < input.getSlots(); slot++) {
            ItemStack stack = input.getStackInSlot(slot);
            if (entity.isFood(stack)) {
                MachineItems.shrink(input, slot, 1);
                return stack.copyWithCount(1);
            }
        }
        return ItemStack.EMPTY;
    }

''' + s[pos:]
edit('AnimalFeederTile.java', feeder)
edit('PlantSowerTile.java', lambda s: s.replace('ItemStack stack = ItemStack.EMPTY;', 'ItemStack stack = ItemStack.EMPTY;\n            int selectedInputSlot = -1;').replace('stack = input.getInventory().getStackInSlot(i);', 'stack = input.getInventory().getStackInSlot(i);\n                    selectedInputSlot = i;').replace('stack.shrink(1);', M + '.shrink(input.getInventory(), selectedInputSlot, 1);'))
edit('PlantFertilizerTile.java', lambda s: s.replace('stack.shrink(1);', M + '.consumeFirst(fertilizer, 1);'))
for name in ['FireworkGeneratorType.java', 'PotionGeneratorType.java']:
    edit(name, lambda s: s.replace('stack.shrink(1);', M + '.shrink((SidedInventoryComponent<?>) inputs[0], 0, 1);'))
edit('FurnaceGeneratorType.java', lambda s: s.replace('itemstack.shrink(1);', 'itemstack.shrink(1);\n                ((SidedInventoryComponent<?>) inputs[0]).setStackInSlot(0, itemstack);'))
edit('DyeMixerTile.java', lambda s: s.replace('increaseBar(ItemStack stack, ProgressBarComponent bar) {', 'increaseBar(SidedInventoryComponent<?> inventory, ProgressBarComponent bar) {\n        ItemStack stack = inventory.getStackInSlot(0);').replace('increaseBar(inputRed.getStackInSlot(0),', 'increaseBar(inputRed,').replace('increaseBar(inputGreen.getStackInSlot(0),', 'increaseBar(inputGreen,').replace('increaseBar(inputBlue.getStackInSlot(0),', 'increaseBar(inputBlue,').replace('stack.shrink(1);', M + '.shrink(inventory, 0, 1);'))
for name in ['RuleControllerEntity.java', 'WeatherControllerEntity.java', 'TimeControllerEntity.java']:
    edit(name, lambda s: s.replace('stack.shrink(1);', M + '.shrink(this.input, 0, 1);'))
edit('PotionBrewerTile.java', lambda s: s.replace('ingredient.shrink(1);', M + '.shrink(brewingItems.getInventory(), slot, 1);'))
edit('MaterialStoneWorkFactoryTile.java', lambda s: s.replace('inputStack.shrink(action.getShrinkAmount());', M + '.shrink(input, slot, action.getShrinkAmount());'))
def enchants(s):
    start = s.index('public Runnable onFinish()')
    pos = s.index('        };', start)
    return s[:pos] + '            this.inputEnchantedItem.setStackInSlot(0, input);\n' + s[pos:]
edit('EnchantmentExtractorTile.java', enchants)
edit('DissolutionChamberTile.java', lambda s: s.replace('ItemStack outputStack = dissolutionChamberRecipe.output.get().copy();\n                    outputStack.getItem().onCraftedPostProcess(outputStack, this.level);\n                    MachineItems.insertItem(output, outputStack, false);', 'dissolutionChamberRecipe.output.ifPresent(result -> {\n                        ItemStack outputStack = result.copy();\n                        outputStack.getItem().onCraftedPostProcess(outputStack, this.level);\n                        MachineItems.insertItem(output, outputStack, false);\n                    });'))
print('Applied client isolation and inventory writeback fixes')
