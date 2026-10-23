/*
 * This file is part of Industrial Foregoing.
 *
 * Copyright 2021, Buuz135
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of
 * this software and associated documentation files (the "Software"), to deal in the
 * Software without restriction, including without limitation the rights to use, copy,
 * modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
 * and to permit persons to whom the Software is furnished to do so, subject to the
 * following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all copies
 * or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
 * INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
 * PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
 * FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
 * ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

package com.buuz135.industrial.recipe;

import com.buuz135.industrial.module.ModuleCore;
import com.buuz135.industrial.utils.Reference;
import com.hrznstudio.titanium.component.fluid.FluidTankComponent;
import com.mojang.serialization.Codec;
import com.mojang.serialization.MapCodec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import net.minecraft.advancements.AdvancementRequirements;
import net.minecraft.advancements.AdvancementRewards;
import net.minecraft.advancements.criterion.RecipeUnlockedTrigger;
import net.minecraft.core.HolderLookup;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.data.recipes.RecipeOutput;
import net.minecraft.resources.Identifier;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.ItemStackTemplate;
import net.minecraft.world.item.crafting.*;
import net.minecraft.world.level.Level;
import net.neoforged.neoforge.common.conditions.ICondition;
import net.neoforged.neoforge.common.conditions.RegisteredCondition;
import net.neoforged.neoforge.fluids.FluidStack;
import net.neoforged.neoforge.fluids.FluidStackTemplate;
import net.neoforged.neoforge.fluids.capability.IFluidHandler;
import net.neoforged.neoforge.fluids.crafting.SizedFluidIngredient;
import net.neoforged.neoforge.items.IItemHandler;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;

public class DissolutionChamberRecipe implements com.buuz135.industrial.compat.MachineRecipe {

    public static final MapCodec<DissolutionChamberRecipe> CODEC = RecordCodecBuilder.mapCodec(in -> in.group(
            Ingredient.CODEC.listOf(0, 8).fieldOf("input").forGetter(o -> o.input),
            SizedFluidIngredient.CODEC.fieldOf("inputFluid").forGetter(o -> o.inputFluid),
            Codec.INT.fieldOf("processingTime").forGetter(o -> o.processingTime),
            ItemStackTemplate.CODEC.optionalFieldOf("output").forGetter(o -> o.outputTemplate),
            FluidStackTemplate.CODEC.optionalFieldOf("outputFluid").forGetter(o -> o.outputFluidTemplate)
    ).apply(in, (input, inputFluid, processingTime, output, outputFluid) -> new DissolutionChamberRecipe(input, inputFluid, processingTime, output, outputFluid, true)));

    public List<Ingredient> input;
    public SizedFluidIngredient inputFluid;
    public int processingTime;
    private Optional<ItemStackTemplate> outputTemplate;
    private Optional<FluidStackTemplate> outputFluidTemplate;

    public DissolutionChamberRecipe(List<Ingredient> input, SizedFluidIngredient inputFluid, int processingTime, Optional<ItemStack> output, Optional<FluidStack> outputFluid) {
        this.input = input;
        this.inputFluid = inputFluid;
        this.processingTime = processingTime;
        this.outputTemplate = output.map(ItemStackTemplate::fromNonEmptyStack);
        this.outputFluidTemplate = outputFluid.map(FluidStackTemplate::fromNonEmptyStack);
    }

    public DissolutionChamberRecipe(List<Ingredient> input, FluidStack inputFluid, int processingTime, Optional<ItemStack> output, Optional<FluidStack> outputFluid) {
        this.input = input;
        this.inputFluid = SizedFluidIngredient.of(inputFluid.getFluid(), inputFluid.getAmount());
        this.processingTime = processingTime;
        this.outputTemplate = output.map(ItemStackTemplate::fromNonEmptyStack);
        this.outputFluidTemplate = outputFluid.map(FluidStackTemplate::fromNonEmptyStack);
    }

    public DissolutionChamberRecipe() {

    }

    public static void createRecipe(RecipeOutput recipeOutput, String name, DissolutionChamberRecipe recipe) {
        var rl = generateRL(name);
        var advancementHolder = recipeOutput.advancement()
                .addCriterion("has_the_recipe", RecipeUnlockedTrigger.unlocked(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.RECIPE, rl)))
                .rewards(AdvancementRewards.Builder.recipe(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.RECIPE, rl)))
                .requirements(AdvancementRequirements.Strategy.OR).build(rl);
        List<ICondition> conditions = new ArrayList<>();
        if (recipe.output().isPresent())
            conditions.add(new RegisteredCondition<>(BuiltInRegistries.ITEM.getResourceKey(recipe.output().get().getItem()).orElseThrow()));
        recipeOutput.accept(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.RECIPE, rl), recipe, advancementHolder, conditions.toArray(new ICondition[conditions.size()]));
    }

    public static Identifier generateRL(String key) {
        return Identifier.fromNamespaceAndPath(Reference.MOD_ID, "dissolution_chamber/" + key);
    }

    public boolean matches(com.hrznstudio.titanium.component.inventory.InventoryComponent<?> handler, FluidTankComponent tank) {
        if (input == null || tank == null || inputFluid == null) return false;
        List<ItemStack> handlerItems = new ArrayList<>();
        for (int i = 0; i < handler.getSlots(); i++) {
            if (!handler.getStackInSlot(i).isEmpty()) handlerItems.add(handler.getStackInSlot(i).copy());
        }
        for (Ingredient ingredient : input) {
            boolean found = false;
            for (ItemStack stack : ingredient.items().map(net.minecraft.world.item.ItemStack::new).toArray(net.minecraft.world.item.ItemStack[]::new)) {
                int i = 0;
                for (; i < handlerItems.size(); i++) {
                    if (ItemStack.isSameItem(handlerItems.get(i), stack)) {
                        found = true;
                        break;
                    }
                }
                if (found) {
                    handlerItems.remove(i);
                    break;
                }
            }
            if (!found) return false;
        }
        // check the tank fluid is in ingredient
        boolean flag = inputFluid.test(tank.getFluid());

        return handlerItems.isEmpty() && flag && com.buuz135.industrial.compat.MachineFluids.drainForced(tank, tank.getFluid().copyWithAmount(inputFluid.amount()), IFluidHandler.FluidAction.SIMULATE).getAmount() == inputFluid.amount();
    }

    @Override
    public List<net.minecraft.world.item.crafting.display.RecipeDisplay> display() {
        return List.of(new com.buuz135.industrial.recipe.display.DissolutionRecipeDisplay(this));
    }

    @Override
    public boolean matches(CraftingInput craftingInput, Level level) {
        return false;
    }

    @Override
    public ItemStack assemble(CraftingInput craftingInput) {
        return ItemStack.EMPTY;
    }

    @Override
    public boolean canCraftInDimensions(int width, int height) {
        return false;
    }

    @Override
    public ItemStack getResultItem(HolderLookup.Provider provider) {
        return this.output().orElse(ItemStack.EMPTY).copy();
    }

    @Override
    public ItemStack getToastSymbol() {
        return new ItemStack(ModuleCore.DISSOLUTION_CHAMBER.getBlock());
    }

    @Override
    public RecipeSerializer getSerializer() {
        return ModuleCore.DISSOLUTION_SERIALIZER.get();
    }

    @Override
    public RecipeType getType() {
        return ModuleCore.DISSOLUTION_TYPE.get();
    }

    public Optional<ItemStack> output() { return outputTemplate.map(ItemStackTemplate::create); }

    public Optional<FluidStack> outputFluid() { return outputFluidTemplate.map(FluidStackTemplate::create); }

    private DissolutionChamberRecipe(List<Ingredient> input, SizedFluidIngredient inputFluid, int processingTime, Optional<ItemStackTemplate> output, Optional<FluidStackTemplate> outputFluid, boolean templates) {
        this.input = input;
        this.inputFluid = inputFluid;
        this.processingTime = processingTime;
        this.outputTemplate = output;
        this.outputFluidTemplate = outputFluid;
        }
}
