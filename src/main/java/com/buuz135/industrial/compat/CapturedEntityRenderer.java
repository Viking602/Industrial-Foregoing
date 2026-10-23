package com.buuz135.industrial.compat;

import com.mojang.blaze3d.vertex.PoseStack;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.SubmitNodeCollector;
import net.minecraft.client.renderer.entity.EntityRenderer;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.state.EntityRenderState;
import net.minecraft.client.renderer.state.level.CameraRenderState;
import net.minecraft.resources.Identifier;
import net.minecraft.world.entity.Entity;

public abstract class CapturedEntityRenderer<T extends Entity> extends EntityRenderer<T, CapturedEntityRenderer.State> {
    public static final class State extends EntityRenderState { private CapturedGeometry geometry; }
    protected CapturedEntityRenderer(EntityRendererProvider.Context context) { super(context); }
    @Override public State createRenderState() { return new State(); }
    @Override public void extractRenderState(T entity, State state, float partial) {
        super.extractRenderState(entity, state, partial);
        state.geometry = new CapturedGeometry();
        render(entity, entity.getYRot(), partial, new PoseStack(), state.geometry, state.lightCoords);
    }
    @Override public void submit(State state, PoseStack pose, SubmitNodeCollector collector, CameraRenderState camera) {
        state.geometry.submit(pose, collector);
        super.submit(state, pose, collector, camera);
    }
    public abstract void render(T entity, float yaw, float partial, PoseStack pose, MultiBufferSource buffer, int light);
    public abstract Identifier getTextureLocation(T entity);
}
