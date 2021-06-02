import * as Http from 'http'
import Koa = require('koa')
import koa_static = require('koa-static')
import { Server, Socket } from 'socket.io'

import { Kanaal } from "./Kanaal";
import { Connectie } from "./Connectie";

const defaultPort: Number = 3000;

interface App {
    koa: Koa
    server: Http.Server|null
    io : Server|null
    port: Number
    kanalen: Kanaal[]
}

function maak_kanalen(aantal: number): Kanaal[] {
    const kanalen: Kanaal[] = []
    for (let i = 0; i < aantal; ++i) {
        kanalen[i] = new Kanaal(i+1)
    }
    return kanalen
}


var app: App = {
    koa: new Koa(),
    server: null,
    io: null,
    port: Number(process.env.PORT) || defaultPort,
    kanalen: maak_kanalen(15)
}

function vind_kanaal(id: number): Kanaal|null {
    if (0 < id && id <= app.kanalen.length) {
        return app.kanalen[id - 1]
    }
    else {
        return null
    }
}

function disconnect(connectie: Connectie) {
    if (connectie.is_master) {
        connectie.stopMaster()
    }
    else {
        const kanaal = vind_kanaal(connectie.kanaal_id)
        connectie.zetKanaal(-1)
        if (kanaal) {
            kanaal.spoelConnecties()
        }
    }
}

function connect(client: Socket) {
    const connectie = new Connectie(vind_kanaal, 1, client)
    connectie.initialize()
    app.kanalen[0].nieuweConnectie(connectie)
    client.on('disconnect', () => disconnect(connectie))
}

function initialize() {
    app.koa.use(koa_static(__dirname + '/../public'))
    app.server = Http.createServer(app.koa.callback())
    app.io = new Server(app.server, {
        cors: {
            origin: "*",
            methods: ["GET"]
        }
    })
    app.io.on('connection', connect)
    app.server.listen(app.port)
    console.log(`Listening on http://localhost:${app.port}/`)
}

initialize()
