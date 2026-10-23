package com.buuz135.industrial.compat;
import net.minecraft.resources.Identifier;
import net.neoforged.neoforge.client.extensions.common.IClientFluidTypeExtensions;
/** Keep client model classes out of dedicated-server class initialization. */
public final class MachineFluidRendering {
    public static IClientFluidTypeExtensions create(Identifier still, Identifier flowing) {
        return net.neoforged.fml.loading.FMLEnvironment.getDist().isClient() ? Client.create(still, flowing, false) : null;
    }
    public static IClientFluidTypeExtensions ore(Identifier still, Identifier flowing) {
        return net.neoforged.fml.loading.FMLEnvironment.getDist().isClient() ? Client.create(still, flowing, true) : null;
    }
    private static final class Client {
        static IClientFluidTypeExtensions create(Identifier still, Identifier flowing, boolean ore) {
            return ore ? new com.buuz135.industrial.fluid.OreTitaniumFluidType.Client(still, flowing)
                    : new com.hrznstudio.titanium.fluid.ClientFluidTypeExtensions(still, flowing);
        }
    }
}
