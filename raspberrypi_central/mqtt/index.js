const mqtt = require('mqtt')
const fs = require('fs')

require('dotenv').config()

const getMqttClient = () => {
  const options = {
    username: process.env.MQTT_USERNAME,
    password: process.env.MQTT_PASSWORD,
    host: process.env.MQTT_HOST,
    port: 8883,
    protocol: 'mqtts',
  
    // @TODO see https://stackoverflow.com/questions/40018804/node-js-mqtt-client-using-tls
    // rejectUnauthorized: false,
    key: fs.readFileSync('test_client.key'),
    cert: fs.readFileSync('test_client.crt'),
    ca: [ fs.readFileSync('/home/mx/www/playing-with-arduino/raspberrypi_central/webapp/config/mosquitto/certs/ca.crt') ],
  }
  
  return mqtt.connect(options)
}

const client = getMqttClient()

client.on('connect', () => {
  client.subscribe('presence', err => {
    if (!err) {
      client.publish('presence', 'Hello mqtt')
    }
  })
})

const presenceHandler = (message) => {
  // message is Buffer
  console.log(message.toString(), 'from handler!')
}

const routes = {
  presence: presenceHandler
}

const routesNames = Object.keys(routes)

client.on('message', function (topic, message) {

  if (routesNames.includes(topic)) {
    routes[topic](message)
  }

  // client.end()
})