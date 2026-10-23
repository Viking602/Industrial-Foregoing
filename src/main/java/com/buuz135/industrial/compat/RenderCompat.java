package com.buuz135.industrial.compat;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import com.mojang.blaze3d.vertex.VertexMultiConsumer;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.rendertype.RenderType;
import net.minecraft.client.renderer.rendertype.RenderTypes;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.ItemDisplayContext;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.AABB;

public final class RenderCompat {
    private RenderCompat() {}
    public static VertexConsumer getFoilBufferDirect(MultiBufferSource buffer, RenderType type, boolean unused, boolean foil) {
        return foil ? VertexMultiConsumer.create(buffer.getBuffer(RenderTypes.entityGlint()), buffer.getBuffer(type)) : buffer.getBuffer(type);
    }
    public static void renderStatic(ItemStack stack, ItemDisplayContext context, int light, int overlay, PoseStack pose, MultiBufferSource buffer, Level level, int seed) {
        ((CapturedGeometry) buffer).item(stack, context, light, overlay, pose, level, seed);
    }
    public static void renderLineBox(PoseStack pose, VertexConsumer buffer, AABB box, float r, float g, float b, float a) {
        net.minecraft.client.renderer.ShapeRenderer.renderShape(pose, buffer, net.minecraft.world.phys.shapes.Shapes.create(box), 0,0,0, net.minecraft.util.ARGB.colorFromFloat(a,r,g,b), 2.5f);
    }
}
