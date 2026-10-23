from pathlib import Path
root=Path('.work/Industrial-Foregoing/src/main/java/com/buuz135/industrial')
p=root/'proxy/client/ClientProxy.java';s=p.read_text()
for imp in ['net.minecraft.client.renderer.BlockEntityWithoutLevelRenderer','net.minecraft.client.renderer.ItemBlockRenderTypes','net.minecraft.client.renderer.entity.player.PlayerRenderer','net.minecraft.client.renderer.item.ItemProperties','net.minecraft.client.resources.model.BakedModel']:
 s=s.replace('import '+imp+';','')
s=s.replace('@EventBusSubscriber(value = Dist.CLIENT, bus = EventBusSubscriber.Bus.MOD)','@EventBusSubscriber(value = Dist.CLIENT, modid = Reference.MOD_ID)')
s=s.replace('    public static BakedModel ears_baked;\n    public static BakedModel HYDROPONIC_SIM_PROCESSOR;', '''    public static net.minecraft.client.renderer.block.dispatch.BlockStateModelPart ears_baked;
    private static final net.neoforged.neoforge.client.model.standalone.StandaloneModelKey<net.minecraft.client.renderer.block.dispatch.BlockStateModelPart> EARS_MODEL = new net.neoforged.neoforge.client.model.standalone.StandaloneModelKey<>(() -> "industrialforegoing:cat_ears");''')
s=s.replace('for (PlayerSkin.Model skin : event.getSkins())', 'for (var skin : event.getSkins())').replace('var renderer = event.getSkin(skin);', 'var playerRenderer = event.getPlayerRenderer(skin);').replace('if (renderer instanceof PlayerRenderer playerRenderer)', 'if (playerRenderer != null)').replace('new InfinityLauncherProjectileArmorLayer(playerRenderer)', 'new InfinityLauncherProjectileArmorLayer(playerRenderer, event.getContext())')
a=s.index('    @SubscribeEvent\n    public static void registerClientExtensions');s=s[:a]+'''    @SubscribeEvent
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
''';p.write_text(s)
