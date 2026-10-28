#include <Arduino.h>
#include <SPI.h>
#include <RadioLib.h>
#include <string.h>

#include "airtime_est.h"
#include "dry_run.h"
#include "duty_cycle.h"
#include "gps_nmea.h"
#include "morse_payload.h"
#include "morse_tx.h"
#include "packet.h"
#include "pins.h"

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
#ifndef BEACON_INTERVAL_MS
#define BEACON_INTERVAL_MS 30000
#endif
#ifndef MORSE_WPM
#define MORSE_WPM 15
#endif
#ifndef DRY_RUN
#define DRY_RUN 1
#endif
#ifndef BEACON_NAME
#define BEACON_NAME "MAKER"
#endif

static const uint8_t kAirtimeCr = (LORA_CR >= 5) ? static_cast<uint8_t>(LORA_CR - 4) : 1;

#if defined(MODULE_SX1262)
SX1262 radio = new Module(CS_PIN, DIO0_PIN, RST_PIN, DIO1_PIN);
#elif defined(MODULE_E22)
SX1268 radio = new Module(CS_PIN, DIO0_PIN, RST_PIN, DIO1_PIN);
#else
SX1276 radio = new Module(CS_PIN, DIO0_PIN, RST_PIN, DIO1_PIN);
#endif

static DutyCycleGate g_gate;
static DryRunState g_dry;
static GpsFix g_gps;
static MorseTx g_morse;
static uint16_t g_seq = 1;
static uint32_t g_last_beacon_ms = 0;
static bool g_radio_ok = false;
static bool g_sos_armed = false;
static char g_morse_buf[MORSE_PAYLOAD_MAX + 1];
static char g_gps_line[120];
static size_t g_gps_line_len = 0;

static const char *module_name(void) {
#if defined(MODULE_SX1262)
  return "SX1262";
#elif defined(MODULE_E22)
  return "E22/SX1268";
#else
  return "SX1276";
#endif
}

static void print_banner(void) {
  Serial.println();
  Serial.println(F("# Signal ch17-field-beacon"));
  Serial.println(F("# Capstone: GPS + LoRa name/lat/lon + Morse sidetone fallback"));
  Serial.println(F("# Not legal advice. Match power/duty to Ch3 worksheet. No false distress."));
  Serial.print(F("# module="));
  Serial.print(module_name());
  Serial.print(F(" dry_run="));
  Serial.println(dry_run_active(&g_dry) ? F("ON") : F("OFF"));
  Serial.print(F("# name="));
  Serial.println(BEACON_NAME);
  Serial.print(F("# freq_MHz="));
  Serial.print(static_cast<float>(LORA_FREQ_MHZ));
  Serial.print(F(" SF="));
  Serial.print(LORA_SF);
  Serial.print(F(" tx_dBm="));
  Serial.print(LORA_TX_DBM);
  Serial.print(F(" duty%="));
  Serial.println(static_cast<float>(DUTY_CYCLE_PERCENT));
  Serial.println(F("# buttons: SOS=arm  SEND=LoRa  MORSE=sidetone  DRY=force dry-run"));
}

static void fill_payload(BeaconPayload *out) {
  memset(out, 0, sizeof(*out));
  out->seq = g_seq;
  strncpy(out->name, BEACON_NAME, PACKET_NAME_MAX);
  out->name[PACKET_NAME_MAX] = '\0';
  if (g_gps.fix_valid) {
    out->lat = g_gps.lat;
    out->lon = g_gps.lon;
  } else {
    // Teaching placeholders when GPS has no fix -- not a real location.
    out->lat = 0.0f;
    out->lon = 0.0f;
  }
}

static bool attempt_lora_send(const BeaconPayload *payload) {
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

  if (dry_run_active(&g_dry)) {
    dry_run_note_blocked(&g_dry);
    dry_run_note_simulated(&g_dry);
    Serial.print(F("# DRY-RUN: would TX seq="));
    Serial.print(payload->seq);
    Serial.print(F(" bytes="));
    Serial.print(static_cast<unsigned>(n));
    Serial.print(F(" air_ms="));
    Serial.print(air_ms);
    Serial.print(F(" name="));
    Serial.print(payload->name);
    Serial.print(F(" lat="));
    Serial.print(payload->lat, 5);
    Serial.print(F(" lon="));
    Serial.println(payload->lon, 5);
    return true;
  }

  if (!g_radio_ok) {
    Serial.println(F("# radio not ready; TX skipped"));
    return false;
  }
  if (!duty_cycle_allow(&g_gate, now, air_ms)) {
    Serial.print(F("# TX blocked by duty-cycle gate; remaining_ms="));
    Serial.println(duty_cycle_remaining_ms(&g_gate, now));
    return false;
  }

  const int16_t st = radio.transmit(buf, n);
  if (st != RADIOLIB_ERR_NONE) {
    Serial.print(F("# transmit error "));
    Serial.println(st);
    return false;
  }
  duty_cycle_record(&g_gate, now, air_ms);
  Serial.print(F("# TX seq="));
  Serial.print(payload->seq);
  Serial.print(F(" bytes="));
  Serial.print(static_cast<unsigned>(n));
  Serial.print(F(" air_ms="));
  Serial.println(air_ms);
  return true;
}

static void play_morse_fallback(const BeaconPayload *payload) {
  if (morse_tx_busy(&g_morse)) {
    Serial.println(F("# Morse busy"));
    return;
  }
  const size_t n = morse_payload_build(payload, g_morse_buf, sizeof(g_morse_buf));
  if (n == 0) {
    Serial.println(F("# Morse payload build failed"));
    return;
  }
  Serial.print(F("# Morse sidetone: "));
  Serial.println(g_morse_buf);
  Serial.println(F("# Sidetone only unless you enable a separate legal RF path per Ch3."));
  morse_tx_start(&g_morse, g_morse_buf);
}

static void poll_gps_uart(void) {
  while (Serial2.available() > 0) {
    const char c = static_cast<char>(Serial2.read());
    if (c == '\r') {
      continue;
    }
    if (c == '\n') {
      g_gps_line[g_gps_line_len] = '\0';
      if (g_gps_line_len > 0) {
        gps_nmea_feed_line(&g_gps, g_gps_line);
      }
      g_gps_line_len = 0;
      continue;
    }
    if (g_gps_line_len + 1 < sizeof(g_gps_line)) {
      g_gps_line[g_gps_line_len++] = c;
    } else {
      g_gps_line_len = 0;
    }
  }
}

static bool button_pressed(uint8_t pin) {
  // Active-low with INPUT_PULLUP.
  static uint32_t last_ms[4] = {0, 0, 0, 0};
  static uint8_t pins[4] = {BTN_SOS_PIN, BTN_SEND_PIN, BTN_MORSE_PIN, BTN_DRY_PIN};
  int idx = 0;
  for (; idx < 4; idx++) {
    if (pins[idx] == pin) {
      break;
    }
  }
  if (digitalRead(pin) != LOW) {
    return false;
  }
  const uint32_t now = millis();
  if (now - last_ms[idx] < 250UL) {
    return false;
  }
  last_ms[idx] = now;
  // Wait for release edge roughly.
  delay(20);
  return digitalRead(pin) == LOW;
}

static void handle_buttons(void) {
  if (button_pressed(BTN_SOS_PIN)) {
    g_sos_armed = !g_sos_armed;
    Serial.print(F("# SOS armed="));
    Serial.println(g_sos_armed ? F("YES") : F("NO"));
    Serial.println(F("# Arming is local UI only. Do not send false distress on air."));
  }
  if (button_pressed(BTN_SEND_PIN)) {
    if (!g_sos_armed) {
      Serial.println(F("# SEND ignored: arm SOS button first (teaching interlock)"));
      return;
    }
    BeaconPayload p;
    fill_payload(&p);
    if (attempt_lora_send(&p)) {
      g_seq++;
    }
  }
  if (button_pressed(BTN_MORSE_PIN)) {
    BeaconPayload p;
    fill_payload(&p);
    play_morse_fallback(&p);
  }
  if (button_pressed(BTN_DRY_PIN)) {
    dry_run_set_runtime(&g_dry, true);
    Serial.println(F("# Dry-run forced ON (compile DRY_RUN=1 cannot be cleared at runtime)"));
  }
}

static void maybe_auto_beacon(void) {
  if (!g_sos_armed) {
    return;
  }
  const uint32_t now = millis();
  if (now - g_last_beacon_ms < static_cast<uint32_t>(BEACON_INTERVAL_MS)) {
    return;
  }
  g_last_beacon_ms = now;
  BeaconPayload p;
  fill_payload(&p);
  if (attempt_lora_send(&p)) {
    g_seq++;
  }
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

void setup() {
  Serial.begin(115200);
  delay(200);

  dry_run_init(&g_dry, DRY_RUN != 0);
  gps_fix_init(&g_gps);
  morse_tx_init(&g_morse, TONE_PIN, MORSE_WPM);
  duty_cycle_init(&g_gate, static_cast<float>(DUTY_CYCLE_PERCENT), 3600000UL);

  pinMode(BTN_SOS_PIN, INPUT_PULLUP);
  pinMode(BTN_SEND_PIN, INPUT_PULLUP);
  pinMode(BTN_MORSE_PIN, INPUT_PULLUP);
  pinMode(BTN_DRY_PIN, INPUT_PULLUP);

  print_banner();

  Serial2.begin(9600, SERIAL_8N1, GPS_RX_PIN, GPS_TX_PIN);
  Serial.println(F("# GPS UART 9600 on Serial2"));

  SPI.begin(LORA_SCK, LORA_MISO, LORA_MOSI, CS_PIN);
  int16_t st = radio.begin(static_cast<float>(LORA_FREQ_MHZ));
  if (st != RADIOLIB_ERR_NONE) {
    Serial.print(F("# radio.begin failed: "));
    Serial.println(st);
    Serial.println(F("# Firmware built; RF path not ready. Dry-run still works."));
    g_radio_ok = false;
  } else {
    st = apply_modem();
    if (st != RADIOLIB_ERR_NONE) {
      Serial.print(F("# modem config failed: "));
      Serial.println(st);
      g_radio_ok = false;
    } else {
      g_radio_ok = true;
      Serial.println(F("# radio ready"));
    }
  }

  Serial.print(F("# duty budget_ms/hour="));
  Serial.println(duty_cycle_budget_ms(&g_gate));
  if (dry_run_active(&g_dry)) {
    Serial.println(F("# DRY-RUN ACTIVE: radio.transmit will never be called"));
  }
  Serial.println(F("# Ready."));
}

void loop() {
  poll_gps_uart();
  handle_buttons();
  maybe_auto_beacon();
  morse_tx_poll(&g_morse, millis());
}
