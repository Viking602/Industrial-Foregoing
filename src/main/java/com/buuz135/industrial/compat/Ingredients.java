package com.buuz135.industrial.compat;

import net.minecraft.core.HolderSet;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.tags.TagKey;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.crafting.Ingredient;
import net.minecraft.world.level.ItemLike;
import java.util.stream.Stream;

/** Ingredient construction shared by machine recipes and recipe viewer displays. */
public final class Ingredients {
    private Ingredients() {}
    public static Ingredient of(ItemLike... items) { return Ingredient.of(items); }
    public static Ingredient of(ItemStack... items) { return of(Stream.of(items)); }
    public static Ingredient of(Stream<ItemStack> items) {
        return net.neoforged.neoforge.common.crafting.CompoundIngredient.of(items.filter(stack -> !stack.isEmpty()).map(stack -> stack.getComponentsPatch().isEmpty()
            ? Ingredient.of(stack.getItem())
            : net.neoforged.neoforge.common.crafting.DataComponentIngredient.of(stack.getComponentsPatch(), stack.getItem())).toArray(Ingredient[]::new));
    }
    public static Ingredient of(HolderSet<Item> items) { return Ingredient.of(items); }
    public static Ingredient of(TagKey<Item> tag) { return Ingredient.of(BuiltInRegistries.ITEM.getOrThrow(tag)); }
}
