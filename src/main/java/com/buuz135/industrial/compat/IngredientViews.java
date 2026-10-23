package com.buuz135.industrial.compat;

import net.neoforged.neoforge.fluids.FluidStack;
import net.neoforged.neoforge.fluids.crafting.SizedFluidIngredient;
import java.util.List;

public final class IngredientViews {
    private IngredientViews() {}
    public static List<FluidStack> fluids(SizedFluidIngredient ingredient) {
        return ingredient.ingredient().fluids().stream().map(fluid -> new FluidStack(fluid, ingredient.amount())).toList();
    }
}
