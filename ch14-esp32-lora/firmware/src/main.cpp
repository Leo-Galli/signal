#include <Arduino.h>
#include <SPI.h>
#include <RadioLib.h>
#include <string.h>

#include "airtime_est.h"
#include "duty_cycle.h"
#include "packet.h"
#include "pins.h"

#ifndef NODE_ROLE
#define NODE_ROLE 1
#endif
#ifndef LORA_FREQ_MHZ
#define LORA_FREQ_MHZ 433.05
#endif
#ifndef LORA_SF
#define LORA_SF 7
#endif
#ifndef LORA_BW_KHZ
#define LORA_BW_KHZ 125.0
#endif
#ifndef LORA_CR
#define LORA_CR 5
#endif
#ifndef LORA_TX_DBM
#define LORA_TX_DBM 2
#endif
#ifndef DUTY_CYCLE_PERCENT
#define DUTY_CYCLE_PERCENT 10
#endif
#ifndef PING_INTERVAL_MS
#define PING_INTERVAL_MS 5000
#endif

// Coding rate for RadioLib setCodingRate is 5..8 meaning 4/5..4/8.
// airtime_est uses Semtech CR 1..4 where rate = 4/(4+CR).
static const uint8_t kAirtimeCr = (LORA_CR >= 5) ? static_cast<uint8_t>(LORA_CR - 4) : 1;

#if defined(MODULE_SX1262)
SX1262 radio = new Module(CS_PIN, DIO0_PIN, RST_PIN, DIO1_PIN);
#elif defined(MODULE_E22)
SX1268 radio = new Module(CS_PIN, DIO0_PIN, RST_PIN, DIO1_PIN);
#else
SX1276 radio = new Module(CS_PIN, DIO0_PIN, RST_PIN, DIO1_PIN);
#endif

static DutyCycleGate g_gate;
static uint16_t g_seq = 1;
static uint32_t g_last_ping_ms = 0;
static uint8_t g_rx_buf[PACKET_MAX_BYTES];
static volatile bool g_rx_flag = false;

static const char *module_name(void) {
#if defined(MODULE_SX1262)
  return "SX1262";
#elif defined(MODULE_E22)
  return "E22/SX1268";
#else
  return "SX1276";
#endif
}

#if defined(ESP8266) || defined(ESP32)
ICACHE_RAM_ATTR
#endif
static void on_rx_flag(void) {
  g_rx_flag = true;
}

static int apply_modem(void) {
  int16_t st = radio.setFrequency(static_cast<float>(LORA_FREQ_MHZ));
  if (st != RADIOLIB_ERR_NONE) {
    return st;
  }
  st = radio.setSpreadingFactor(LORA_SF);
  if (st != RADIOLIB_ERR_NONE) {
    return st;
  }
  st = radio.setBandwidth(static_cast<float>(LORA_BW_KHZ));
  if (st != RADIOLIB_ERR_NONE) {
    return st;
  }
  st = radio.setCodingRate(LORA_CR);
  if (st != RADIOLIB_ERR_NONE) {
    return st;
  }
  st = radio.setOutputPower(LORA_TX_DBM);
  if (st != RADIOLIB_ERR_NONE) {
    return st;
  }
  return RADIOLIB_ERR_NONE;
}

static void print_banner(void) {
  Serial.println();
  Serial.println(F("# Signal ch14-esp32-lora"));
  Serial.println(F("# P2P ping at FAIL-SAFE low power + software duty-cycle cap"));
  Serial.println(F("# Not legal advice. Match LORA_TX_DBM and DUTY_CYCLE_PERCENT to Ch3 worksheet."));
  Serial.print(F("# module="));
  Serial.print(module_name());
  Serial.print(F(" role="));
  Serial.println(NODE_ROLE == 1 ? F("A-ping") : F("B-pong"));
  Serial.print(F("# freq_MHz="));
  Serial.print(static_cast<float>(LORA_FREQ_MHZ));
  Serial.print(F(" SF="));
  Serial.print(LORA_SF);
  Serial.print(F(" BW_kHz="));
  Serial.print(static_cast<float>(LORA_BW_KHZ));
  Serial.print(F(" CR="));
  Serial.print(LORA_CR);
  Serial.print(F(" tx_dBm="));
  Serial.println(LORA_TX_DBM);
  Serial.print(F("# duty_cycle_percent="));
  Serial.print(static_cast<float>(DUTY_CYCLE_PERCENT));
  Serial.print(F(" pins CS="));
  Serial.print(CS_PIN);
  Serial.print(F(" DIO0="));
  Serial.print(DIO0_PIN);
  Serial.print(F(" RST="));
  Serial.print(RST_PIN);
  Serial.print(F(" DIO1="));
  Serial.println(DIO1_PIN);
}

static bool send_payload(const BeaconPayload *payload, const char *tag) {
  uint8_t buf[PACKET_MAX_BYTES];
  const size_t n = packet_encode(payload, buf, sizeof(buf));
  if (n == 0) {
    Serial.println(F("# encode failed"));
    return false;
  }

  const uint32_t air_ms = airtime_est_ms(
    LORA_SF,
    static_cast<float>(LORA_BW_KHZ) * 1000.0f,
    static_cast<uint16_t>(n),
    kAirtimeCr,
    8
  );
  const uint32_t now = millis();
  if (!duty_cycle_allow(&g_gate, now, air_ms)) {
    Serial.print(F("# TX blocked by duty-cycle gate; remaining_ms="));
    Serial.println(duty_cycle_remaining_ms(&g_gate, now));
    return false;
  }

  const int16_t st = radio.transmit(buf, n);
  if (st != RADIOLIB_ERR_NONE) {
    Serial.print(F("# transmit error "));
    Serial.println(st);
    radio.startReceive();
    return false;
  }
  duty_cycle_record(&g_gate, now, air_ms);
  Serial.print(F("# "));
  Serial.print(tag);
  Serial.print(F(" seq="));
  Serial.print(payload->seq);
  Serial.print(F(" bytes="));
  Serial.print(static_cast<unsigned>(n));
  Serial.print(F(" air_ms="));
  Serial.println(air_ms);
  radio.startReceive();
  return true;
}

static void handle_rx(void) {
  if (!g_rx_flag) {
    return;
  }
  g_rx_flag = false;

  const size_t cap = sizeof(g_rx_buf);
  const int16_t st = radio.readData(g_rx_buf, cap);
  if (st != RADIOLIB_ERR_NONE) {
    Serial.print(F("# readData error "));
    Serial.println(st);
    radio.startReceive();
    return;
  }

  const size_t n = radio.getPacketLength();
  BeaconPayload got;
  if (!packet_decode(g_rx_buf, n, &got)) {
    Serial.println(F("# RX bad magic/CRC"));
    radio.startReceive();
    return;
  }

  const float rssi = radio.getRSSI();
  const float snr = radio.getSNR();
  Serial.print(F("RX name="));
  Serial.print(got.name);
  Serial.print(F(" seq="));
  Serial.print(got.seq);
  Serial.print(F(" lat="));
  Serial.print(got.lat, 5);
  Serial.print(F(" lon="));
  Serial.print(got.lon, 5);
  Serial.print(F(" rssi="));
  Serial.print(rssi, 1);
  Serial.print(F(" snr="));
  Serial.println(snr, 1);

#if NODE_ROLE == 2
  BeaconPayload reply;
  memset(&reply, 0, sizeof(reply));
  reply.seq = got.seq;
  strncpy(reply.name, "pong", PACKET_NAME_MAX);
  reply.name[PACKET_NAME_MAX] = '\0';
  reply.lat = got.lat;
  reply.lon = got.lon;
  send_payload(&reply, "pong");
#else
  radio.startReceive();
#endif
}

static void maybe_ping(void) {
#if NODE_ROLE != 1
  return;
#else
  const uint32_t now = millis();
  if (now - g_last_ping_ms < static_cast<uint32_t>(PING_INTERVAL_MS)) {
    return;
  }
  g_last_ping_ms = now;

  BeaconPayload ping;
  memset(&ping, 0, sizeof(ping));
  ping.seq = g_seq++;
  strncpy(ping.name, "ping", PACKET_NAME_MAX);
  // Teaching placeholders only -- not a real GPS fix. Replace in your notes if needed.
  ping.lat = 0.0f;
  ping.lon = 0.0f;
  send_payload(&ping, "ping");
#endif
}

void setup() {
  Serial.begin(115200);
  delay(200);
  print_banner();

  SPI.begin(LORA_SCK, LORA_MISO, LORA_MOSI, CS_PIN);

  int16_t st = radio.begin(static_cast<float>(LORA_FREQ_MHZ));
  if (st != RADIOLIB_ERR_NONE) {
    Serial.print(F("# radio.begin failed: "));
    Serial.println(st);
    Serial.println(F("# Check wiring / MODULE_* env. Firmware built; RF path not ready."));
  } else {
    st = apply_modem();
    if (st != RADIOLIB_ERR_NONE) {
      Serial.print(F("# modem config failed: "));
      Serial.println(st);
    } else {
      radio.setPacketReceivedAction(on_rx_flag);
      st = radio.startReceive();
      if (st != RADIOLIB_ERR_NONE) {
        Serial.print(F("# startReceive failed: "));
        Serial.println(st);
      } else {
        Serial.println(F("# radio ready"));
      }
    }
  }

  duty_cycle_init(&g_gate, static_cast<float>(DUTY_CYCLE_PERCENT), 3600000UL);
  Serial.print(F("# duty budget_ms/hour="));
  Serial.println(duty_cycle_budget_ms(&g_gate));
  Serial.println(F("# Ready."));
}

void loop() {
  handle_rx();
  maybe_ping();
}
