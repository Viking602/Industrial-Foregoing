from pathlib import Path
root=Path('.work/Industrial-Foregoing/src/main/java/com/buuz135/industrial')
(root/'proxy/client/render/item/IndustrialForegoingISTER.java').write_text('''package com.buuz135.industrial.proxy.client.render.item;
import com.mojang.blaze3d.vertex.PoseStack;
import net.minecraft.client.renderer.SubmitNodeCollector;
import net.minecraft.client.renderer.item.ItemStackRenderState;
import net.minecraft.client.renderer.special.SpecialModelRenderer;
import net.minecraft.world.item.ItemStack;
import org.joml.Vector3f;
import org.joml.Vector3fc;
import java.util.function.Consumer;
/** Submits a previously extracted item model inside a composite item. */
public final class IndustrialForegoingISTER implements SpecialModelRenderer<ItemStackRenderState> {
    public static final IndustrialForegoingISTER INSTANCE = new IndustrialForegoingISTER();
    @Override public void submit(ItemStackRenderState state, PoseStack pose, SubmitNodeCollector collector, int light, int overlay, boolean foil, int outline) {
        if (state != null) state.submit(pose, collector, light, overlay, outline);
    }
    @Override public void getExtents(Consumer<Vector3fc> output) { output.accept(new Vector3f(0)); output.accept(new Vector3f(1)); }
    @Override public ItemStackRenderState extractArgument(ItemStack stack) { throw new UnsupportedOperationException("Arguments are extracted by the composite item model"); }
}
''')
(root/'proxy/client/render/item/HydroponicSimProcessorISTER.java').write_text('''package com.buuz135.industrial.proxy.client.render.item;
import com.buuz135.industrial.item.HydroponicSimulationProcessorItem;
import com.buuz135.industrial.utils.IFAttachments;
import com.mojang.serialization.MapCodec;
import net.minecraft.client.Minecraft;
import net.minecraft.client.multiplayer.ClientLevel;
import net.minecraft.client.renderer.item.*;
import net.minecraft.client.resources.model.ResolvableModel;
import net.minecraft.resources.Identifier;
import net.minecraft.world.entity.ItemOwner;
import net.minecraft.world.item.ItemDisplayContext;
import net.minecraft.world.item.ItemStack;
import org.joml.Matrix4f;
import org.joml.Matrix4fc;
import org.joml.Vector3f;
import org.joml.Vector3fc;
import java.util.List;
import java.util.Optional;
/** Processor/crop composite with an enlarged crop preview while holding Shift. */
public record HydroponicSimProcessorISTER(ItemModel base) implements ItemModel {
    private static final Identifier BASE = Identifier.fromNamespaceAndPath("industrialforegoing", "item/clean_hydroponic_simulation_processor");
    @Override public void update(ItemStackRenderState output, ItemStack stack, ItemModelResolver resolver, ItemDisplayContext display,
                                 ClientLevel level, ItemOwner owner, int seed) {
        output.appendModelIdentityElement(this);
        boolean shift = Minecraft.getInstance().hasShiftDown();
        ItemStack crop = stack.has(IFAttachments.HYDROPONIC_SIMULATION_PROCESSOR)
                ? new HydroponicSimulationProcessorItem.Simulation(stack.get(IFAttachments.HYDROPONIC_SIMULATION_PROCESSOR)).getCrop() : ItemStack.EMPTY;
        if (!shift || display != ItemDisplayContext.GUI || crop.isEmpty()) base.update(output, stack, resolver, display, level, owner, seed);
        if (crop.isEmpty()) return;
        var cropState = new ItemStackRenderState();
        resolver.updateForTopItem(cropState, crop, display, level, owner, seed);
        Matrix4f transform = new Matrix4f().translation(0.5f, 0.5f, display == ItemDisplayContext.GUI ? 8.5f : 0.5f);
        if (!shift) transform.translate(display == ItemDisplayContext.GUI ? 0.25f : 0.1f, display == ItemDisplayContext.GUI ? -0.25f : -0.1f, 0.001f).scale(0.5f,0.5f,1);
        var layer = output.newLayer();
        layer.setupSpecialModel(IndustrialForegoingISTER.INSTANCE, cropState);
        layer.setLocalTransform(transform);
        layer.setExtents(() -> new Vector3fc[]{new Vector3f(0),new Vector3f(1)});
        layer.setUsesBlockLight(false);
        output.appendModelIdentityElement(cropState);
        output.appendModelIdentityElement(shift);
    }
    public record Unbaked() implements ItemModel.Unbaked {
        public static final MapCodec<Unbaked> CODEC = MapCodec.unit(new Unbaked());
        @Override public MapCodec<Unbaked> type() { return CODEC; }
        @Override public void resolveDependencies(ResolvableModel.Resolver resolver) { resolver.markDependency(BASE); }
        @Override public ItemModel bake(ItemModel.BakingContext context, Matrix4fc transform) {
            return new HydroponicSimProcessorISTER(new CuboidItemModelWrapper.Unbaked(BASE, Optional.empty(), List.of()).bake(context, transform));
        }
    }
}
''')
(root/'proxy/client/render/ContributorsCatEarsRender.java').write_text('''package com.buuz135.industrial.proxy.client.render;
import com.buuz135.industrial.proxy.client.ClientProxy;
import com.hrznstudio.titanium.reward.storage.ClientRewardStorage;
import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.math.Axis;
import net.minecraft.client.Minecraft;
import net.minecraft.client.model.player.PlayerModel;
import net.minecraft.client.renderer.SubmitNodeCollector;
import net.minecraft.client.renderer.block.dispatch.BlockStateModelPart;
import net.minecraft.client.renderer.entity.RenderLayerParent;
import net.minecraft.client.renderer.entity.layers.RenderLayer;
import net.minecraft.client.renderer.entity.state.AvatarRenderState;
import net.minecraft.client.renderer.rendertype.RenderTypes;
import net.minecraft.client.renderer.texture.OverlayTexture;
import net.minecraft.resources.Identifier;
import net.minecraft.util.RandomSource;
import net.minecraft.util.context.ContextKey;
import net.minecraft.world.entity.Avatar;
import net.minecraft.world.level.block.Blocks;
import java.util.*;
public class ContributorsCatEarsRender extends RenderLayer<AvatarRenderState, PlayerModel> {
    public static final ContextKey<Ears> EARS = new ContextKey<>(Identifier.fromNamespaceAndPath("industrialforegoing", "ears"));
    public record Ears(boolean seasonal, List<BlockStateModelPart> parts) {}
    public ContributorsCatEarsRender(RenderLayerParent<AvatarRenderState, PlayerModel> parent) { super(parent); }
    public static void extract(Avatar avatar, AvatarRenderState state) {
        state.setRenderData(EARS, null);
        var rewards = ClientRewardStorage.REWARD_STORAGE.getRewards().get(avatar.getUUID());
        if (rewards == null) return;
        String type = rewards.getEnabled().get(Identifier.fromNamespaceAndPath("industrialforegoing", "cat_ears"));
        if (type == null) return;
        int month = Calendar.getInstance().get(Calendar.MONTH);
        boolean spooky = type.equalsIgnoreCase("spooky") || month == Calendar.OCTOBER && type.equalsIgnoreCase("normal");
        boolean snowy = type.equalsIgnoreCase("snowy") || month == Calendar.DECEMBER && type.equalsIgnoreCase("normal");
        List<BlockStateModelPart> parts = new ArrayList<>();
        if (spooky || snowy) {
            var block = snowy ? Blocks.CAKE : avatar.level().getGameTime() % 200 < 100 ? Blocks.CARVED_PUMPKIN : Blocks.JACK_O_LANTERN;
            Minecraft.getInstance().getBlockRenderer().getBlockModel(block.defaultBlockState()).collectParts(RandomSource.create(0), parts);
        } else if (ClientProxy.ears_baked != null) parts.add(ClientProxy.ears_baked);
        state.setRenderData(EARS, new Ears(spooky || snowy, List.copyOf(parts)));
    }
    @Override public void submit(PoseStack pose, SubmitNodeCollector collector, int light, AvatarRenderState state, float yaw, float pitch) {
        Ears ears = state.getRenderData(EARS);
        if (ears == null || ears.parts.isEmpty()) return;
        pose.pushPose();
        pose.translate(0,-0.015,0);
        if (!state.headEquipment.isEmpty()) pose.translate(0,-0.02,0);
        if (state.isCrouching) pose.translate(0,0.27,0);
        pose.mulPose(Axis.YP.rotationDegrees(90));
        pose.mulPose(Axis.XP.rotationDegrees(180));
        pose.mulPose(Axis.YN.rotationDegrees(yaw));
        pose.mulPose(Axis.ZN.rotationDegrees(pitch));
        if (ears.seasonal) {
            pose.mulPose(Axis.YN.rotationDegrees(90));
            pose.translate(0.08,0.485,-0.1);
            pose.scale(0.125f,0.125f,0.125f);
        }
        collector.submitBlockModel(pose, RenderTypes.cutoutMovingBlock(), ears.parts, new int[0], light, OverlayTexture.NO_OVERLAY, state.outlineColor);
        if (ears.seasonal) {
            pose.translate(-0.08 * 28,0,0);
            collector.submitBlockModel(pose, RenderTypes.cutoutMovingBlock(), ears.parts, new int[0], light, OverlayTexture.NO_OVERLAY, state.outlineColor);
        }
        pose.popPose();
    }
}
''')
(root/'entity/client/InfinityLauncherProjectileArmorLayer.java').write_text('''package com.buuz135.industrial.entity.client;
import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.math.Axis;
import net.minecraft.client.model.player.PlayerModel;
import net.minecraft.client.renderer.SubmitNodeCollector;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.RenderLayerParent;
import net.minecraft.client.renderer.entity.layers.RenderLayer;
import net.minecraft.client.renderer.entity.state.AvatarRenderState;
import net.minecraft.client.renderer.entity.state.EntityRenderState;
import net.minecraft.client.renderer.texture.OverlayTexture;
import net.minecraft.resources.Identifier;
import net.minecraft.util.Mth;
import net.minecraft.util.RandomSource;
import net.minecraft.util.context.ContextKey;
import java.util.HashMap;
public class InfinityLauncherProjectileArmorLayer extends RenderLayer<AvatarRenderState, PlayerModel> {
    public static final HashMap<String,Integer> PROJECTILE_AMOUNT = new HashMap<>();
    public static final ContextKey<Integer> COUNT = new ContextKey<>(Identifier.fromNamespaceAndPath("industrialforegoing", "stuck_plungers"));
    private final InfinityLauncherProjectileModel model;
    public InfinityLauncherProjectileArmorLayer(RenderLayerParent<AvatarRenderState, PlayerModel> parent, EntityRendererProvider.Context context) {
        super(parent);
        model = new InfinityLauncherProjectileModel(context.bakeLayer(InfinityLauncherProjectileRenderer.PROJECTILE_LAYER));
    }
    @Override public void submit(PoseStack pose, SubmitNodeCollector collector, int light, AvatarRenderState state, float yaw, float pitch) {
        Integer count = state.getRenderData(COUNT);
        if (count == null || count <= 0) return;
        var random = RandomSource.create(state.id);
        for (int i=0; i<count; i++) {
            pose.pushPose();
            var part = getParentModel().getRandomBodyPart(random);
            var cube = part.getRandomCube(random);
            part.translateAndRotate(pose);
            float x=random.nextFloat(), y=random.nextFloat(), z=random.nextFloat();
            pose.translate(Mth.lerp(x,cube.minX,cube.maxX)/16f, Mth.lerp(y,cube.minY,cube.maxY)/16f, Mth.lerp(z,cube.minZ,cube.maxZ)/16f);
            x=1-2*x; y=1-2*y; z=1-2*z;
            pose.mulPose(Axis.YP.rotationDegrees((float)Math.toDegrees(Math.atan2(x,z))-90));
            pose.mulPose(Axis.ZP.rotationDegrees((float)Math.toDegrees(Math.atan2(y,Math.sqrt(x*x+z*z)))+90));
            pose.translate(0,-0.8,0);
            collector.submitModel(model, new EntityRenderState(), pose, InfinityLauncherProjectileRenderer.PROJECTILE, light, OverlayTexture.NO_OVERLAY, state.outlineColor, null);
            pose.popPose();
        }
    }
}
''')
