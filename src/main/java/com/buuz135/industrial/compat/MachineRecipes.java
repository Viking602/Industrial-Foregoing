package com.buuz135.industrial.compat;

import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.crafting.*;
import net.minecraft.world.level.Level;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import java.util.List;

/** Uses the server recipe manager or NeoForge's synchronized full recipes on the client. */
@EventBusSubscriber(modid = "industrialforegoing")
public final class MachineRecipes {
    private static volatile RecipeMap clientRecipes = RecipeMap.EMPTY;
    @SubscribeEvent public static void sync(net.neoforged.neoforge.event.OnDatapackSyncEvent event) {
        event.sendRecipes(BuiltInRegistries.RECIPE_TYPE.entrySet().stream()
                .filter(entry -> java.util.Set.of("industrialforegoing", "ifeu").contains(entry.getKey().identifier().getNamespace()))
                .map(java.util.Map.Entry::getValue).toList());
        event.sendRecipes(RecipeType.CRAFTING, RecipeType.SMELTING);
    }
    @SuppressWarnings("unchecked")
    public static <T extends Recipe<?>> List<RecipeHolder<T>> getHolders(Level level, RecipeType<T> type) {
        var recipes = level.recipeAccess() instanceof RecipeManager manager ? manager.getRecipes() : clientRecipes.values();
        return recipes.stream().filter(holder -> holder.value().getType() == type).map(holder -> (RecipeHolder<T>)holder).toList();
    }
    public static <T extends Recipe<?>> List<T> getRecipes(Level level, RecipeType<T> type) { return getHolders(level,type).stream().map(RecipeHolder::value).toList(); }
    public static List<SmeltingRecipe> getCookingRecipes(Level level) { return getRecipes(level, RecipeType.SMELTING); }
    public static SmeltingRecipe getSmelingRecipeFor(Level level, ItemStack stack) { return getCookingRecipes(level).stream().filter(recipe -> recipe.input().test(stack)).findFirst().orElse(null); }
    @EventBusSubscriber(modid = "industrialforegoing", value = net.neoforged.api.distmarker.Dist.CLIENT)
    public static final class ClientEvents {
        @SubscribeEvent(priority = net.neoforged.bus.api.EventPriority.HIGHEST)
        public static void received(net.neoforged.neoforge.client.event.RecipesReceivedEvent event) { clientRecipes = event.getRecipeMap(); }
        @SubscribeEvent public static void disconnected(net.neoforged.neoforge.client.event.ClientPlayerNetworkEvent.LoggingOut event) { clientRecipes = RecipeMap.EMPTY; }
    }
}
