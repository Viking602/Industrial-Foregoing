package com.buuz135.industrial.compat;

import net.neoforged.neoforge.energy.IEnergyStorage;
import net.neoforged.neoforge.transfer.energy.EnergyHandler;
import net.neoforged.neoforge.transfer.transaction.Transaction;

public final class MachineEnergy {
    private MachineEnergy() {}
    public static int extractEnergy(EnergyHandler energy, int amount, boolean simulate) {
        try (var transaction = Transaction.openRoot()) {
            int extracted = energy.extract(amount, transaction);
            if (!simulate) transaction.commit();
            return extracted;
        }
    }
    public static int receiveEnergy(EnergyHandler energy, int amount, boolean simulate) {
        try (var transaction = Transaction.openRoot()) {
            int inserted = energy.insert(amount, transaction);
            if (!simulate) transaction.commit();
            return inserted;
        }
    }
    public static int extractEnergy(IEnergyStorage energy, int amount, boolean simulate) { return energy.extractEnergy(amount, simulate); }
    public static int receiveEnergy(IEnergyStorage energy, int amount, boolean simulate) { return energy.receiveEnergy(amount, simulate); }
}
