package com.buuz135.industrial.recipe.display;

import com.buuz135.industrial.module.ModuleCore;
import com.buuz135.industrial.recipe.DissolutionChamberRecipe;
import com.mojang.serialization.MapCodec;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.world.item.ItemStackTemplate;
import net.minecraft.world.item.crafting.display.RecipeDisplay;
import net.minecraft.world.item.crafting.display.SlotDisplay;
import net.neoforged.neoforge.fluids.crafting.display.FluidStackSlotDisplay;

/** The synchronized recipe display also supplies the in-game manual. */
public record DissolutionRecipeDisplay(DissolutionChamberRecipe recipe) implements RecipeDisplay {
    public static final MapCodec<DissolutionRecipeDisplay> CODEC = DissolutionChamberRecipe.CODEC.xmap(DissolutionRecipeDisplay::new, DissolutionRecipeDisplay::recipe);
    public static final Type<DissolutionRecipeDisplay> TYPE = new Type<>(CODEC, ByteBufCodecs.fromCodecWithRegistries(CODEC.codec()));
    @Override public SlotDisplay result() {
        if (recipe.output().isPresent() && !recipe.output().get().isEmpty())
            return new SlotDisplay.ItemStackSlotDisplay(ItemStackTemplate.fromNonEmptyStack(recipe.output().get()));
        if (recipe.outputFluid().isPresent()) return new FluidStackSlotDisplay(recipe.outputFluid().get());
        return SlotDisplay.Empty.INSTANCE;
    }
    @Override public SlotDisplay craftingStation() { return new SlotDisplay.ItemSlotDisplay(ModuleCore.DISSOLUTION_CHAMBER.getBlock().asItem()); }
    @Override public Type<DissolutionRecipeDisplay> type() { return TYPE; }
}
