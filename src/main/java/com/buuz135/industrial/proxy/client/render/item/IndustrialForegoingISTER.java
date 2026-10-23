package com.buuz135.industrial.proxy.client.render.item;
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
