import { app } from "../../scripts/app.js";
import { tr, trNode, trBool } from "./tr.js";

const MIN_INPUTS = 2;
const MAX_INPUTS = 10;
const VAR_NAMES = Array.from({ length: MAX_INPUTS }, (_, i) => String.fromCharCode(65 + i));

app.registerExtension({
    name: "Logic.MathVisual",
    nodeCreated(node) {
        if (node.comfyClass !== "Logic_Math") return;

        const optionalShape = node.inputs.find(inp => VAR_NAMES.includes(inp.name))?.shape;

        let data = null;

        function getVarInputs() {
            return node.inputs.filter(inp => VAR_NAMES.includes(inp.name));
        }

        function adjustInputs() {
            const opts = getVarInputs();
            let lastConnected = -1;
            for (let i = 0; i < opts.length; i++) {
                if (opts[i].link != null) lastConnected = i;
            }

            const target = Math.min(Math.max(MIN_INPUTS, lastConnected + 2), MAX_INPUTS);

            while (getVarInputs().length > target) {
                const cur = getVarInputs();
                const last = cur[cur.length - 1];
                if (last.link != null) break;
                node.removeInput(node.inputs.indexOf(last));
            }

            while (getVarInputs().length < target) {
                const idx = getVarInputs().length;
                const name = VAR_NAMES[idx];
                node.addInput(name, "*");
                if (optionalShape != null) {
                    node.inputs[node.inputs.length - 1].shape = optionalShape;
                }
            }

            node.setSize(node.computeSize());
            node.setDirtyCanvas(true, true);
        }

        while (getVarInputs().length > MIN_INPUTS) {
            const cur = getVarInputs();
            const last = cur[cur.length - 1];
            node.removeInput(node.inputs.indexOf(last));
        }

        node.addCustomWidget({
            type: "custom", name: tr("Logic.Math.resultLabel", "Result"), serialize: false,
            computeSize: () => [node.size[0], data ? (data.error ? 30 : 60) : 0],
            draw(ctx, _node, width, y) {
                if (!data) return;
                ctx.save();

                if (data.error) {
                    ctx.textAlign = "center";
                    ctx.font = "bold 12px Arial";
                    ctx.fillStyle = "#f66";
                    const msg = "⚠ " + data.error;
                    const maxW = width - 20;
                    ctx.fillText(
                        ctx.measureText(msg).width > maxW ? "⚠ " + tr("Logic.Math.expressionError") : msg,
                        width / 2, y + 18
                    );
                    ctx.restore();
                    return;
                }

                ctx.strokeStyle = "#555";
                ctx.beginPath();
                ctx.moveTo(10, y + 4);
                ctx.lineTo(width - 10, y + 4);
                ctx.stroke();

                const x0 = 10, x1 = width - 10;
                const lines = [
                    { icon: "🔢", label: tr("Logic.Math.FLOAT"), value: data.float, color: "#fda" },
                    { icon: "🔢", label: tr("Logic.Math.INT"),   value: data.int,   color: "#fda" },
                    { icon: "⚡", label: tr("Logic.Math.BOOL"),  value: trBool(data.bool),  color: data.bool === "True" ? "#8f8" : "#f88" },
                ];
                let cy = y + 20;
                for (const l of lines) {
                    ctx.font = "12px Arial";
                    ctx.textAlign = "left";
                    ctx.fillStyle = l.color;
                    ctx.fillText(`${l.icon} ${l.label}`, x0, cy);
                    ctx.textAlign = "right";
                    ctx.fillStyle = "#ddd";
                    ctx.fillText(l.value, x1, cy);
                    cy += 16;
                }
                ctx.restore();
            },
        });

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
        node.onExecuted = function (o) {
            origExec?.call(this, o);
            data = {
                float: o?.float_val?.[0]  ?? "0.0",
                int:   o?.int_val?.[0]    ?? "0",
                bool:  o?.bool_val?.[0]   ?? "False",
                error: o?.error?.[0]      ?? "",
            };
            const baseTitle = trNode("Logic_Math");
            node.title = data.error ? "⚠ " + baseTitle : `🧮 = ${data.float}`;
            node.setSize(node.computeSize());
            node.setDirtyCanvas(true, true);
        };

        adjustInputs();
    },
});
