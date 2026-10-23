from pathlib import Path
import re
root=Path('.work/Industrial-Foregoing/src/main/java/com/buuz135/industrial')
for p in (root/'plugin/jei').rglob('*.java'):
 s=p.read_text().replace('IRecipeCategory.super.draw(recipe, recipeSlotsView, guiGraphics, mouseX, mouseY);','').replace('IRecipeCategory.super.', 'com.buuz135.industrial.plugin.jei.MachineRecipeCategory.super.').replace('itemTagKey.identifier()', 'itemTagKey.location()');p.write_text(s)
p=root/'plugin/patchouli/PageDissolution.java';s=p.read_text();s=re.sub(r'        com.buuz135.industrial.compat.MachineGui.blit\(graphics, x, y, 0, 16, 16, sprite,.*?;', '        graphics.blitSprite(net.minecraft.client.renderer.RenderPipelines.GUI_TEXTURED, sprite, x, y, 16, 16, color);',s,flags=re.S);p.write_text(s)
p=root/'module/ModuleCore.java';s=p.read_text().replace('net.minecraft.world.item.crafting.display.RecipeDisplay.Type<com.buuz135.industrial.recipe.display.DissolutionRecipeDisplay>> DISSOLUTION_DISPLAY', 'net.minecraft.world.item.crafting.display.RecipeDisplay.Type<?>> DISSOLUTION_DISPLAY');p.write_text(s)
for p in root.rglob('TexturedStateButtonGuiComponent.java'):
 s=p.read_text().replace('RenderSystem.setShaderColor(1, 1, 1, 1);','');p.write_text(s)
for p in root.rglob('ContainerTransporter.java'):
 s=p.read_text().replace('new SlotItemHandler(augment,', 'new com.hrznstudio.titanium.container.addon.UpdatableSlotItemHandler(augment,');p.write_text(s)
p=root/'proxy/client/particle/ParticleVex.java';s=p.read_text().replace('import com.mojang.blaze3d.platform.GlStateManager;','');a=s.index('    public static ParticleRenderType RENDER');b=s.index('    private final Entity entity;',a);s=s[:a]+'''    public static final ParticleRenderType RENDER = new ParticleRenderType("industrialforegoing:vex_trail");

'''+s[b:];a=s.index('    @Override\n    public void render(');b=s.index('    private Direction getRandomFacing',a)
s=s[:a]+'''    private boolean hiddenInFirstPerson() {
        var player = Minecraft.getInstance().player;
        return player != null && entity == player && Minecraft.getInstance().options.getCameraType() == CameraType.FIRST_PERSON
                && entity.position().add(0, 1, 0).distanceToSqr(new Vec3(x, y, z)) < 3;
    }

    @Override public ParticleRenderType getGroup() { return RENDER; }

    public static final class Group extends net.minecraft.client.particle.ParticleGroup<ParticleVex> {
        public Group(net.minecraft.client.particle.ParticleEngine engine) { super(engine); }
        @Override public net.minecraft.client.renderer.state.level.ParticleGroupRenderState extractRenderState(
                net.minecraft.client.renderer.culling.Frustum frustum, Camera camera, float partialTick) {
            // Copy the paths now: ticking particles must not mutate a submitted frame.
            List<List<Vector3f>> trails = new ArrayList<>();
            Vec3 cameraPos = camera.position();
            for (ParticleVex particle : particles) {
                if (!particle.hiddenInFirstPerson()) trails.add(particle.lines.stream()
                        .map(point -> new Vector3f(point).sub((float)cameraPos.x, (float)cameraPos.y, (float)cameraPos.z)).toList());
            }
            return (collector, cameraState) -> collector.submitCustomGeometry(new PoseStack(), net.minecraft.client.renderer.rendertype.RenderTypes.lines(), (pose, buffer) -> {
                for (List<Vector3f> trail : trails) for (int i = 1; i < trail.size(); i++) {
                    Vector3f from = trail.get(i-1), to = trail.get(i);
                    Vector3f normal = new Vector3f(to).sub(from);
                    if (normal.lengthSquared() == 0) continue;
                    normal.normalize();
                    buffer.addVertex(pose, from.x, from.y, from.z).setColor(-1).setNormal(pose, normal.x, normal.y, normal.z).setLineWidth(1.5f);
                    buffer.addVertex(pose, to.x, to.y, to.z).setColor(-1).setNormal(pose, normal.x, normal.y, normal.z).setLineWidth(1.5f);
                }
            });
        }
    }

'''+s[b:];s=s.replace('            directions.remove(directions.size() - 1);','            if (!directions.isEmpty()) directions.removeLast();');p.write_text(s)
p=root/'proxy/client/event/IFClientEvents.java';s=p.read_text();a=s.index('    @SubscribeEvent\n    public void blockOverlayEvent');s=s[:a]+'''    @SubscribeEvent
    public void blockOverlayEvent(net.neoforged.neoforge.client.event.ExtractBlockOutlineRenderStateEvent event) {
        var player = Minecraft.getInstance().player;
        if (player == null || !(player.getMainHandItem().getItem() instanceof ItemInfinityDrill drill)) return;
        var hit = event.getHitResult();
        var area = drill.getArea(hit.getBlockPos(), hit.getDirection(), drill.getSelectedTier(player.getMainHandItem()), false);
        var world = event.getLevel();
        var camera = event.getCamera().position();
        var boxes = new java.util.ArrayList<net.minecraft.world.phys.AABB>();
        for (BlockPos pos : BlockPos.betweenClosed(area.getLeft(), area.getRight())) {
            var state = world.getBlockState(pos);
            var shape = state.getShape(world, pos);
            if (!shape.isEmpty() && !state.isAir() && state.getDestroySpeed(world, pos) >= 0 && !(state.getBlock() instanceof LiquidBlock))
                boxes.add(shape.bounds().move(pos).move(-camera.x, -camera.y, -camera.z));
        }
        event.addCustomRenderer((state, buffers, pose, translucent, levelState) -> {
            var lines = buffers.getBuffer(net.minecraft.client.renderer.rendertype.RenderTypes.lines());
            for (var box : boxes) com.buuz135.industrial.compat.RenderCompat.renderLineBox(pose, lines, box, 0, 0, 0, 0.35f);
            return true;
        });
    }
}
''';s=s.replace('import net.neoforged.neoforge.client.event.RenderHighlightEvent;','').replace('import net.neoforged.neoforge.client.event.RenderPlayerEvent;','');p.write_text(s)
# The old RenderPlayerEvent handler compared Item to a holder, so it never ran. Poses are now extracted by the renderer.
p=root/'IndustrialForegoing.java';s=p.read_text().replace('import net.minecraft.client.resources.model.ModelResourceLocation;','');a=s.index('            EventManager.mod(ModelEvent.RegisterAdditional');b=s.index('            this.initClient();',a);s=s[:a]+s[b:];a=s.index('        EventManager.mod(ModelEvent.BakingCompleted');b=s.index('        EventManager.forge(ClientTickEvent.Post.class)',a);s=s[:a]+s[b:];p.write_text(s)
