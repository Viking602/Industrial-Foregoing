package com.buuz135.industrial.fluid;
@net.neoforged.fml.common.EventBusSubscriber(modid = "industrialforegoing", value = net.neoforged.api.distmarker.Dist.CLIENT)
public final class OreFluidClientEvents {
    @net.neoforged.bus.api.SubscribeEvent
    public static void models(net.neoforged.neoforge.client.event.RegisterFluidModelsEvent event) {
        for (var instance : OreFluidInstance.INSTANCES) {
            if (instance.renderProperties instanceof com.hrznstudio.titanium.fluid.TitaniumFluidRenderProperties properties) {
                event.register(new net.minecraft.client.renderer.block.FluidModel.Unbaked(
                        new net.minecraft.client.resources.model.sprite.Material(properties.getStillTexture()),
                        new net.minecraft.client.resources.model.sprite.Material(properties.getFlowingTexture()),
                        properties.getOverlayTexture() == null ? null : new net.minecraft.client.resources.model.sprite.Material(properties.getOverlayTexture()),
                        properties.getTintSource()), instance.getSourceFluid(), instance.getFlowingFluid());
            }
        }
    }
    @net.neoforged.bus.api.SubscribeEvent
    public static void extensions(net.neoforged.neoforge.client.extensions.common.RegisterClientExtensionsEvent event) {
        for (var instance : OreFluidInstance.INSTANCES) event.registerFluidType(instance.renderProperties, instance.getFluidType());
    }
}
