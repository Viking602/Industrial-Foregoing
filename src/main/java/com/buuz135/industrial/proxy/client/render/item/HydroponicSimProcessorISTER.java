package com.buuz135.industrial.proxy.client.render.item;
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
