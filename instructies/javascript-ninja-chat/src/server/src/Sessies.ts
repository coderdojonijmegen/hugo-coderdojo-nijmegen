import { randomUUID } from 'crypto'

// Een ninja die een dag niet is teruggekomen, begint aan een nieuwe dojo.
const SESSIE_DUUR = 24 * 60 * 60 * 1000

export interface Sessie {
    id: string
    naam: string
    laatstGezien: number
}

export class Sessies {
    private sessies = new Map<string, Sessie>()

    public verbind(id: unknown): Sessie {
        const nu = Date.now()
        for (const [sessieId, sessie] of this.sessies) {
            if (nu - sessie.laatstGezien >= SESSIE_DUUR) {
                this.sessies.delete(sessieId)
            }
        }

        const bestaand = typeof id === 'string' ? this.sessies.get(id) : undefined
        if (bestaand) {
            bestaand.laatstGezien = nu
            return bestaand
        }

        const nieuw: Sessie = {
            id: randomUUID(),
            naam: `anon${Math.floor(Math.random() * 1000)}`,
            laatstGezien: nu
        }
        this.sessies.set(nieuw.id, nieuw)
        return nieuw
    }

    public zetNaam(sessie: Sessie, naam: string): void {
        sessie.naam = naam
        sessie.laatstGezien = Date.now()
    }
}
