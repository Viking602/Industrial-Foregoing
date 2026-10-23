package com.buuz135.industrial.compat;

import net.minecraft.core.HolderLookup;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.crafting.*;

/** Recipes executed by Industrial Foregoing machines, outside the vanilla recipe book. */
public interface MachineRecipe extends Recipe<CraftingInput> {
    @Override default boolean isSpecial() { return true; }
    @Override default boolean showNotification() { return false; }
    @Override default String group() { return ""; }
    @Override default PlacementInfo placementInfo() { return PlacementInfo.NOT_PLACEABLE; }
    @Override default RecipeBookCategory recipeBookCategory() { return RecipeBookCategories.CRAFTING_MISC; }
    default boolean canCraftInDimensions(int width, int height) { return false; }
    default ItemStack getResultItem(HolderLookup.Provider registries) { return ItemStack.EMPTY; }
    default ItemStack getToastSymbol() { return ItemStack.EMPTY; }
}
