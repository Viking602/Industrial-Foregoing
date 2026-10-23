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

package com.buuz135.industrial.proxy.client.event;

import com.buuz135.industrial.item.infinity.InfinityTier;
import com.buuz135.industrial.item.infinity.item.ItemInfinityDrill;
import com.buuz135.industrial.module.ModuleTool;
import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import net.minecraft.client.Camera;
import net.minecraft.client.CameraType;
import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.LevelRenderer;
import net.minecraft.client.renderer.rendertype.RenderType;
import net.minecraft.core.BlockPos;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.LiquidBlock;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.HitResult;
import net.minecraft.world.phys.shapes.VoxelShape;
import net.neoforged.bus.api.SubscribeEvent;


import org.apache.commons.lang3.tuple.Pair;

public class IFClientEvents {

    @SubscribeEvent
    public void blockOverlayEvent(net.neoforged.neoforge.client.event.ExtractBlockOutlineRenderStateEvent event) {
        var player = Minecraft.getInstance().player;
        if (player == null || !(player.getMainHandItem().getItem() instanceof ItemInfinityDrill drill)) return;
        var hit = event.getHitResult();
        var area = drill.getArea(hit.getBlockPos(), hit.getDirection(), drill.getSelectedTier(player.getMainHandItem()), false);
        var world = event.getLevel();
        var camera = event.getCamera().position();
        var boxes = new java.util.ArrayList<net.minecraft.world.phys.AABB>();
        for (BlockPos pos : BlockPos.betweenClosed(area.getLeft(), area.getRight())) {
            var state = world.getBlockState(pos);
            var shape = state.getShape(world, pos);
            if (!shape.isEmpty() && !state.isAir() && state.getDestroySpeed(world, pos) >= 0 && !(state.getBlock() instanceof LiquidBlock))
                boxes.add(shape.bounds().move(pos).move(-camera.x, -camera.y, -camera.z));
        }
        event.addCustomRenderer((state, buffers, pose, translucent, levelState) -> {
            var lines = buffers.getBuffer(net.minecraft.client.renderer.rendertype.RenderTypes.lines());
            for (var box : boxes) com.buuz135.industrial.compat.RenderCompat.renderLineBox(pose, lines, box, 0, 0, 0, 0.35f);
            return true;
        });
    }
}
