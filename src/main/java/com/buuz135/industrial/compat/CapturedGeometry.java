package com.buuz135.industrial.compat;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.SubmitNodeCollector;
import net.minecraft.client.renderer.item.ItemStackRenderState;
import net.minecraft.client.renderer.rendertype.RenderType;
import net.minecraft.world.item.ItemDisplayContext;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import org.joml.Matrix4f;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/** Detached geometry collected during extraction and replayed in the submission phase. */
public final class CapturedGeometry implements MultiBufferSource {
    private final Map<RenderType, Mesh> meshes = new LinkedHashMap<>();
    private final List<ItemCommand> items = new ArrayList<>();
    @Override public VertexConsumer getBuffer(RenderType type) { return meshes.computeIfAbsent(type, unused -> new Mesh()); }
    public void item(ItemStack stack, ItemDisplayContext context, int light, int overlay, PoseStack pose, Level level, int seed) {
        var state = new ItemStackRenderState();
        Minecraft.getInstance().getItemModelResolver().updateForTopItem(state, stack, context, level, null, seed);
        items.add(new ItemCommand(state, new Matrix4f(pose.last().pose()), light, overlay));
    }
    public void submit(PoseStack pose, SubmitNodeCollector collector) {
        meshes.forEach((type, mesh) -> collector.submitCustomGeometry(pose, type, (transform, buffer) -> {
            for (Vertex v : mesh.vertices) {
                buffer.addVertex(transform, v.x, v.y, v.z).setColor(v.color).setUv(v.u, v.v)
                    .setUv1(v.overlayU, v.overlayV).setUv2(v.lightU, v.lightV)
                    .setNormal(transform, v.nx, v.ny, v.nz).setLineWidth(v.width);
            }
        }));
        for (ItemCommand item : items) {
            pose.pushPose();
            pose.mulPose(item.pose());
            item.state().submit(pose, collector, item.light(), item.overlay(), 0);
            pose.popPose();
        }
    }
    private record ItemCommand(ItemStackRenderState state, Matrix4f pose, int light, int overlay) {}
    private static final class Vertex {
        float x, y, z, u, v, nx, ny = 1, nz, width = 2.5f;
        int color = -1, overlayU, overlayV = 10, lightU = 240, lightV = 240;
    }
    private static final class Mesh implements VertexConsumer {
        private final List<Vertex> vertices = new ArrayList<>();
        private Vertex current;
        public VertexConsumer addVertex(float x, float y, float z) { current = new Vertex(); current.x=x; current.y=y; current.z=z; vertices.add(current); return this; }
        public VertexConsumer setColor(int r,int g,int b,int a) { return setColor(net.minecraft.util.ARGB.color(a,r,g,b)); }
        public VertexConsumer setColor(int color) { current.color=color; return this; }
        public VertexConsumer setUv(float u,float v) { current.u=u; current.v=v; return this; }
        public VertexConsumer setUv1(int u,int v) { current.overlayU=u; current.overlayV=v; return this; }
        public VertexConsumer setUv2(int u,int v) { current.lightU=u; current.lightV=v; return this; }
        public VertexConsumer setNormal(float x,float y,float z) { current.nx=x; current.ny=y; current.nz=z; return this; }
        public VertexConsumer setLineWidth(float width) { current.width=width; return this; }
    }
}
