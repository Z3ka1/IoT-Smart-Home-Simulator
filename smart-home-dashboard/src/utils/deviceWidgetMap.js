import GenericDeviceWidget from "@/components/devices/GenericDeviceWidget.vue";
import LightWidget from "@/components/devices/LightWidget.vue";
import ThermometerWidget from "@/components/devices/ThermometerWidget.vue";
import SimpleLEDWidget from "@/components/devices/SimpleLEDWidget.vue";

export const deviceWidgetMap = {
    light: LightWidget,
    thermometer: ThermometerWidget,
    simpleled: SimpleLEDWidget,
    // Add more mappings as needed
}