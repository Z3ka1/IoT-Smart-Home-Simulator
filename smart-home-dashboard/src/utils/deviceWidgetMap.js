import GenericDeviceWidget from "@/components/devices/GenericDeviceWidget.vue";
import LightWidget from "@/components/devices/LightWidget.vue";
import ThermometerWidget from "@/components/devices/ThermometerWidget.vue";
import SimpleLEDWidget from "@/components/devices/SimpleLEDWidget.vue";
import AlarmSensorWidget from "@/components/devices/AlarmSensorWidget.vue";
import RGBStripWidget from "@/components/devices/RGBStripWidget.vue";
import LCDDisplayWidget from "@/components/devices/LCDDisplayWidget.vue";

export const deviceWidgetMap = {
    light: LightWidget,
    thermometer: ThermometerWidget,
    simpleled: SimpleLEDWidget,
    alarmsensor: AlarmSensorWidget,
    rgbstrip: RGBStripWidget,
    lcddisplay: LCDDisplayWidget,
}