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

package com.buuz135.industrial.module;

import com.buuz135.industrial.IndustrialForegoing;
import com.buuz135.industrial.api.conveyor.ConveyorUpgradeFactory;
import com.buuz135.industrial.api.transporter.TransporterTypeFactory;
import com.buuz135.industrial.block.IndustrialBlockItem;
import com.buuz135.industrial.block.transportstorage.ConveyorBlock;
import com.buuz135.industrial.block.transportstorage.TransporterBlock;
import com.buuz135.industrial.block.transportstorage.conveyor.*;
import com.buuz135.industrial.block.transportstorage.transporter.TransporterFluidType;
import com.buuz135.industrial.block.transportstorage.transporter.TransporterItemType;
import com.buuz135.industrial.block.transportstorage.transporter.TransporterWorldType;
import com.buuz135.industrial.gui.conveyor.ContainerConveyor;
import com.buuz135.industrial.gui.transporter.ContainerTransporter;
import com.buuz135.industrial.item.ItemConveyorUpgrade;
import com.buuz135.industrial.item.ItemTransporterType;
import com.buuz135.industrial.proxy.client.model.ConveyorBlockModel;
import com.buuz135.industrial.proxy.client.model.TransporterBlockModel;
import com.buuz135.industrial.utils.Reference;
import com.hrznstudio.titanium.event.handler.EventManager;
import com.hrznstudio.titanium.module.BlockWithTile;
import com.hrznstudio.titanium.module.DeferredRegistryHelper;
import com.hrznstudio.titanium.tab.TitaniumTab;
import com.mojang.math.Transformation;
import net.minecraft.client.resources.model.*;
import net.minecraft.core.Direction;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.Identifier;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.api.distmarker.OnlyIn;
import net.neoforged.fml.loading.FMLEnvironment;
import net.neoforged.neoforge.client.event.ModelEvent;

import net.neoforged.neoforge.common.extensions.IMenuTypeExtension;

import java.util.HashMap;

public class ModuleTransportStorage implements IModule {

    public static TitaniumTab TAB_TRANSPORT = new TitaniumTab(Identifier.fromNamespaceAndPath(Reference.MOD_ID, "transport"));

    public static ConveyorUpgradeFactory upgrade_extraction = new ConveyorExtractionUpgrade.Factory();
    public static ConveyorUpgradeFactory upgrade_insertion = new ConveyorInsertionUpgrade.Factory();
    public static ConveyorUpgradeFactory upgrade_detector = new ConveyorDetectorUpgrade.Factory();
    public static ConveyorUpgradeFactory upgrade_bouncing = new ConveyorBouncingUpgrade.Factory();
    public static ConveyorUpgradeFactory upgrade_dropping = new ConveyorDroppingUpgrade.Factory();
    public static ConveyorUpgradeFactory upgrade_blinking = new ConveyorBlinkingUpgrade.Factory();
    public static ConveyorUpgradeFactory upgrade_splitting = new ConveyorSplittingUpgrade.Factory();

    public static BlockWithTile CONVEYOR = IndustrialForegoing.INSTANCE.getRegistries().registerBlockWithTileItem("conveyor", () -> new ConveyorBlock(TAB_TRANSPORT), blockRegistryObject -> () -> new IndustrialBlockItem(blockRegistryObject.get(), TAB_TRANSPORT), TAB_TRANSPORT);
    public static HashMap<Identifier, net.minecraft.client.renderer.block.dispatch.BlockStateModelPart> CONVEYOR_UPGRADES_CACHE = new HashMap<>();

    public static TransporterTypeFactory ITEM_TRANSPORTER = new TransporterItemType.Factory();
    public static TransporterTypeFactory FLUID_TRANSPORTER = new TransporterFluidType.Factory();
    public static TransporterTypeFactory WORLD_TRANSPORTER = new TransporterWorldType.Factory();

    public static BlockWithTile TRANSPORTER = IndustrialForegoing.INSTANCE.getRegistries().registerBlockWithTileItem("transporter", () -> new TransporterBlock(), blockRegistryObject -> () -> new TransporterBlock.Item(blockRegistryObject.get(), TAB_TRANSPORT), TAB_TRANSPORT);
    public static HashMap<Identifier, net.minecraft.client.renderer.block.dispatch.BlockStateModelPart> TRANSPORTER_CACHE = new HashMap<>();

    @Override
    public void generateFeatures(DeferredRegistryHelper registryHelper) {
        ContainerConveyor.TYPE = registryHelper.registerGeneric(Registries.MENU, "conveyor", () -> IMenuTypeExtension.create(ContainerConveyor::new));
        ConveyorUpgradeFactory.FACTORIES.forEach(conveyorUpgradeFactory -> registryHelper.registerGeneric(Registries.ITEM, "conveyor_" + conveyorUpgradeFactory.getName() + "_upgrade", () -> new ItemConveyorUpgrade(conveyorUpgradeFactory, TAB_TRANSPORT)));
        ContainerTransporter.TYPE = registryHelper.registerGeneric(Registries.MENU, "transporter", () -> IMenuTypeExtension.create(ContainerTransporter::new));
        TransporterTypeFactory.FACTORIES.forEach(transporterTypeFactory -> registryHelper.registerGeneric(Registries.ITEM, transporterTypeFactory.getName() + "_transporter_type", () -> new ItemTransporterType(transporterTypeFactory, TAB_TRANSPORT)));
        if (FMLEnvironment.getDist().isClient()) {
            new Client().onClient();
        }
    }

    private static final class Client {
    private static final java.util.Map<Identifier, net.neoforged.neoforge.client.model.standalone.StandaloneModelKey<net.minecraft.client.renderer.block.dispatch.BlockStateModelPart>> MODEL_KEYS = new HashMap<>();

    private void registerModels(ModelEvent.RegisterStandalone event) {
        java.util.Set<Identifier> models = new java.util.HashSet<>();
        for (var factory : TransporterTypeFactory.FACTORIES) for (var facing : factory.getValidFacings()) for (var action : TransporterTypeFactory.TransporterAction.values()) models.add(factory.getModel(facing,action));
        for (var factory : ConveyorUpgradeFactory.FACTORIES) for (var facing : factory.getValidFacings()) for (var conveyor : ConveyorBlock.FACING.getPossibleValues()) models.add(factory.getModel(facing,conveyor));
        for (var id : models) {
            var key = MODEL_KEYS.computeIfAbsent(id, name -> new net.neoforged.neoforge.client.model.standalone.StandaloneModelKey<>(name::toString));
            event.register(key, net.neoforged.neoforge.client.model.standalone.SimpleUnbakedStandaloneModel.simpleModelWrapper(id));
        }
    }
    private void bakingCompleted(ModelEvent.BakingCompleted event) {
        CONVEYOR_UPGRADES_CACHE.clear();
        TRANSPORTER_CACHE.clear();
        MODEL_KEYS.forEach((id,key) -> {
            var model = event.getModelManager().getStandaloneModel(key);
            CONVEYOR_UPGRADES_CACHE.put(id,model);
            TRANSPORTER_CACHE.put(id,model);
        });
    }
    private void modifyBakingResult(ModelEvent.ModifyBakingResult event) {
        event.getBakingResult().blockStateModels().replaceAll((state,model) -> {
            if (state.is(CONVEYOR.getBlock())) return new ConveyorBlockModel(model);
            if (state.is(TRANSPORTER.getBlock())) return new TransporterBlockModel(model);
            return model;
        });
    }
    private void onClient() {
        EventManager.mod(ModelEvent.RegisterStandalone.class).process(this::registerModels).subscribe();
        EventManager.mod(ModelEvent.BakingCompleted.class).process(this::bakingCompleted).subscribe();
        EventManager.mod(ModelEvent.ModifyBakingResult.class).process(this::modifyBakingResult).subscribe();
    }
}
}
