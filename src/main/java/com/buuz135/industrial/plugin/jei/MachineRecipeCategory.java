package com.buuz135.industrial.plugin.jei;

import mezz.jei.api.gui.builder.ITooltipBuilder;
import mezz.jei.api.gui.drawable.IDrawable;
import mezz.jei.api.gui.ingredient.IRecipeSlotsView;
import mezz.jei.api.recipe.category.IRecipeCategory;
import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.network.chat.Component;
import java.util.List;

/** Shared dimensions and background/tooltip extraction for the machine layouts. */
public interface MachineRecipeCategory<T> extends IRecipeCategory<T> {
    IDrawable getBackground();
    @Override default int getWidth() { return getBackground().getWidth(); }
    @Override default int getHeight() { return getBackground().getHeight(); }
    @Override default void draw(T recipe, IRecipeSlotsView slots, GuiGraphicsExtractor gui, double x, double y) {
        getBackground().draw(gui, 0, 0);
    }
    default List<Component> getTooltipStrings(T recipe, IRecipeSlotsView slots, double x, double y) { return List.of(); }
    @Override default void getTooltip(ITooltipBuilder tooltip, T recipe, IRecipeSlotsView slots, double x, double y) {
        for (Component line : getTooltipStrings(recipe, slots, x, y)) tooltip.add(line);
    }
}
