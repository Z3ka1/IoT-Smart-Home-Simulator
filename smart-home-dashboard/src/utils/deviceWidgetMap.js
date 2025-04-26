import GenericDeviceWidget from "@/components/devices/GenericDeviceWidget.vue";
import LightWidget from "@/components/devices/LightWidget.vue";
import ThermometerWidget from "@/components/devices/ThermometerWidget.vue";

export const deviceWidgetMap = {
    light: LightWidget,
    thermometer: ThermometerWidget,
    // Add more mappings as needed
}