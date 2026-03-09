import { app } from "../../scripts/app.js";

const TYPE_COLORS = {
    IMAGE: "#6af", MASK: "#fff", LATENT: "#d8f",
    STRING: "#8f8", INT: "#fda", FLOAT: "#fda",
    BOOLEAN: "#f88", DICT: "#cc8", LIST: "#cc8",
    NONE: "#888",
};

function typeColor(t) {
    return TYPE_COLORS[t] || TYPE_COLORS[Object.keys(TYPE_COLORS).find(k => t?.startsWith(k))] || "#ccc";
}

function truncate(s, max = 20) {
    return s.length > max ? s.slice(0, max) + "…" : s;
}

app.registerExtension({
    name: "Logic.ConverterVisual",
    nodeCreated(node) {
        if (node.comfyClass !== "Logic_Converter") return;

        let data = null;

        node.addCustomWidget({
            type: "custom", name: "转换结果", serialize: false,
            computeSize: () => [node.size[0], data ? 90 : 0],
            draw(ctx, _node, width, y) {
                if (!data) return;
                ctx.save();

                ctx.textAlign = "center";
                ctx.font = "bold 13px Arial";
                ctx.fillStyle = typeColor(data.type);
                ctx.fillText(`源类型: ${data.type}`, width / 2, y + 14);

                ctx.strokeStyle = "#555";
                ctx.beginPath();
                ctx.moveTo(10, y + 20);
                ctx.lineTo(width - 10, y + 20);
                ctx.stroke();

                const x0 = 10, x1 = width - 10;
                const lines = [
                    { icon: "📝", label: "STR",   value: truncate(data.str, 24), color: "#8f8" },
                    { icon: "🔢", label: "INT",   value: data.int,               color: "#fda" },
                    { icon: "🔢", label: "FLOAT", value: data.float,             color: "#fda" },
                    { icon: "⚡", label: "BOOL",  value: data.bool,              color: data.bool === "True" ? "#8f8" : "#f88" },
                ];
                let cy = y + 36;
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

        const orig = node.onExecuted;
        node.onExecuted = function (o) {
            orig?.call(this, o);
            if (o?.str_val) {
                data = {
                    type:  o.original_type?.[0] || "?",
                    str:   o.str_val?.[0]   ?? "",
                    int:   o.int_val?.[0]   ?? "0",
                    float: o.float_val?.[0] ?? "0.0",
                    bool:  o.bool_val?.[0]  ?? "False",
                };
            }
            node.setSize(node.computeSize());
            node.setDirtyCanvas(true, true);
        };
    },
});
