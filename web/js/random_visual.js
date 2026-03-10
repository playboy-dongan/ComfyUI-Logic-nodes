import { app } from "../../scripts/app.js";
import { tr, replaceComboWithTranslated } from "./tr.js";

const RANDOM_MODES = ["random_int", "random_float", "random_seed", "random_bool"];

app.registerExtension({
    name: "Logic.RandomVisual",
    nodeCreated(node) {
        if (node.comfyClass !== "Logic_Random") return;

        const minWidget = node.widgets?.find(w => w.name === "min_val");
        const maxWidget = node.widgets?.find(w => w.name === "max_val");

        function updateWidgets() {
            const modeWidget = node.widgets?.find(w => w.name === "mode");
            if (!modeWidget || !minWidget || !maxWidget) return;
            const mode = modeWidget.value;
            const needRange = mode === "random_int" || mode === "random_float";
            minWidget.type = needRange ? "number" : "hidden";
            maxWidget.type = needRange ? "number" : "hidden";
            node.setSize(node.computeSize());
            node.setDirtyCanvas(true, true);
        }

        replaceComboWithTranslated(node, "mode", RANDOM_MODES, "Logic.Random.", updateWidgets);
        updateWidgets();

        const origExec = node.onExecuted;
        node.onExecuted = function (data) {
            if (origExec) origExec.call(this, data);
            const value = data?.value?.[0];
            if (value != null) {
                node.title = tr("Logic.Random.title").replace("{value}", value);
            }
            node.setDirtyCanvas(true, true);
        };
    },
});
