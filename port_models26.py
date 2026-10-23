from pathlib import Path
import re,json,zipfile,hashlib,shutil
r=Path('.work/Industrial-Foregoing/src/main/java/com/buuz135/industrial/proxy/client')
p=r/'render/item/MachineModelProperty.java'
p.write_text('''package com.buuz135.industrial.proxy.client.render.item;
import com.mojang.serialization.MapCodec;
import net.minecraft.client.multiplayer.ClientLevel;
import net.minecraft.client.renderer.item.properties.numeric.RangeSelectItemModelProperty;
import net.minecraft.world.entity.ItemOwner;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
public record MachineModelProperty(boolean cooldown) implements RangeSelectItemModelProperty {
    public static final MapCodec<MachineModelProperty> COOLDOWN = MapCodec.unit(new MachineModelProperty(true));
    public static final MapCodec<MachineModelProperty> STORED = MapCodec.unit(new MachineModelProperty(false));
    @Override public float get(ItemStack stack, ClientLevel level, ItemOwner owner, int seed) {
        if (cooldown) return owner instanceof Player player && player.getCooldowns().isOnCooldown(stack) ? 1 : 2;
        return stack.has(com.buuz135.industrial.utils.IFAttachments.SETTINGS_COPIER) ? 1 : 0;
    }
    @Override public MapCodec<MachineModelProperty> type() { return cooldown ? COOLDOWN : STORED; }
}
''',encoding='utf-8')
p=r/'ClientProxy.java';s=p.read_text(encoding='utf-8');s=s.replace('    @SubscribeEvent\n    public static void itemTints(','''    @SubscribeEvent
    public static void modelProperties(net.neoforged.neoforge.client.event.RegisterRangeSelectItemModelPropertyEvent event) {
        event.register(Identifier.fromNamespaceAndPath(Reference.MOD_ID, "cooldown"), com.buuz135.industrial.proxy.client.render.item.MachineModelProperty.COOLDOWN);
        event.register(Identifier.fromNamespaceAndPath(Reference.MOD_ID, "stored"), com.buuz135.industrial.proxy.client.render.item.MachineModelProperty.STORED);
    }
    @SubscribeEvent
    public static void itemTints(''');p.write_text(s,encoding='utf-8')
for p in Path('.work/IndustrialForegoingExtraUpgrades/src/main/java/net/yxiao233/ifeu/common/compact/jei/category').glob('*.java'):
 s=p.read_text(encoding='utf-8')
 s=re.sub(r'(public void draw\([^\n]+GuiGraphicsExtractor guiGraphics[^\n]+\{)\n',r'\1\n        getBackground().draw(guiGraphics, 0, 0);\n',s)
 p.write_text(s,encoding='utf-8')
# Point dev runs at disposable, isolated instances.
p=Path('.work/IndustrialForegoingExtraUpgrades/build.gradle');s=p.read_text().replace("server { server(); programArgument '--nogui' }","server { server(); gameDirectory = file('../test-if-server-20261011'); programArgument '--nogui' }")
p.write_text(s)
test=Path('.work/test-if-server-20261011');test.mkdir(exist_ok=True)
shutil.copyfile('.work/test-server/eula.txt',test/'eula.txt')
(test/'server.properties').write_text('server-port=25637\nserver-ip=127.0.0.1\nonline-mode=false\nlevel-name=world\nlevel-type=minecraft:flat\ngenerate-structures=false\nview-distance=3\nsimulation-distance=3\nmax-players=2\n',encoding='utf-8')
# Record hashes for originals, read-only throughout this port.
report=Path('.work/verification/industrialforegoing-20261011');report.mkdir(exist_ok=True)
originals=list(Path('.').glob('*.jar'))+list(Path('../../libraries').glob('org/lwjgl/**/*.jar'))+list(Path('../../libraries').glob('net/minecraft/**/*.jar'))+list(Path('../../libraries').glob('net/neoforged/neoforge/**/*.jar'))
(report/'original-hashes.json').write_text(json.dumps({str(p.resolve()):hashlib.sha256(p.read_bytes()).hexdigest() for p in originals},indent=2))
print('Original files hashed:',len(originals))
for p in Path('../../libraries').glob('net/neoforged/neoforge/**/**universal.jar'):
 with zipfile.ZipFile(p) as z:
  masks=[n for n in z.namelist() if 'bucket' in n and ('mask' in n or n.endswith('.json'))];print(p.name,masks[:15])
