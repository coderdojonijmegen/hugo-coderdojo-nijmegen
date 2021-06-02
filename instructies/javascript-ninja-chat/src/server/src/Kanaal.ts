import { Bericht } from "./Bericht";
import { Connectie } from "./Connectie";

export class Kanaal {
    public geschiedenis: Bericht[] = []
    public connecties: Connectie[] = []
    public ninja_master: Connectie|null = null

    constructor(
        public id: number
    ) {}

    public nieuweConnectie(conn: Connectie) {
        this.connecties.push(conn)
        this.stuurDeelnemers()
    }

    public spoelConnecties() {
        const filter_connecties = this.connecties.filter(
            conn => (conn.kanaal_id === this.id)
        )
        this.connecties = filter_connecties
        this.stuurDeelnemers()
    }
    
    public omroep(bericht: Bericht) {
        if (this.ninja_master) {
            this.ninja_master.stuurBericht(bericht)
        }
        for (let conn of this.connecties) {
            conn.stuurBericht(bericht)
        }
        this.geschiedenis.push(bericht)
    }

    public stuurDeelnemers() {
        for (let conn of this.connecties) {
            conn.stuurDeelnemers()
        }
    }
}
