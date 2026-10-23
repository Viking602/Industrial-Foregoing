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

package com.buuz135.industrial.proxy.client.particle;


import com.mojang.blaze3d.systems.RenderSystem;
import com.mojang.blaze3d.vertex.*;
import net.minecraft.client.Camera;
import net.minecraft.client.CameraType;
import net.minecraft.client.Minecraft;
import net.minecraft.client.multiplayer.ClientLevel;
import net.minecraft.client.particle.Particle;
import net.minecraft.client.particle.ParticleRenderType;
import net.minecraft.client.player.LocalPlayer;
import net.minecraft.client.renderer.GameRenderer;
import net.minecraft.client.renderer.texture.TextureManager;
import net.minecraft.core.Direction;
import net.minecraft.util.RandomSource;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.phys.Vec3;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.api.distmarker.OnlyIn;
import org.jetbrains.annotations.Nullable;
import org.joml.Vector3f;

import java.util.ArrayList;
import java.util.List;

public class ParticleVex extends Particle {

    public static final ParticleRenderType RENDER = new ParticleRenderType("industrialforegoing:vex_trail");

    private final Entity entity;
    private List<Direction> directions;
    private List<Vector3f> lines;
    private boolean isDying = false;

    public ParticleVex(Entity entity) { //getPosition
        super((ClientLevel) entity.level(), entity.getX() + entity.level().getRandom().nextDouble() - 0.5, entity.getY() + 1 + entity.level().getRandom().nextDouble() - 0.5, entity.getZ() + entity.level().getRandom().nextDouble() - 0.5);
        this.entity = entity;
        directions = new ArrayList<>();
        Direction prev = Direction.NORTH;
        directions.add(0, prev);
        for (int i = 1; i < 50; i++) {
            prev = directions.get(i - 1);
            directions.add(i, level.getRandom().nextDouble() < 0.05 ? getRandomFacing(level.getRandom(), prev) : prev);
        }
        calculateLines();
        this.lifetime = 500;
    }

    @Override
    public void tick() {
        super.tick();
        if (this.entity.position().distanceToSqr(new Vec3(x, y, z)) > 10) {
            isDying = true;
        }
        if (!isDying && !this.removed) {
            directions.add(0, level.getRandom().nextDouble() < 0.05 ? getRandomFacing(level.getRandom(), directions.get(0)) : directions.get(0));
            directions.remove(50);
            Vec3 directionVector = new Vec3(directions.get(0).getUnitVec3i().getX(), directions.get(0).getUnitVec3i().getY(), directions.get(0).getUnitVec3i().getZ()).scale(0.01);
            this.setPos(x - directionVector.x, y - directionVector.y, z - directionVector.z);
            calculateLines();
        } else {
            if (!directions.isEmpty()) directions.removeLast();
            calculateLines();
            if (directions.isEmpty()) this.remove();
        }
    }

    private boolean hiddenInFirstPerson() {
        var player = Minecraft.getInstance().player;
        return player != null && entity == player && Minecraft.getInstance().options.getCameraType() == CameraType.FIRST_PERSON
                && entity.position().add(0, 1, 0).distanceToSqr(new Vec3(x, y, z)) < 3;
    }

    @Override public ParticleRenderType getGroup() { return RENDER; }

    public static final class Group extends net.minecraft.client.particle.ParticleGroup<ParticleVex> {
        public Group(net.minecraft.client.particle.ParticleEngine engine) { super(engine); }
        @Override public net.minecraft.client.renderer.state.level.ParticleGroupRenderState extractRenderState(
                net.minecraft.client.renderer.culling.Frustum frustum, Camera camera, float partialTick) {
            // Copy the paths now: ticking particles must not mutate a submitted frame.
            List<List<Vector3f>> trails = new ArrayList<>();
            Vec3 cameraPos = camera.position();
            for (ParticleVex particle : particles) {
                if (!particle.hiddenInFirstPerson()) trails.add(particle.lines.stream()
                        .map(point -> new Vector3f(point).sub((float)cameraPos.x, (float)cameraPos.y, (float)cameraPos.z)).toList());
            }
            return (collector, cameraState) -> collector.submitCustomGeometry(new PoseStack(), net.minecraft.client.renderer.rendertype.RenderTypes.lines(), (pose, buffer) -> {
                for (List<Vector3f> trail : trails) for (int i = 1; i < trail.size(); i++) {
                    Vector3f from = trail.get(i-1), to = trail.get(i);
                    Vector3f normal = new Vector3f(to).sub(from);
                    if (normal.lengthSquared() == 0) continue;
                    normal.normalize();
                    buffer.addVertex(pose, from.x, from.y, from.z).setColor(-1).setNormal(pose, normal.x, normal.y, normal.z).setLineWidth(1.5f);
                    buffer.addVertex(pose, to.x, to.y, to.z).setColor(-1).setNormal(pose, normal.x, normal.y, normal.z).setLineWidth(1.5f);
                }
            });
        }
    }

    private Direction getRandomFacing(RandomSource random, Direction opposite) {
        Direction facing = Direction.getRandom(random); //random
        while (facing.getOpposite().equals(opposite)) facing = Direction.getRandom(random);
        return facing;
    }

    private void calculateLines() {
        lines = new ArrayList<>();
        if (directions.size() == 0) return;
        Direction prev = directions.get(0);
        int currentPosition = 0;
        Vector3f prevBlockPos = new Vector3f((float) x, (float) y, (float) z);
        lines.add(prevBlockPos);
        for (int i = 1; i < directions.size(); i++) {
            if (!directions.get(i).equals(prev) || i == directions.size() - 1) {
                Vec3 directionVector = new Vec3(prev.getUnitVec3i().getX(), prev.getUnitVec3i().getY(), prev.getUnitVec3i().getZ()).scale(0.01);
                Vector3f endBlockPos = new Vector3f((float) (prevBlockPos.x + directionVector.x * (i - currentPosition)), (float) (prevBlockPos.y + directionVector.y * (i - currentPosition)), (float) (prevBlockPos.z + directionVector.z * (i - currentPosition)));
                lines.add(endBlockPos);
                prev = directions.get(i);
                currentPosition = i;
                prevBlockPos = endBlockPos;
            }
        }
    }
}
