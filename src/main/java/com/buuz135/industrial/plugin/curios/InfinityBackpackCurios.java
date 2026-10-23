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

package com.buuz135.industrial.plugin.curios;

import com.buuz135.industrial.item.infinity.item.ItemInfinityBackpack;
import com.buuz135.industrial.module.ModuleTool;
import com.buuz135.industrial.plugin.CuriosPlugin;
import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.math.Axis;
import net.minecraft.client.Minecraft;
import net.minecraft.client.model.EntityModel;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.entity.RenderLayerParent;
import net.minecraft.client.renderer.texture.OverlayTexture;

import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.ItemDisplayContext;
import net.minecraft.world.item.ItemStack;
import top.theillusivec4.curios.api.SlotContext;
import top.theillusivec4.curios.api.client.ICurioRenderer;
import top.theillusivec4.curios.api.type.capability.ICurio;

public class InfinityBackpackCurios implements ICurio, ICurioRenderer {

    @Override
    public boolean canEquip(SlotContext identifier) {
        return identifier.identifier().equals("back");
    }

    @Override
    public ItemStack getStack() {
        return new ItemStack(ModuleTool.INFINITY_BACKPACK.get());
    }

    @Override
    public void curioTick(SlotContext slotContext) {
        LivingEntity livingEntity = slotContext.entity();
        ItemStack stack = CuriosPlugin.getStack(livingEntity, "back", 0);
        if (stack.getItem() instanceof ItemInfinityBackpack) {
            if (livingEntity.level() instanceof net.minecraft.server.level.ServerLevel serverLevel) ModuleTool.INFINITY_BACKPACK.get().inventoryTick(stack, serverLevel, livingEntity, null);
        }
    }

    @Override
    public <S extends net.minecraft.client.renderer.entity.state.LivingEntityRenderState, M extends EntityModel<? super S>> void render(
            ItemStack stack, SlotContext slotContext, PoseStack matrixStack, net.minecraft.client.renderer.SubmitNodeCollector collector,
            int light, S state, RenderLayerParent<S, M> parent, net.minecraft.client.renderer.entity.EntityRendererProvider.Context context,
            float yRot, float xRot) {
        if (!(stack.getItem() instanceof ItemInfinityBackpack)) return;
        var itemState = new net.minecraft.client.renderer.item.ItemStackRenderState();
        context.getItemModelResolver().updateForLiving(itemState, stack, ItemDisplayContext.FIXED, slotContext.entity());
        matrixStack.pushPose();
        if (state instanceof net.minecraft.client.renderer.entity.state.HumanoidRenderState humanoid && humanoid.isCrouching) {
            matrixStack.translate(0, 0.2, 0);
            matrixStack.mulPose(Axis.XP.rotationDegrees((float) (90 / Math.PI)));
        }
        matrixStack.mulPose(Axis.XP.rotationDegrees(180));
        matrixStack.translate(0, -0.4, -0.2);
        matrixStack.scale(0.65f, 0.65f, 0.65f);
        itemState.submit(matrixStack, collector, light, OverlayTexture.NO_OVERLAY, 0);
        matrixStack.popPose();
    }
}
