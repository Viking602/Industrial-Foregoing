/*
 * This file is part of Industrial Foregoing.
 *
 * Copyright 2021, Buuz135
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of
 * this software and associated documentation files (the "Software"), to deal in the
 * Software without restriction, including without limitation the rights to use, copy,
 * modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
 * and to permit persons to whom the Software is furnished to do so, subject to the
 * following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all copies
 * or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
 * INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
 * PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
 * FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
 * ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */
package com.buuz135.industrial.entity.client;
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
