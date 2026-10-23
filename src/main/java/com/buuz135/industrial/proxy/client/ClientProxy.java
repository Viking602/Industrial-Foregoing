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

package com.buuz135.industrial.proxy.client;

import com.buuz135.industrial.block.generator.tile.MycelialReactorTile;
import com.buuz135.industrial.block.tile.IndustrialAreaWorkingTile;
import com.buuz135.industrial.block.transportstorage.tile.ConveyorTile;
import com.buuz135.industrial.block.transportstorage.tile.TransporterTile;
import com.buuz135.industrial.entity.InfinityLauncherProjectileEntity;
import com.buuz135.industrial.entity.InfinityNukeEntity;
import com.buuz135.industrial.entity.InfinityTridentEntity;
import com.buuz135.industrial.entity.client.*;
import com.buuz135.industrial.item.MobImprisonmentToolItem;
import com.buuz135.industrial.item.infinity.InfinityTier;
import com.buuz135.industrial.item.infinity.ItemInfinity;
import com.buuz135.industrial.module.*;
import com.buuz135.industrial.proxy.CommonProxy;
import com.buuz135.industrial.proxy.client.event.IFClientEvents;
import com.buuz135.industrial.proxy.client.render.*;
import com.buuz135.industrial.proxy.client.render.item.HydroponicSimProcessorISTER;
import com.buuz135.industrial.utils.FluidUtils;
import com.buuz135.industrial.utils.IFAttachments;
import com.buuz135.industrial.utils.Reference;
import com.hrznstudio.titanium.event.handler.EventManager;
import com.hrznstudio.titanium.module.BlockWithTile;
import net.minecraft.ChatFormatting;
import net.minecraft.client.KeyMapping;
import net.minecraft.client.Minecraft;
import net.minecraft.client.model.geom.builders.CubeDeformation;


import net.minecraft.client.renderer.rendertype.RenderType;
import net.minecraft.client.renderer.entity.EntityRenderDispatcher;


import net.minecraft.world.entity.player.PlayerSkin;

import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.util.ARGB;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.SpawnEggItem;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.capabilities.Capabilities;
import net.neoforged.neoforge.client.event.EntityRenderersEvent;
import net.neoforged.neoforge.client.extensions.common.IClientItemExtensions;
import net.neoforged.neoforge.client.extensions.common.RegisterClientExtensionsEvent;
import net.neoforged.neoforge.common.NeoForge;
import net.neoforged.neoforge.event.entity.player.ItemTooltipEvent;

import java.util.Calendar;

@EventBusSubscriber(value = Dist.CLIENT, modid = Reference.MOD_ID)
public class ClientProxy extends CommonProxy {

    public static Identifier GUI = Identifier.fromNamespaceAndPath(Reference.MOD_ID, "textures/gui/machines.png");
    public static net.minecraft.client.renderer.block.dispatch.BlockStateModelPart ears_baked;
    private static final net.neoforged.neoforge.client.model.standalone.StandaloneModelKey<net.minecraft.client.renderer.block.dispatch.BlockStateModelPart> EARS_MODEL = new net.neoforged.neoforge.client.model.standalone.StandaloneModelKey<>(() -> "industrialforegoing:cat_ears");

    public static KeyMapping OPEN_BACKPACK;

    @SubscribeEvent
    public static void onRegisterRenderers(EntityRenderersEvent.RegisterRenderers event) {
        registerAreaRender(event, ModuleCore.FLUID_EXTRACTOR);
        registerAreaRender(event, ModuleAgricultureHusbandry.PLANT_GATHERER);
        registerAreaRender(event, ModuleAgricultureHusbandry.PLANT_SOWER);
        registerAreaRender(event, ModuleAgricultureHusbandry.SEWER);
        registerAreaRender(event, ModuleAgricultureHusbandry.PLANT_FERTILIZER);
        registerAreaRender(event, ModuleAgricultureHusbandry.SLAUGHTER_FACTORY);
        registerAreaRender(event, ModuleAgricultureHusbandry.ANIMAL_RANCHER);
        registerAreaRender(event, ModuleAgricultureHusbandry.ANIMAL_FEEDER);
        registerAreaRender(event, ModuleAgricultureHusbandry.ANIMAL_BABY_SEPARATOR);
        registerAreaRender(event, ModuleAgricultureHusbandry.MOB_CRUSHER);
        registerAreaRender(event, ModuleAgricultureHusbandry.WITHER_BUILDER);
        registerAreaRender(event, ModuleMisc.STASIS_CHAMBER);
        registerAreaRender(event, ModuleResourceProduction.LASER_DRILL);
        registerAreaRender(event, ModuleAgricultureHusbandry.MOB_DUPLICATOR);
        registerAreaRender(event, ModuleMisc.MOB_DETECTOR);

        event.registerBlockEntityRenderer((BlockEntityType<? extends MycelialReactorTile>) ModuleGenerator.MYCELIAL_REACTOR.type().get(), MycelialReactorTESR::new);

        event.registerEntityRenderer((EntityType<? extends InfinityTridentEntity>) ModuleTool.TRIDENT_ENTITY_TYPE.value(), InfinityTridentRenderer::new);
        event.registerEntityRenderer((EntityType<? extends InfinityNukeEntity>) ModuleTool.INFINITY_NUKE_ENTITY_TYPE.value(), InfinityNukeRenderer::new);
        event.registerEntityRenderer((EntityType<? extends InfinityLauncherProjectileEntity>) ModuleTool.INFINITY_LAUNCHER_PROJECTILE_ENTITY_TYPE.value(), InfinityLauncherProjectileRenderer::new);

        event.registerBlockEntityRenderer(((BlockEntityType<? extends TransporterTile>) ModuleTransportStorage.TRANSPORTER.type().get()), TransporterTESR::new);

        event.registerBlockEntityRenderer(((BlockEntityType<? extends ConveyorTile>) ModuleTransportStorage.CONVEYOR.type().get()), FluidConveyorTESR::new);
    }

    private static void registerAreaRender(EntityRenderersEvent.RegisterRenderers event, BlockWithTile pair) {
        event.registerBlockEntityRenderer((BlockEntityType<? extends IndustrialAreaWorkingTile>) pair.type().get(), WorkingAreaTESR::new);
    }

    @SubscribeEvent
    public static void addLayers(EntityRenderersEvent.AddLayers event) {
        for (var skin : event.getSkins()) {
            var playerRenderer = event.getPlayerRenderer(skin);
            if (playerRenderer != null) {
                playerRenderer.addLayer(new ContributorsCatEarsRender(playerRenderer));
                playerRenderer.addLayer(new InfinityLauncherProjectileArmorLayer(playerRenderer, event.getContext()));
            }
        }
    }

    @SubscribeEvent
    public static void layerDefinitions(EntityRenderersEvent.RegisterLayerDefinitions event) {
        event.registerLayerDefinition(InfinityTridentRenderer.TRIDENT_LAYER, InfinityTridentModel::createBodyLayer);
        event.registerLayerDefinition(InfinityNukeRenderer.NUKE_LAYER, InfinityNukeModel::createBodyLayer);
        event.registerLayerDefinition(InfinityNukeRenderer.NUKE_ARMED_LAYER, () -> InfinityNukeModelArmed.createBodyLayer(new CubeDeformation(0f)));
        event.registerLayerDefinition(InfinityNukeRenderer.NUKE_ARMED_BIG_LAYER, () -> InfinityNukeModelArmed.createBodyLayer(new CubeDeformation(0.2f)));
        event.registerLayerDefinition(InfinityLauncherProjectileRenderer.PROJECTILE_LAYER, InfinityLauncherProjectileModel::createBodyLayer);
    }

    @SubscribeEvent
    public static void registerModels(net.neoforged.neoforge.client.event.ModelEvent.RegisterStandalone event) {
        event.register(EARS_MODEL, net.neoforged.neoforge.client.model.standalone.SimpleUnbakedStandaloneModel.simpleModelWrapper(Identifier.fromNamespaceAndPath(Reference.MOD_ID,"block/catears")));
    }
    @SubscribeEvent
    public static void modelsLoaded(net.neoforged.neoforge.client.event.ModelEvent.BakingCompleted event) {
        ears_baked = event.getModelManager().getStandaloneModel(EARS_MODEL);
        com.buuz135.industrial.proxy.client.render.item.MachineItemTint.clearCache();
    }
    @SubscribeEvent
    public static void itemModels(net.neoforged.neoforge.client.event.RegisterItemModelsEvent event) {
        event.register(Identifier.fromNamespaceAndPath(Reference.MOD_ID,"hydroponic_processor"), HydroponicSimProcessorISTER.Unbaked.CODEC);
    }
    @SubscribeEvent
    public static void modelProperties(net.neoforged.neoforge.client.event.RegisterRangeSelectItemModelPropertyEvent event) {
        event.register(Identifier.fromNamespaceAndPath(Reference.MOD_ID, "cooldown"), com.buuz135.industrial.proxy.client.render.item.MachineModelProperty.COOLDOWN);
        event.register(Identifier.fromNamespaceAndPath(Reference.MOD_ID, "stored"), com.buuz135.industrial.proxy.client.render.item.MachineModelProperty.STORED);
    }
    @SubscribeEvent
    public static void itemTints(net.neoforged.neoforge.client.event.RegisterColorHandlersEvent.ItemTintSources event) {
        event.register(Identifier.fromNamespaceAndPath(Reference.MOD_ID,"machine"), com.buuz135.industrial.proxy.client.render.item.MachineItemTint.CODEC);
    }
    @SubscribeEvent
    public static void blockTints(net.neoforged.neoforge.client.event.RegisterColorHandlersEvent.BlockTintSources event) {
        event.register(java.util.List.of(new net.minecraft.client.color.block.BlockTintSource() {
            @Override public int color(net.minecraft.world.level.block.state.BlockState state) { return -1; }
            @Override public int colorInWorld(net.minecraft.world.level.block.state.BlockState state, net.minecraft.client.renderer.block.BlockAndTintGetter level, net.minecraft.core.BlockPos pos) {
                return level.getBlockEntity(pos) instanceof ConveyorTile conveyor ? ARGB.opaque(conveyor.getColor()) : -1;
            }
        }), ModuleTransportStorage.CONVEYOR.getBlock());
    }
    @SubscribeEvent
    public static void keys(net.neoforged.neoforge.client.event.RegisterKeyMappingsEvent event) {
        OPEN_BACKPACK = new KeyMapping("key.industrialforegoing.backpack.desc", -1, KeyMapping.Category.register(Identifier.fromNamespaceAndPath(Reference.MOD_ID,"general")));
        event.register(OPEN_BACKPACK);
    }
    @SubscribeEvent
    public static void particles(net.neoforged.neoforge.client.event.RegisterParticleGroupsEvent event) {
        event.register(com.buuz135.industrial.proxy.client.particle.ParticleVex.RENDER, com.buuz135.industrial.proxy.client.particle.ParticleVex.Group::new);
    }
    @SubscribeEvent
    public static void renderState(net.neoforged.neoforge.client.renderstate.RegisterRenderStateModifiersEvent event) {
        event.registerAvatarEntityModifier(new net.neoforged.neoforge.client.renderstate.AvatarRenderStateModifier() {
            @Override public <T extends net.minecraft.world.entity.Avatar & net.minecraft.client.entity.ClientAvatarEntity> void accept(T avatar, net.minecraft.client.renderer.entity.state.AvatarRenderState state) {
                ContributorsCatEarsRender.extract(avatar, state);
                state.setRenderData(InfinityLauncherProjectileArmorLayer.COUNT, InfinityLauncherProjectileArmorLayer.PROJECTILE_AMOUNT.getOrDefault(avatar.getUUID().toString(), 0));
            }
        });
    }
    @Override public void run() {
        NeoForge.EVENT_BUS.register(new IFClientEvents());
        EventManager.forge(ItemTooltipEvent.class).filter(event -> BuiltInRegistries.ITEM.getKey(event.getItemStack().getItem()).getNamespace().equals(Reference.MOD_ID)).process(event -> {
            if (Calendar.getInstance().get(Calendar.DAY_OF_MONTH) == 1 && Calendar.getInstance().get(Calendar.MONTH) == Calendar.APRIL)
                event.getToolTip().add(Component.translatable("text.industrialforegoing.proxy.client.alt_f4").withStyle(ChatFormatting.DARK_AQUA));
        }).subscribe();
    }
}
