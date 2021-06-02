export class Gebruiker {
    naam: string
    
    constructor() {
        this.naam = this.anon()
    }

    private anon() {
        const random_getal = Math.floor(Math.random() * 1000);
        return `anon${random_getal}`
    }
}
