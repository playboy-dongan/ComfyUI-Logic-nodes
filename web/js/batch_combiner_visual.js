import { app } from "../../scripts/app.js";

const MIN_INPUTS = 2;
const MAX_INPUTS = 10;

app.registerExtension({
    name: "Logic.BatchCombinerVisual",
    nodeCreated(node) {
        if (node.comfyClass !== "Logic_BatchCombiner") return;

        const optionalShape = node.inputs[0]?.shape;

        function adjustInputs() {
            let lastConnected = -1;
            for (let i = 0; i < node.inputs.length; i++) {
                if (node.inputs[i].link != null) lastConnected = i;
            }

            const target = Math.min(Math.max(MIN_INPUTS, lastConnected + 2), MAX_INPUTS);

            while (node.inputs.length > target) {
                const last = node.inputs[node.inputs.length - 1];
                if (last.link != null) break;
                node.removeInput(node.inputs.length - 1);
            }

            while (node.inputs.length < target) {
                const idx = node.inputs.length + 1;
                node.addInput(`任意${idx}`, "*");
                if (optionalShape != null) {
                    node.inputs[node.inputs.length - 1].shape = optionalShape;
                }
            }

            updateTitle();
        }

        function countConnected() {
            let n = 0;
            for (let i = 0; i < node.inputs.length; i++) {
                if (node.inputs[i].link != null) n++;
            }
            return n;
        }

        function updateTitle() {
            const n = countConnected();
            if (n > 0) {
                node.title = `📦 组合任意批次 (${n}个输入)`;
            } else {
                node.title = "📦 组合任意批次";
            }
            node.setSize(node.computeSize());
            node.setDirtyCanvas(true, true);
        }

        while (node.inputs.length > MIN_INPUTS) {
            node.removeInput(node.inputs.length - 1);
        }

        const origConn = node.onConnectionsChange;
        node.onConnectionsChange = function (...args) {
            origConn?.call(this, ...args);
            adjustInputs();
        };

        const origConf = node.onConfigure;
        node.onConfigure = function (info) {
            origConf?.call(this, info);
            setTimeout(() => adjustInputs(), 100);
        };

        const origExec = node.onExecuted;
        node.onExecuted = function (data) {
            origExec?.call(this, data);
            const detail = data?.detail?.[0];
            const typeName = data?.type_name?.[0];
            if (typeName && detail) {
                node.title = `📦 组合任意批次 → ${typeName} ${detail}`;
            }
            node.setDirtyCanvas(true, true);
        };

        updateTitle();
    },
});
