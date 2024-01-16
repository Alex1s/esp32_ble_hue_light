import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.const import CONF_ID, CONF_MODEL
from esphome.components import esp32_ble
from esphome.core import CORE
from esphome.components.esp32 import add_idf_sdkconfig_option

AUTO_LOAD = ["esp32_ble"]
CODEOWNERS = ["@jesserockz", "@clydebarrow", "@Rapsssito", "@Alex1s"]
CONFLICTS_WITH = ["esp32_ble_beacon", "esp32_ble_server"]
DEPENDENCIES = ["esp32"]

esp32_ble_hue_light_ns = cg.esphome_ns.namespace("esp32_ble_hue_light_ns")
BLEServer = esp32_ble_hue_light_ns.class_(
    "BLEServer",
    cg.Component,
    esp32_ble.GATTsEventHandler,
    cg.Parented.template(esp32_ble.ESP32BLE),
)
BLEServiceComponent = esp32_ble_hue_light_ns.class_("BLEServiceComponent")


CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(BLEServer),
        cv.GenerateID(esp32_ble.CONF_BLE_ID): cv.use_id(esp32_ble.ESP32BLE),
    }
).extend(cv.COMPONENT_SCHEMA)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])

    await cg.register_component(var, config)

    parent = await cg.get_variable(config[esp32_ble.CONF_BLE_ID])
    cg.add(parent.register_gatts_event_handler(var))
    cg.add(parent.register_ble_status_event_handler(var))
    cg.add(var.set_parent(parent))

    cg.add_define("USE_ESP32_BLE_SERVER")

    if CORE.using_esp_idf:
        add_idf_sdkconfig_option("CONFIG_BT_ENABLED", True)
