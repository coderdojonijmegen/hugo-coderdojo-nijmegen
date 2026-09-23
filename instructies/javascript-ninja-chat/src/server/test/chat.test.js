const { test } = require('node:test')
const assert = require('node:assert/strict')
const { spawn } = require('node:child_process')
const net = require('node:net')
const path = require('node:path')
const { io } = require('socket.io-client')

function nextEvent(socket, event, matches = () => true) {
  return new Promise((resolve, reject) => {
    const timeout = setTimeout(() => {
      socket.off(event, onEvent)
      reject(new Error(`Timed out waiting for ${event}`))
    }, 5000)
    function onEvent(value) {
      if (!matches(value)) return
      clearTimeout(timeout)
      socket.off(event, onEvent)
      resolve(value)
    }
    socket.on(event, onEvent)
  })
}

async function unusedPort() {
  const server = net.createServer()
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve))
  const port = server.address().port
  await new Promise(resolve => server.close(resolve))
  return port
}

test('serves the chat and exchanges messages between channels', async t => {
  const port = await unusedPort()
  const server = spawn(process.execPath, ['build/app.js'], {
    cwd: path.join(__dirname, '..'),
    env: { ...process.env, PORT: String(port) },
    stdio: ['ignore', 'pipe', 'pipe']
  })
  t.after(() => server.kill())
  await new Promise((resolve, reject) => {
    server.once('error', reject)
    server.once('exit', code => reject(new Error(`Server exited: ${code}`)))
    server.stdout.once('data', resolve)
  })

  const response = await fetch(`http://127.0.0.1:${port}/`)
  assert.equal(response.status, 200)
  assert.match(await response.text(), /socket\.io\/4\.8\.3/)

  const first = io(`http://127.0.0.1:${port}`, { forceNew: true })
  const second = io(`http://127.0.0.1:${port}`, { forceNew: true })
  t.after(() => { first.disconnect(); second.disconnect() })
  await Promise.all([nextEvent(first, 'connect'), nextEvent(second, 'connect')])

  const named = nextEvent(first, 'krijgNaam', name => name === 'Ninja')
  first.emit('zetNaam', 'Ninja')
  assert.equal(await named, 'Ninja')

  const broadcast = nextEvent(second, 'krijgBericht', message => message.tekst === 'Hallo!')
  first.emit('maakBericht', 'Hallo!')
  assert.equal((await broadcast).gebruiker, 'Ninja')

  const moved = nextEvent(second, 'krijgKanaal', id => id === 2)
  second.emit('zetKanaal', 2)
  assert.equal(await moved, 2)

  const otherChannel = nextEvent(second, 'krijgBericht', message => message.tekst === 'Kanaal twee')
  second.emit('maakBericht', 'Kanaal twee')
  assert.equal((await otherChannel).kanaal, 2)
})
