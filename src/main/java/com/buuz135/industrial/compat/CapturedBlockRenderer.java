package com.buuz135.industrial.compat;

import com.mojang.blaze3d.vertex.PoseStack;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.SubmitNodeCollector;
import net.minecraft.client.renderer.blockentity.BlockEntityRenderer;
import net.minecraft.client.renderer.blockentity.state.BlockEntityRenderState;
import net.minecraft.client.renderer.feature.ModelFeatureRenderer;
import net.minecraft.client.renderer.state.level.CameraRenderState;
import net.minecraft.client.renderer.texture.OverlayTexture;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.phys.Vec3;

public abstract class CapturedBlockRenderer<T extends BlockEntity> implements BlockEntityRenderer<T, CapturedBlockRenderer.State> {
    public static final class State extends BlockEntityRenderState { private CapturedGeometry geometry; }
    @Override public State createRenderState() { return new State(); }
    @Override public void extractRenderState(T block, State state, float partial, Vec3 camera, ModelFeatureRenderer.CrumblingOverlay breaking) {
        BlockEntityRenderer.super.extractRenderState(block, state, partial, camera, breaking);
        state.geometry = new CapturedGeometry();
        render(block, partial, new PoseStack(), state.geometry, state.lightCoords, OverlayTexture.NO_OVERLAY);
    }
    @Override public void submit(State state, PoseStack pose, SubmitNodeCollector collector, CameraRenderState camera) { state.geometry.submit(pose, collector); }
    public abstract void render(T block, float partial, PoseStack pose, MultiBufferSource buffer, int light, int overlay);
}
