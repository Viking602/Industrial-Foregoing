from pathlib import Path
root=Path('.work/Industrial-Foregoing/src/main/java/com/buuz135/industrial')
p=root/'proxy/client/render/FluidConveyorTESR.java';s=p.read_text();head=s[:s.index('public class FluidConveyorTESR')]
s=head+'''public class FluidConveyorTESR extends com.buuz135.industrial.compat.CapturedBlockRenderer<ConveyorTile> {
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
'''
p.write_text(s)
p=root/'utils/FluidUtils.java';s=p.read_text();a=s.index('    public static int getFluidColor(');s=s[:a]+'''    public static int getFluidColor(FluidStack stack) {
        if (stack.isEmpty()) return -1;
        var model = net.minecraft.client.Minecraft.getInstance().getModelManager().getFluidStateModelSet().get(stack.getFluid().defaultFluidState());
        int tint = model.fluidTintSource() == null ? -1 : model.fluidTintSource().colorAsStack(stack);
        return ARGB.multiply(ColorUtils.getColorFrom(model.stillMaterial().sprite()), tint);
    }
    public static int getFluidColor(Fluid fluid) { return getFluidColor(new FluidStack(fluid, 1000)); }
}
''';p.write_text(s)
p=root/'utils/ItemStackUtils.java';s=p.read_text();s=s.replace('return ColorUtils.getColorFrom(Minecraft.getInstance().getItemRenderer().getModel(stack, Minecraft.getInstance().level, Minecraft.getInstance().player, 0).getParticleIcon());','''var state = new net.minecraft.client.renderer.item.ItemStackRenderState();
        Minecraft.getInstance().getItemModelResolver().updateForTopItem(state, stack, net.minecraft.world.item.ItemDisplayContext.NONE, Minecraft.getInstance().level, null, 0);
        var material = state.pickParticleMaterial(net.minecraft.util.RandomSource.create(0));
        return material == null ? -1 : ColorUtils.getColorFrom(material.sprite());''');p.write_text(s)
for name,cache,modeldata,lookup in [('Conveyor','CONVEYOR_UPGRADES_CACHE','ConveyorModelData','upgrade.getFactory().getModel(upgrade.getSide(), state.getValue(com.buuz135.industrial.block.transportstorage.ConveyorBlock.FACING))'),('Transporter','TRANSPORTER_CACHE','TransporterModelData','upgrade.getFactory().getModel(upgrade.getSide(), upgrade.getAction())')]:
 p=root/f'proxy/client/model/{name}BlockModel.java';s=p.read_text();head=s[:s.index('package ')]
 s=head+f'''package com.buuz135.industrial.proxy.client.model;
import com.buuz135.industrial.module.ModuleTransportStorage;
import net.minecraft.client.renderer.block.BlockAndTintGetter;
import net.minecraft.client.renderer.block.dispatch.BlockStateModel;
import net.minecraft.client.renderer.block.dispatch.BlockStateModelPart;
import net.minecraft.core.BlockPos;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.block.state.BlockState;
import net.neoforged.neoforge.client.model.DelegateBlockStateModel;
import java.util.List;

public class {name}BlockModel extends DelegateBlockStateModel {{
    public {name}BlockModel(BlockStateModel base) {{ super(base); }}
    @Override public void collectParts(BlockAndTintGetter level, BlockPos pos, BlockState state, RandomSource random, List<BlockStateModelPart> parts) {{
        super.collectParts(level,pos,state,random,parts);
        var data = level.getModelData(pos).get({modeldata}.UPGRADE_PROPERTY);
        if (data != null) for (var upgrade : data.getUpgrades().values()) {{
            if (upgrade == null) continue;
            var model = ModuleTransportStorage.{cache}.get({lookup});
            if (model != null) parts.add(model);
        }}
    }}
}}
''';p.write_text(s)
p=root/'module/ModuleTransportStorage.java';s=p.read_text();s=s.replace('HashMap<Identifier, BakedModel>', 'HashMap<Identifier, net.minecraft.client.renderer.block.dispatch.BlockStateModelPart>')
a=s.index('    @OnlyIn(Dist.CLIENT)\n    private void bakingCompleted');s=s[:a]+'''    private static final java.util.Map<Identifier, net.neoforged.neoforge.client.model.standalone.StandaloneModelKey<net.minecraft.client.renderer.block.dispatch.BlockStateModelPart>> MODEL_KEYS = new HashMap<>();

    @OnlyIn(Dist.CLIENT)
    private void registerModels(ModelEvent.RegisterStandalone event) {
        java.util.Set<Identifier> models = new java.util.HashSet<>();
        for (var factory : TransporterTypeFactory.FACTORIES) for (var facing : factory.getValidFacings()) for (var action : TransporterTypeFactory.TransporterAction.values()) models.add(factory.getModel(facing,action));
        for (var factory : ConveyorUpgradeFactory.FACTORIES) for (var facing : factory.getValidFacings()) for (var conveyor : ConveyorBlock.FACING.getPossibleValues()) models.add(factory.getModel(facing,conveyor));
        for (var id : models) {
            var key = MODEL_KEYS.computeIfAbsent(id, name -> new net.neoforged.neoforge.client.model.standalone.StandaloneModelKey<>(name::toString));
            event.register(key, net.neoforged.neoforge.client.model.standalone.SimpleUnbakedStandaloneModel.simpleModelWrapper(id));
        }
    }
    @OnlyIn(Dist.CLIENT)
    private void bakingCompleted(ModelEvent.BakingCompleted event) {
        CONVEYOR_UPGRADES_CACHE.clear();
        TRANSPORTER_CACHE.clear();
        MODEL_KEYS.forEach((id,key) -> {
            var model = event.getModelManager().getStandaloneModel(key);
            CONVEYOR_UPGRADES_CACHE.put(id,model);
            TRANSPORTER_CACHE.put(id,model);
        });
    }
    @OnlyIn(Dist.CLIENT)
    private void modifyBakingResult(ModelEvent.ModifyBakingResult event) {
        event.getBakingResult().blockStateModels().replaceAll((state,model) -> {
            if (state.is(CONVEYOR.getBlock())) return new ConveyorBlockModel(model);
            if (state.is(TRANSPORTER.getBlock())) return new TransporterBlockModel(model);
            return model;
        });
    }
    @OnlyIn(Dist.CLIENT)
    private void onClient() {
        EventManager.mod(ModelEvent.RegisterStandalone.class).process(this::registerModels).subscribe();
        EventManager.mod(ModelEvent.BakingCompleted.class).process(this::bakingCompleted).subscribe();
        EventManager.mod(ModelEvent.ModifyBakingResult.class).process(this::modifyBakingResult).subscribe();
    }
}
''';s=s.replace('import net.neoforged.neoforge.client.model.SimpleModelState;','');p.write_text(s)
