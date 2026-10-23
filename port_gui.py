from pathlib import Path
import re
root=Path(__file__).resolve().parent
for f in (root/'src/main/java').rglob('*.java'):
    s=f.read_text(encoding='utf-8')
    s=s.replace('getResourceLocation()', 'getIdentifier()')
    if 'GuiGraphicsExtractor' in s:
        s=s.replace('.renderComponentTooltip(', '.setComponentTooltipForNextFrame(')
        s=s.replace('.renderItemDecorations(','.itemDecorations(')
        s=s.replace('.pose().pushPose()', '.pose().pushMatrix()').replace('.pose().popPose()', '.pose().popMatrix()')
        s=re.sub(r'(\.pose\(\)\.scale\([^,]+,[^,]+),[^)]+\)',r'\1)',s)
        s=re.sub(r'(\w+)\.pose\(\)\.translate\(0,\s*0,\s*\d+\);',r'\1.nextStratum();',s)
        s=re.sub(r'(?<![\w])0x([0-9A-Fa-f]{6})(?![0-9A-Fa-f])',r'0xFF\1',s)
    if f.name in ['GuiConveyor.java','GuiTransporter.java']:
        s=s.replace('protected void renderBg(GuiGraphicsExtractor guiGraphics, float partialTicks, int mouseX, int mouseY) {','public void extractBackground(GuiGraphicsExtractor guiGraphics, int mouseX, int mouseY, float partialTicks) {\n        super.extractBackground(guiGraphics, mouseX, mouseY, partialTicks);')
        s=s.replace('protected void renderLabels(', 'protected void extractLabels(').replace('renderTooltip(guiGraphics,', 'extractTooltip(guiGraphics,')
        s=re.sub(r'^\s*RenderSystem.setShader\([^\n]+\);\n','\n',s,flags=re.M)
        s=re.sub(r'^\s*RenderSystem.setShaderColor\(1\.0F, 1\.0F, 1\.0F, 1\.0F\);\n','\n',s,flags=re.M)
        s=s.replace('public boolean mouseClicked(double mouseX, double mouseY, int mouseButton) {', 'public boolean mouseClicked(net.minecraft.client.input.MouseButtonEvent event, boolean doubleClick) {\n        double mouseX = event.x(), mouseY = event.y();\n        int mouseButton = event.button();')
        s=s.replace('super.mouseClicked(mouseX, mouseY, mouseButton)', 'super.mouseClicked(event, doubleClick)')
    if f.name=='GeneratorBackgroundScreenAddon.java':
        s=s.replace('import com.mojang.blaze3d.platform.GlStateManager;','')
        a=s.index('        float scale = 4;'); b=s.index('\n    }',a)
        s=s[:a]+'''        int x = guiX + getPosX() - 24;
        int y = guiY + getPosY() - 24;
        guiGraphics.pose().pushMatrix();
        guiGraphics.pose().translate(x, y);
        guiGraphics.pose().scale(4f, 4f);
        guiGraphics.item(new ItemStack(type.getDisplay()), 0, 0);
        guiGraphics.pose().popMatrix();
        guiGraphics.nextStratum();
        guiGraphics.blit(net.minecraft.client.renderer.RenderPipelines.GUI_TEXTURED,
            IAssetProvider.DEFAULT_LOCATION, x, y, 4, 4, 64, 64, 256, 256, 0x99FFFFFF);'''+s[b:]
    if f.name=='ItemStackTankScreenAddon.java':
        a=s.index('        asset = IAssetProvider.getAsset(provider, type.getAssetType());'); b=s.index('\n    }',a)
        s=s[:a]+'''        asset = IAssetProvider.getAsset(provider, type.getAssetType());
        Rectangle area = asset.getArea();
        FluidStack fluid = tank.getFluidInTank(tankSlot);
        int capacity = tank.getTankCapacity(tankSlot);
        if (!fluid.isEmpty() && capacity > 0) {
            int usableHeight = area.height - asset.getFluidRenderPadding(Direction.UP) - asset.getFluidRenderPadding(Direction.DOWN);
            int height = (int) Math.clamp((long) fluid.getAmount() * usableHeight / capacity, 0, usableHeight);
            var model = screen.getMinecraft().getModelManager().getFluidStateModelSet().get(fluid.getFluid().defaultFluidState());
            int color = model.fluidTintSource() == null ? -1 : model.fluidTintSource().colorAsStack(fluid);
            int x = guiX + getPosX() + asset.getFluidRenderPadding(Direction.WEST);
            int y = guiY + getPosY() + asset.getFluidRenderPadding(Direction.UP);
            if (!fluid.is(Tags.Fluids.GASEOUS)) y += usableHeight - height;
            int width = area.width - asset.getFluidRenderPadding(Direction.WEST) - asset.getFluidRenderPadding(Direction.EAST);
            guiGraphics.blitSprite(net.minecraft.client.renderer.RenderPipelines.GUI_TEXTURED, model.stillMaterial().sprite(), x, y, width, height, color);
        }
        AssetUtil.drawAsset(guiGraphics, screen, asset, guiX + getPosX(), guiY + getPosY());'''+s[b:]
    f.write_text(s,encoding='utf-8')
print('GUI extraction, transforms, text colors and fluid display migrated')
