
/* This example demonstrates using the raw WebSocket API to connect
to the littleBits Cloud Stream API. You need to supply two variables
for this example to work: Your Access Token and Device ID. */

var access_token = 'ENTER_YOUR_ACCESS_TOKEN_HERE'
var device_id = 'ENTER_YOUR_DEVICE_ID_HERE'
var uri = 'wss://api-stream.littlebitscloud.cc/primus/?access_token=' + access_token


/* Instantiate a connection to the Stream API. */

var conn = new WebSocket(uri)

conn.onerror = Logger('connection-error:')
conn.onclose = Logger('connection-closed:')
conn.onmessage = Logger('data-received:')
conn.onopen = Main(conn)



/* Library */

function Main (conn) {
  return function (event) {
    console.log('connection-opened:', event)
    conn.send(JSON.stringify({
      name: 'subscribe',
      args: {
        device_id: device_id
      }
    }))
  }
}

function Logger (namespace) {
  return function () {
    console.log.apply(
      console,
      [namespace].concat(Array.prototype.slice.apply(arguments))
    )
  }
}
