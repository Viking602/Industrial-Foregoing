package com.buuz135.industrial.plugin.patchouli;

import com.buuz135.industrial.block.core.tile.DissolutionChamberTile;
import com.buuz135.industrial.module.ModuleCore;
import com.buuz135.industrial.recipe.DissolutionChamberRecipe;
import com.buuz135.industrial.utils.Reference;
import com.mojang.blaze3d.systems.RenderSystem;
import net.minecraft.ChatFormatting;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.renderer.texture.AbstractTexture;
import net.minecraft.client.renderer.texture.TextureAtlas;
import net.minecraft.client.renderer.texture.TextureAtlasSprite;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.util.ARGB;
import net.minecraft.world.inventory.InventoryMenu;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.crafting.RecipeType;
import net.minecraft.world.level.Level;
import net.neoforged.neoforge.client.extensions.common.IClientFluidTypeExtensions;
import net.neoforged.neoforge.fluids.FluidStack;
import vazkii.patchouli.client.book.gui.GuiBook;
import vazkii.patchouli.client.book.page.abstr.PageDoubleRecipeRegistry;

import java.util.Arrays;
import java.util.List;
import java.util.Optional;

public class PageDissolution extends PageDoubleRecipeRegistry<DissolutionChamberRecipe, com.buuz135.industrial.recipe.display.DissolutionRecipeDisplay> {
    public final Identifier patchouliTexture = Identifier.fromNamespaceAndPath(Reference.MOD_ID, "textures/gui/patchouli.png");

    @SuppressWarnings("unchecked")
    public PageDissolution() {
        super((RecipeType<? extends DissolutionChamberRecipe>) ModuleCore.DISSOLUTION_TYPE.get(), com.buuz135.industrial.recipe.display.DissolutionRecipeDisplay.class);
    }

    @Override
    protected void drawRecipe(GuiGraphicsExtractor graphics, com.buuz135.industrial.recipe.display.DissolutionRecipeDisplay display, net.minecraft.util.context.ContextMap context, int recipeX, int recipeY, int mouseX, int mouseY, boolean second) {
        DissolutionChamberRecipe recipe = display.recipe();
        Level level = Minecraft.getInstance().level;
        if (level == null) {
            return;
        }

        com.buuz135.industrial.compat.MachineGui.blit(graphics, patchouliTexture, recipeX - 6, recipeY, 0, 0, 128, 70, 128, 128);

        parent.drawCenteredStringNoShadow(graphics, getTitle(second).getVisualOrderText(), GuiBook.PAGE_WIDTH / 2, recipeY - 10, book.headerColor);

        for (int i = 0; i < recipe.input.size(); i++) {
            parent.renderIngredient(graphics,
                    recipeX + DissolutionChamberTile.getSlotPos(i).getLeft(),
                    recipeY + DissolutionChamberTile.getSlotPos(i).getRight() + 6,
                    mouseX, mouseY,
                    recipe.input.get(i));
        }
        if (recipe.inputFluid != null && !recipe.inputFluid.ingredient().fluids().isEmpty()) {
            Optional<FluidStack> optionalInputFluid = com.buuz135.industrial.compat.IngredientViews.fluids(recipe.inputFluid).stream().findFirst();
            optionalInputFluid.ifPresent(fluidStack -> renderFluid(graphics, recipeX + 22, recipeY + 28, mouseX, mouseY, fluidStack));
        }
        if (!recipe.output().isEmpty()) {
            ItemStack stack = recipe.output().get();
            parent.renderItemStack(graphics, recipeX + 79, recipeY + 28, mouseX, mouseY, stack);
        }

        parent.renderItemStack(graphics, recipeX + 79, recipeY + 49, mouseX, mouseY, recipe.getToastSymbol());
    }


    @Override
    protected int getRecipeHeight() {
        return 70;
    }

    private void renderFluid(GuiGraphicsExtractor graphics, int x, int y, int mouseX, int mouseY, FluidStack fluid) {
        if (fluid == null || fluid.isEmpty())
            return;

        var model = Minecraft.getInstance().getModelManager().getFluidStateModelSet().get(fluid.getFluid().defaultFluidState());
        TextureAtlasSprite sprite = model.stillMaterial().sprite();
        int color = model.fluidTintSource() == null ? -1 : model.fluidTintSource().colorAsStack(fluid);
        graphics.blitSprite(net.minecraft.client.renderer.RenderPipelines.GUI_TEXTURED, sprite, x, y, 16, 16, color);
        if (parent.isMouseInRelativeRange(mouseX, mouseY, x, y, 16, 16)) {
            parent.setTooltip(List.of(fluid.getHoverName(), Component.literal(fluid.getAmount() + " mB").withStyle(ChatFormatting.GRAY)));
        }
    }
}
