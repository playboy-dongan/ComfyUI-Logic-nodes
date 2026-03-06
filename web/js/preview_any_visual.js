import { app } from "../../scripts/app.js";

const ICONS = {
    IMAGE: "🖼️", IMAGE_LIST: "🖼️", MASK: "🎭", MASK_LIST: "🎭",
    LATENT: "🔲", STRING: "📝", STRING_LIST: "📝",
    INT: "🔢", INT_LIST: "🔢", FLOAT: "🔢", FLOAT_LIST: "🔢",
    BOOLEAN: "⚡", BOOLEAN_LIST: "⚡", CONDITIONING: "🎯",
    DICT: "📦", DICT_LIST: "📦", TENSOR_1D: "📊", TENSOR_2D: "📊",
    TENSOR_LIST: "📊", NESTED_LIST: "📂", LIST: "📋", NONE: "⭕",
};

const COLORS = {
    IMAGE: "#6af", IMAGE_LIST: "#6af", MASK: "#fff", MASK_LIST: "#fff",
    LATENT: "#d8f", STRING: "#8f8", STRING_LIST: "#8f8",
    INT: "#fda", INT_LIST: "#fda", FLOAT: "#fda", FLOAT_LIST: "#fda",
    BOOLEAN: "#f88", BOOLEAN_LIST: "#f88", CONDITIONING: "#fa6",
    DICT: "#cc8", DICT_LIST: "#cc8", NONE: "#888",
};

app.registerExtension({
    name: "Logic.PreviewTypeVisual",
    nodeCreated(node) {
        if (node.comfyClass !== "Logic_PreviewType") return;
        let typeName = "", detail = "";

        node.addCustomWidget({
            type: "custom", name: "类型显示", serialize: false,
            computeSize: () => [node.size[0], detail ? 46 : 30],
            draw(ctx, _node, width, y) {
                if (!typeName) return;
                ctx.save();
                ctx.textAlign = "center";
                ctx.font = "bold 15px Arial";
                ctx.fillStyle = COLORS[typeName] || "#ccc";
                ctx.fillText(`${ICONS[typeName] || "❓"}  ${typeName}`, width / 2, y + 18);
                if (detail) {
                    ctx.font = "12px Arial";
                    ctx.fillStyle = "#999";
                    ctx.fillText(detail, width / 2, y + 38);
                }
                ctx.restore();
            },
        });

        const orig = node.onExecuted;
        node.onExecuted = function (o) {
            orig?.call(this, o);
            typeName = o?.type_name?.[0] || "";
            detail = o?.detail?.[0] || "";
            node.setSize(node.computeSize());
            node.setDirtyCanvas(true, true);
        };
    },
});
