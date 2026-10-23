from pathlib import Path
import re
root=Path('.work/Industrial-Foregoing/src/main/java/com/buuz135/industrial')
p=root/'plugin/curios/InfinityBackpackCurios.java';s=p.read_text().replace('import net.minecraft.client.resources.model.BakedModel;','')
a=s.index('    @Override\n    public <T extends LivingEntity');s=s[:a]+'''    @Override
    public <S extends net.minecraft.client.renderer.entity.state.LivingEntityRenderState, M extends EntityModel<? super S>> void render(
            ItemStack stack, SlotContext slotContext, PoseStack matrixStack, net.minecraft.client.renderer.SubmitNodeCollector collector,
            int light, S state, RenderLayerParent<S, M> parent, net.minecraft.client.renderer.entity.EntityRendererProvider.Context context,
            float yRot, float xRot) {
        if (!(stack.getItem() instanceof ItemInfinityBackpack)) return;
        var itemState = new net.minecraft.client.renderer.item.ItemStackRenderState();
        context.getItemModelResolver().updateForLiving(itemState, stack, ItemDisplayContext.FIXED, slotContext.entity());
        matrixStack.pushPose();
        if (state instanceof net.minecraft.client.renderer.entity.state.HumanoidRenderState humanoid && humanoid.isCrouching) {
            matrixStack.translate(0, 0.2, 0);
            matrixStack.mulPose(Axis.XP.rotationDegrees((float) (90 / Math.PI)));
        }
        matrixStack.mulPose(Axis.XP.rotationDegrees(180));
        matrixStack.translate(0, -0.4, -0.2);
        matrixStack.scale(0.65f, 0.65f, 0.65f);
        itemState.submit(matrixStack, collector, light, OverlayTexture.NO_OVERLAY, 0);
        matrixStack.popPose();
    }
}
''';p.write_text(s)
p=root/'plugin/curios/MeatFeedCurios.java';s=p.read_text();s=s[:s.index('    @Override\n    public <T extends LivingEntity')]+ '}\n';p.write_text(s)
p=root/'module/ModuleCore.java';s=p.read_text();s=s.replace('    public static DeferredHolder<RecipeType<?>, RecipeType<?>> DISSOLUTION_TYPE;', '''    public static DeferredHolder<RecipeType<?>, RecipeType<?>> DISSOLUTION_TYPE;
    public static DeferredHolder<net.minecraft.world.item.crafting.display.RecipeDisplay.Type<?>, net.minecraft.world.item.crafting.display.RecipeDisplay.Type<com.buuz135.industrial.recipe.display.DissolutionRecipeDisplay>> DISSOLUTION_DISPLAY;''')
needle='        DISSOLUTION_SERIALIZER =';idx=s.index(needle);s=s[:idx]+'''        DISSOLUTION_DISPLAY = helper.registerGeneric(Registries.RECIPE_DISPLAY, "dissolution_chamber", () -> com.buuz135.industrial.recipe.display.DissolutionRecipeDisplay.TYPE);
'''+s[idx:];p.write_text(s)
p=root/'recipe/DissolutionChamberRecipe.java';s=p.read_text();idx=s.index('    @Override\n    public boolean matches(CraftingInput');s=s[:idx]+'''    @Override
    public List<net.minecraft.world.item.crafting.display.RecipeDisplay> display() {
        return List.of(new com.buuz135.industrial.recipe.display.DissolutionRecipeDisplay(this));
    }

'''+s[idx:];p.write_text(s)
p=root/'plugin/patchouli/PageDissolution.java';s=p.read_text();s=s.replace('PageDoubleRecipeRegistry<DissolutionChamberRecipe>', 'PageDoubleRecipeRegistry<DissolutionChamberRecipe, com.buuz135.industrial.recipe.display.DissolutionRecipeDisplay>').replace('ModuleCore.DISSOLUTION_TYPE.get());', 'ModuleCore.DISSOLUTION_TYPE.get(), com.buuz135.industrial.recipe.display.DissolutionRecipeDisplay.class);')
s=s.replace('GuiGraphicsExtractor graphics, DissolutionChamberRecipe recipe, int recipeX', 'GuiGraphicsExtractor graphics, com.buuz135.industrial.recipe.display.DissolutionRecipeDisplay display, net.minecraft.util.context.ContextMap context, int recipeX').replace('        Level level = Minecraft', '        DissolutionChamberRecipe recipe = display.recipe();\n        Level level = Minecraft')
s=s.replace('        RenderSystem.enableBlend();\n','').replace('recipe.inputFluid.ingredient().isEmpty()', 'recipe.inputFluid.ingredient().fluids().isEmpty()').replace('Arrays.stream(recipe.inputFluid.getFluids())', 'com.buuz135.industrial.compat.IngredientViews.fluids(recipe.inputFluid).stream()').replace('            stack.getItem().onCraftedBy(stack, null, null);\n','')
s=re.sub(r'    @Override\n    protected ItemStack getRecipeOutput\(.*?\n    \}\n','',s,flags=re.S)
a=s.index('        final IClientFluidTypeExtensions');s=s[:a]+'''        var model = Minecraft.getInstance().getModelManager().getFluidStateModelSet().get(fluid.getFluid().defaultFluidState());
        TextureAtlasSprite sprite = model.stillMaterial().sprite();
        int color = model.fluidTintSource() == null ? -1 : model.fluidTintSource().colorAsStack(fluid);
        com.buuz135.industrial.compat.MachineGui.blit(graphics, x, y, 0, 16, 16, sprite,
                ARGB.red(color) / 255f, ARGB.green(color) / 255f, ARGB.blue(color) / 255f, ARGB.alpha(color) / 255f);
        if (parent.isMouseInRelativeRange(mouseX, mouseY, x, y, 16, 16)) {
            parent.setTooltip(List.of(fluid.getHoverName(), Component.literal(fluid.getAmount() + " mB").withStyle(ChatFormatting.GRAY)));
        }
    }
}
''';p.write_text(s)
p=root/'plugin/PatchouliPlugin.java';s=p.read_text().replace('BuiltInRegistries.ITEM.get(', 'BuiltInRegistries.ITEM.getValue(');p.write_text(s)
