import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "Logic.RandomVisual",
    nodeCreated(node) {
        if (node.comfyClass !== "Logic_Random") return;

        const modeWidget = node.widgets?.find(w => w.name === "模式");
        const minWidget = node.widgets?.find(w => w.name === "最小值");
        const maxWidget = node.widgets?.find(w => w.name === "最大值");

        function updateWidgets() {
            if (!modeWidget || !minWidget || !maxWidget) return;
            const mode = modeWidget.value;
            const needRange = mode === "随机整数" || mode === "随机浮点数";
            minWidget.type = needRange ? "number" : "hidden";
            maxWidget.type = needRange ? "number" : "hidden";
            node.setSize(node.computeSize());
            node.setDirtyCanvas(true, true);
        }

        if (modeWidget) {
            const origCb = modeWidget.callback;
            modeWidget.callback = function (v) {
                updateWidgets();
                origCb?.call(this, v);
            };
            updateWidgets();
        }

        const origExec = node.onExecuted;
        node.onExecuted = function (data) {
            if (origExec) origExec.call(this, data);
            const value = data?.value?.[0];
            if (value != null) {
                node.title = `🎲 随机工具 → ${value}`;
            }
            node.setDirtyCanvas(true, true);
        };
    },
});
