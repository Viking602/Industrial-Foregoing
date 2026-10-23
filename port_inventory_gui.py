from pathlib import Path
import re,ast
root=Path(__file__).resolve().parent
# Load only the reusable transformation function, not the earlier migration's top-level actions.
tree=ast.parse((root/'port_recipes_fluids.py').read_text())
fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef))
exec(compile(ast.Module(body=[fn],type_ignores=[]),'<helper>','exec'))
for f in (root/'src/main/java').rglob('*.java'):
    if '/compat/' in f.as_posix(): continue
    s=f.read_text(encoding='utf-8')
    s=s.replace('import net.neoforged.neoforge.items.ItemHandlerHelper;', 'import com.buuz135.industrial.compat.MachineItems;')
    s=s.replace('ItemHandlerHelper.', 'MachineItems.')
    s=s.replace('ItemStack.parseOptional(', 'com.buuz135.industrial.compat.ItemNbt.parseOptional(')
    s=static_calls(s,'saveOptional','com.buuz135.industrial.compat.ItemNbt')
    s=s.replace('.drawString(','.text(').replace('.renderItem(','.item(').replace('.renderFakeItem(','.fakeItem(')
    s=s.replace('.absMoveTo(','.snapTo(').replace('.noCollission()', '.noCollision()')
    s=s.replace('Tags.Items.SLIMEBALLS','Tags.Items.SLIME_BALLS')
    s=s.replace('::location','::identifier')
    if 'GuiGraphicsExtractor' in s:
        s=static_calls(s,'blit','com.buuz135.industrial.compat.MachineGui')
        s=s.replace('.blitSprite(','.blitSprite(net.minecraft.client.renderer.RenderPipelines.GUI_TEXTURED, ')
    if f.name=='WitherBuilderTile.java':
        s=s.replace('ItemStackHandler', 'com.hrznstudio.titanium.component.inventory.InventoryComponent')
        s=s.replace('import net.neoforged.neoforge.items.com.hrznstudio.titanium.component.inventory.InventoryComponent;','')
    if f.name=='ItemStackUtils.java':
        s=s.replace('isInventoryFull(ItemStackHandler handler)', 'isInventoryFull(com.hrznstudio.titanium.component.inventory.InventoryComponent<?> handler)')
    if f.name=='DissolutionChamberRecipe.java':
        s=s.replace('matches(IItemHandler handler,', 'matches(com.hrznstudio.titanium.component.inventory.InventoryComponent<?> handler,')
    f.write_text(s,encoding='utf-8')
print('Item transactions, item NBT and GUI calls migrated')
