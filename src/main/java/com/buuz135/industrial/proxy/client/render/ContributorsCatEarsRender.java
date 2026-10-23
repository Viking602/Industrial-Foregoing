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

package com.buuz135.industrial.proxy.client.render;
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
            Minecraft.getInstance().getModelManager().getBlockStateModelSet().get(block.defaultBlockState()).collectParts(RandomSource.create(0), parts);
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
