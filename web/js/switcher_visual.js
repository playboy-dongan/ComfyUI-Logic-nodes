import { app } from "../../scripts/app.js";
import { tr, trTypeName } from "./tr.js";

const MIN_INPUTS = 2;
const MAX_INPUTS = 10;

app.registerExtension({
    name: "Logic.SwitcherVisual",
    nodeCreated(node) {
        if (node.comfyClass !== "Logic_Switcher") return;

        const selectWidget = node.widgets?.find(w => w.name === "select");
        if (!selectWidget) return;

        const optionalShape = node.inputs[0]?.shape;

        function getOptInputs() {
            return node.inputs.filter(inp => inp.name.startsWith("any"));
        }

        function getSourceType(optIndex) {
            const opts = getOptInputs();
            const inp = opts[optIndex];
            if (!inp || inp.link == null) return null;
            const link = app.graph.links[inp.link];
            if (!link) return null;
            const srcNode = app.graph.getNodeById(link.origin_id);
            if (!srcNode) return null;
            const srcOut = srcNode.outputs?.[link.origin_slot];
            if (!srcOut) return null;
            const t = srcOut.type;
            if (t && t !== "*") return t;
            const info = srcNode.constructor?.nodeData;
            if (info?.output?.[link.origin_slot]) return info.output[link.origin_slot];
            return t;
        }

        function resetOutputType() {
            const out = node.outputs?.[0];
            if (!out) return;
            out.type = "*";
            const selIdx = selectWidget.value - 1;
            const srcType = getSourceType(selIdx);
            out.label = (srcType && srcType !== "*") ? tr("Logic.Switcher.outputWithType").replace("{type}", trTypeName(srcType)) : tr("Logic.Switcher.output");
        }

        function adjustInputs() {
            const opts = getOptInputs();
            let lastConnected = -1;
            for (let i = 0; i < opts.length; i++) {
                if (opts[i].link != null) lastConnected = i;
            }

            const target = Math.min(Math.max(MIN_INPUTS, lastConnected + 2), MAX_INPUTS);

            while (getOptInputs().length > target) {
                const cur = getOptInputs();
                const last = cur[cur.length - 1];
                if (last.link != null) break;
                node.removeInput(node.inputs.indexOf(last));
            }

            while (getOptInputs().length < target) {
                const idx = getOptInputs().length + 1;
                node.addInput(`any${idx}`, "*");
                if (optionalShape != null) {
                    node.inputs[node.inputs.length - 1].shape = optionalShape;
                }
            }

            const optCount = getOptInputs().length;
            selectWidget.options.max = optCount;
            if (selectWidget.value > optCount) {
                selectWidget.value = optCount;
            }

            updateLabels();
        }

        function updateLabels() {
            const idx = selectWidget.value;
            node.title = tr("Logic.Switcher.title").replace("{idx}", idx);
            node.inputs.forEach((inp) => {
                if (!inp.name.startsWith("any")) return;
                const num = parseInt(inp.name.replace("any", ""));
                const fmt = (num === idx) ? tr("Logic.Switcher.anyLabelSelected") : tr("Logic.Switcher.anyLabel");
                inp.label = fmt.replace("{idx}", num);
            });
            resetOutputType();
            node.setSize(node.computeSize());
            node.setDirtyCanvas(true, true);
        }

        while (getOptInputs().length > MIN_INPUTS) {
            const cur = getOptInputs();
            const last = cur[cur.length - 1];
            node.removeInput(node.inputs.indexOf(last));
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

        const origCb = selectWidget.callback;
        selectWidget.callback = function (v) { updateLabels(); origCb?.call(this, v); };

        updateLabels();
    },
});
