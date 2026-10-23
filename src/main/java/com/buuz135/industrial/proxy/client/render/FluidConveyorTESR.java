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

import com.buuz135.industrial.block.transportstorage.ConveyorBlock;
import com.buuz135.industrial.block.transportstorage.tile.ConveyorTile;
import com.mojang.blaze3d.systems.RenderSystem;
import com.mojang.blaze3d.vertex.DefaultVertexFormat;
import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import com.mojang.blaze3d.vertex.VertexFormat;
import com.mojang.math.Axis;
import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.GameRenderer;
import net.minecraft.client.renderer.MultiBufferSource;

import net.minecraft.client.renderer.rendertype.RenderType;
import net.minecraft.client.renderer.blockentity.BlockEntityRenderer;
import net.minecraft.client.renderer.blockentity.BlockEntityRendererProvider;
import net.minecraft.client.renderer.texture.AbstractTexture;
import net.minecraft.client.renderer.texture.TextureAtlas;
import net.minecraft.client.renderer.texture.TextureAtlasSprite;
import net.minecraft.core.Direction;
import net.minecraft.resources.Identifier;
import net.neoforged.neoforge.client.extensions.common.IClientFluidTypeExtensions;
import net.neoforged.neoforge.fluids.FluidStack;
import org.joml.Matrix4f;
import org.lwjgl.opengl.GL11;

import java.awt.*;

public class FluidConveyorTESR extends com.buuz135.industrial.compat.CapturedBlockRenderer<ConveyorTile> {
    public FluidConveyorTESR(BlockEntityRendererProvider.Context context) {}
    @Override
    public void render(ConveyorTile tile, float partial, PoseStack pose, MultiBufferSource buffers, int light, int overlay) {
        FluidStack fluid = tile.getTank().getFluid();
        if (fluid.isEmpty()) return;
        var model = Minecraft.getInstance().getModelManager().getFluidStateModelSet().get(fluid.getFluid().defaultFluidState());
        var sprite = model.flowingMaterial().sprite();
        int tint = model.fluidTintSource() == null ? -1 : model.fluidTintSource().colorAsStack(fluid);
        var buffer = buffers.getBuffer(net.minecraft.client.renderer.rendertype.RenderTypes.entityTranslucentEmissive(sprite.atlasLocation()));
        pose.pushPose();
        Direction facing = tile.getFacing();
        if (facing == Direction.NORTH) { pose.translate(1,0,1); pose.mulPose(Axis.YP.rotationDegrees(180)); }
        if (facing == Direction.EAST) { pose.translate(0,0,1); pose.mulPose(Axis.YP.rotationDegrees(90)); }
        if (facing == Direction.WEST) { pose.translate(1,0,0); pose.mulPose(Axis.YP.rotationDegrees(-90)); }
        var matrix = pose.last().pose();
        float y = 3 / 32f;
        quad(buffer, matrix, tint, sprite, 15/16f,y,0, 1/16f,y,0, 1/16f,y,1, 15/16f,y,1);
        sprite = model.stillMaterial().sprite();
        if (!(tile.getLevel().getBlockEntity(tile.getBlockPos().relative(facing.getOpposite())) instanceof ConveyorTile other) || other.getTank().getFluidAmount() <= 0)
            quad(buffer,matrix,tint,sprite, 1/16f,y,0,15/16f,y,0,15/16f,1/16f,0,1/16f,1/16f,0);
        if (!(tile.getLevel().getBlockEntity(tile.getBlockPos().relative(facing)) instanceof ConveyorTile other) || other.getTank().getFluidAmount() <= 0)
            quad(buffer,matrix,tint,sprite, 15/16f,y,1,1/16f,y,1,1/16f,1/16f,1,15/16f,1/16f,1);
        pose.popPose();
    }
    private static void quad(VertexConsumer buffer, Matrix4f matrix, int tint, TextureAtlasSprite sprite, float... xyz) {
        float[] us = {sprite.getU0(),sprite.getU1(),sprite.getU1(),sprite.getU0()};
        float[] vs = {sprite.getV0(),sprite.getV0(),sprite.getV1(),sprite.getV1()};
        for (int i=0;i<4;i++) buffer.addVertex(matrix,xyz[i*3],xyz[i*3+1],xyz[i*3+2]).setColor(tint).setUv(us[i],vs[i]);
    }
}
