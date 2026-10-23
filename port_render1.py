from pathlib import Path
import re
root=Path('.work/Industrial-Foregoing/src/main/java')
for p in root.rglob('*.java'):
 s=p.read_text()
 s=s.replace('Minecraft.getInstance().getEntityRenderDispatcher().cameraOrientation()', 'Minecraft.getInstance().gameRenderer.getMainCamera().rotation()')
 s=s.replace('net.minecraft.client.renderer.entity.ItemRenderer.getFoilBufferDirect', 'com.buuz135.industrial.compat.RenderCompat.getFoilBufferDirect')
 s=s.replace('Minecraft.getInstance().getItemRenderer().renderStatic', 'com.buuz135.industrial.compat.RenderCompat.renderStatic')
 if p.name in ['WorkingAreaTESR.java','FluidConveyorTESR.java','MycelialReactorTESR.java','TransporterTESR.java']:
  s=re.sub(r'implements BlockEntityRenderer<([^>]+)>',r'extends com.buuz135.industrial.compat.CapturedBlockRenderer<\1>',s)
  a=s.index('    public static RenderType createRenderType('); b=s.index('\n    }',a)+6
  if p.name=='WorkingAreaTESR.java':method='    public static RenderType createRenderType() { return net.minecraft.client.renderer.rendertype.RenderTypes.debugQuads(); }'
  elif p.name=='FluidConveyorTESR.java':method='    public static RenderType createRenderType(Identifier texture) { return net.minecraft.client.renderer.rendertype.RenderTypes.entityTranslucentEmissive(texture); }'
  elif p.name=='MycelialReactorTESR.java':method='    public static RenderType createRenderType() { return net.minecraft.client.renderer.rendertype.RenderTypes.entityTranslucentEmissive(Identifier.fromNamespaceAndPath("industrialforegoing", "textures/block/mycelial.png")); }'
  else:method='    public static RenderType createRenderType() { return net.minecraft.client.renderer.rendertype.RenderTypes.entityTranslucentEmissive(TEXTURE); }'
  s=s[:a]+method+s[b:]
  s=s.replace('import com.mojang.blaze3d.platform.GlStateManager;','').replace('import net.minecraft.client.renderer.RenderStateShard;','')
  if 'import net.minecraft.client.renderer.rendertype.RenderType;' not in s:s=s.replace('import net.minecraft.client.Minecraft;', 'import net.minecraft.client.Minecraft;\nimport net.minecraft.client.renderer.rendertype.RenderType;')
  s=re.sub(r'        RenderSystem.lineWidth\([^\n]+\);\n','',s)
  s=s.replace('RenderType.lines()', 'net.minecraft.client.renderer.rendertype.RenderTypes.lines()').replace('LevelRenderer.renderLineBox', 'com.buuz135.industrial.compat.RenderCompat.renderLineBox')
  s=s.replace('shouldRenderOffScreen(IndustrialAreaWorkingTile te)', 'shouldRenderOffScreen()')
  s=s.replace('BlockEntityRenderer.super.getRenderBoundingBox(blockEntity)', 'super.getRenderBoundingBox(blockEntity)')
 if p.name in ['InfinityTridentRenderer.java','InfinityNukeRenderer.java','InfinityLauncherProjectileRenderer.java']:
  s=s.replace('extends EntityRenderer<', 'extends com.buuz135.industrial.compat.CapturedEntityRenderer<')
  s=re.sub(r'        super.render\([^;]+;\n','',s)
  s=s.replace('RenderType.', 'net.minecraft.client.renderer.rendertype.RenderTypes.').replace('0xFFFFFF)', '0xFFFFFFFF)')
 if p.name in ['InfinityTridentModel.java','InfinityNukeModel.java','InfinityNukeModelArmed.java','InfinityLauncherProjectileModel.java']:
  s=re.sub(r'extends EntityModel<[^>]+>', 'extends EntityModel<net.minecraft.client.renderer.entity.state.EntityRenderState>',s)
  s=s.replace('(ModelPart model) {', '(ModelPart model) {\n        super(model);')
  s=re.sub(r'    @Override\n    public void setupAnim\([^)]*\) \{.*?\n    \}\n','',s,flags=re.S)
  s=re.sub(r'    @Override\n    public void renderToBuffer\([^)]*\) \{.*?\n    \}\n','',s,flags=re.S)
 p.write_text(s)
