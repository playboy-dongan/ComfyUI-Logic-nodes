/**
 * ComfyUI-Logic 中英文翻译词典
 * 单一数据源，便于维护。新增文案时在 EN 和 ZH 中同时添加。
 *
 * Key 命名规范：
 *   Logic_NodeName     - 节点显示名（用于 node.title）
 *   Logic.NodeName.key - 节点内文案
 *   Logic.type.NAME    - 类型名（IMAGE、MASK 等）
 *   Logic.detail.key   - 详情标签（batch、size 等）
 *   Logic.common.key  - 通用文案
 *   Literal.True/False - 布尔字面量
 */

export const EN = {
    // === 节点显示名 ===
    "Logic_Blocker": "🚧 Blocker",
    "Logic_Switch": "🔀 Switch",
    "Logic_Judge": "⚖️ Judge",
    "Logic_PreviewType": "👁️ Preview Type",
    "Logic_UniversalPreview": "🖥️ Universal Preview",
    "Logic_BatchCombiner": "📦 Batch Combiner",
    "Logic_Looper": "⚙️ Batch Processor",
    "Logic_Random": "🎲 Random Tool",
    "Logic_Switcher": "🎚️ Switcher",
    "Logic_Converter": "🔄 Type Converter",
    "Logic_Math": "🧮 Math Expression",
    "Logic_VideoDecompose": "✂️ Decompose Video",
    "Logic_VideoCompose": "🎞️ Compose Video",

    // === Blocker ===
    "Logic.Blocker.Pass": "Pass",
    "Logic.Blocker.Blocked": "Block",

    // === Switch ===
    "Logic.Switch.True": "True",
    "Logic.Switch.False": "False",

    // === Judge (condition options) ===
    "Logic.Judge.True": "True",
    "Logic.Judge.False": "False",
    "Logic.Judge.ResultLabel": "Result",
    "Logic.Judge.A == B": "A == B",
    "Logic.Judge.A != B": "A != B",
    "Logic.Judge.A > B": "A > B",
    "Logic.Judge.A < B": "A < B",
    "Logic.Judge.A >= B": "A >= B",
    "Logic.Judge.A <= B": "A <= B",
    "Logic.Judge.A contains B": "A contains B",
    "Logic.Judge.A is empty": "A is empty",
    "Logic.Judge.A is not empty": "A is not empty",
    "Logic.Judge.A is true": "A is true",
    "Logic.Judge.A is false": "A is false",
    "Logic.Judge.length == B": "length == B",
    "Logic.Judge.length > B": "length > B",
    "Logic.Judge.length < B": "length < B",

    // === Random (mode options) ===
    "Logic.Random.random_int": "Random Integer",
    "Logic.Random.random_float": "Random Float",
    "Logic.Random.random_seed": "Random Seed",
    "Logic.Random.random_bool": "Random Boolean",

    // === BatchCombiner ===
    "Logic.BatchCombiner.title": "📦 Batch Combiner",
    "Logic.BatchCombiner.titleWithInputs": "📦 Batch Combiner ({n} inputs)",
    "Logic.BatchCombiner.titleWithResult": "📦 Batch Combiner → {type} {detail}",

    "Logic.Random.title": "🎲 Random Tool → {value}",

    // === Switcher ===
    "Logic.Switcher.title": "🎚️ Switcher → any{idx}",
    "Logic.Switcher.output": "Output",
    "Logic.Switcher.outputWithType": "Output ({type})",
    "Logic.Switcher.anyLabel": "any{idx}",
    "Logic.Switcher.anyLabelSelected": "▶ any{idx}",

    // === Converter ===
    "Logic.Converter.resultLabel": "Result",
    "Logic.Converter.Source": "Source",
    "Logic.Converter.STR": "STR",
    "Logic.Converter.INT": "INT",
    "Logic.Converter.FLOAT": "FLOAT",
    "Logic.Converter.BOOL": "BOOL",

    // === Preview ===
    "Logic.Preview.textLabel": "Preview Text",
    "Logic.Preview.audioLabel": "Preview Audio",

    // === PreviewType ===
    "Logic.PreviewType.typeLabel": "Type Display",

    // === Math ===
    "Logic.Math.resultLabel": "Result",
    "Logic.Math.expressionError": "Expression error",
    "Logic.Math.FLOAT": "FLOAT",
    "Logic.Math.INT": "INT",
    "Logic.Math.BOOL": "BOOL",

    // === Video ===
    "Logic.VideoDecompose.infoLabel": "Video Info",
    "Logic.VideoCompose.infoLabel": "Compose Info",

    // === Looper ===
    "Logic.Looper.Waiting": "Waiting...",
    "Logic.Looper.Processing": "Processing...",
    "Logic.Looper.Done": "Done ✓",
    "Logic.Looper.Progress": "Progress",

    // === 通用 ===
    "Logic.common.Resolution": "Resolution",
    "Logic.common.Duration": "Duration",
    "Logic.common.FPS": "FPS",
    "Logic.common.Frames": "Frames",
    "Logic.common.Audio": "Audio",
    "Logic.common.Yes": "Yes",
    "Logic.common.No": "No",

    // === 类型名（PreviewType、BatchCombiner 等）===
    "Logic.type.IMAGE": "IMAGE",
    "Logic.type.MASK": "MASK",
    "Logic.type.LATENT": "LATENT",
    "Logic.type.STRING": "STRING",
    "Logic.type.INT": "INT",
    "Logic.type.FLOAT": "FLOAT",
    "Logic.type.BOOLEAN": "BOOLEAN",
    "Logic.type.DICT": "DICT",
    "Logic.type.LIST": "LIST",
    "Logic.type.NONE": "NONE",
    "Logic.type.CONDITIONING": "CONDITIONING",
    "Logic.type.AUDIO": "AUDIO",
    "Logic.type.TENSOR": "TENSOR",
    "Logic.type.IMAGE_LIST": "IMAGE_LIST",
    "Logic.type.MASK_LIST": "MASK_LIST",
    "Logic.type.INT_LIST": "INT_LIST",
    "Logic.type.FLOAT_LIST": "FLOAT_LIST",
    "Logic.type.BOOLEAN_LIST": "BOOLEAN_LIST",
    "Logic.type.STRING_LIST": "STRING_LIST",
    "Logic.type.TENSOR_LIST": "TENSOR_LIST",
    "Logic.type.DICT_LIST": "DICT_LIST",
    "Logic.type.NESTED_LIST": "NESTED_LIST",
    "Logic.type.TENSOR_1D": "TENSOR_1D",
    "Logic.type.TENSOR_2D": "TENSOR_2D",

    // === 详情标签（Python 返回的 detail 字符串中的英文词）===
    "Logic.detail.noInput": "no input",
    "Logic.detail.batch": "batch",
    "Logic.detail.size": "size",
    "Logic.detail.ch": "ch",
    "Logic.detail.count": "count",
    "Logic.detail.empty": "empty",
    "Logic.detail.keys": "keys",
    "Logic.detail.value": "value",
    "Logic.detail.length": "length",
    "Logic.detail.shape": "shape",

    // === 布尔字面量（Python 返回 "True"/"False"）===
    "Literal.True": "True",
    "Literal.False": "False",
};

export const ZH = {
    // === 节点显示名 ===
    "Logic_Blocker": "🚧 阻断器",
    "Logic_Switch": "🔀 条件切换",
    "Logic_Judge": "⚖️ 判断器",
    "Logic_PreviewType": "👁️ 预览任意类型",
    "Logic_UniversalPreview": "🖥️ 通用预览",
    "Logic_BatchCombiner": "📦 组合任意批次",
    "Logic_Looper": "⚙️ 批处理器",
    "Logic_Random": "🎲 随机工具",
    "Logic_Switcher": "🎚️ 切换器",
    "Logic_Converter": "🔄 类型转换",
    "Logic_Math": "🧮 数学表达式",
    "Logic_VideoDecompose": "✂️ 分解视频",
    "Logic_VideoCompose": "🎞️ 合成视频",

    // === Blocker ===
    "Logic.Blocker.Pass": "通过",
    "Logic.Blocker.Blocked": "阻断",

    // === Switch ===
    "Logic.Switch.True": "真",
    "Logic.Switch.False": "假",

    // === Judge（条件下拉选项）===
    "Logic.Judge.True": "真",
    "Logic.Judge.False": "假",
    "Logic.Judge.ResultLabel": "判断结果",
    "Logic.Judge.A == B": "A == B",
    "Logic.Judge.A != B": "A != B",
    "Logic.Judge.A > B": "A > B",
    "Logic.Judge.A < B": "A < B",
    "Logic.Judge.A >= B": "A >= B",
    "Logic.Judge.A <= B": "A <= B",
    "Logic.Judge.A contains B": "A 包含 B",
    "Logic.Judge.A is empty": "A 为空",
    "Logic.Judge.A is not empty": "A 不为空",
    "Logic.Judge.A is true": "A 为真",
    "Logic.Judge.A is false": "A 为假",
    "Logic.Judge.length == B": "长度 == B",
    "Logic.Judge.length > B": "长度 > B",
    "Logic.Judge.length < B": "长度 < B",

    // === Random（模式下拉选项）===
    "Logic.Random.random_int": "随机整数",
    "Logic.Random.random_float": "随机浮点数",
    "Logic.Random.random_seed": "随机种子",
    "Logic.Random.random_bool": "随机布尔",

    // === BatchCombiner ===
    "Logic.BatchCombiner.title": "📦 组合任意批次",
    "Logic.BatchCombiner.titleWithInputs": "📦 组合任意批次 ({n} 输入)",
    "Logic.BatchCombiner.titleWithResult": "📦 组合任意批次 → {type} {detail}",

    // === Random ===
    "Logic.Random.title": "🎲 随机工具 → {value}",

    // === Switcher ===
    "Logic.Switcher.title": "🎚️ 切换器 → 任意{idx}",
    "Logic.Switcher.output": "输出",
    "Logic.Switcher.outputWithType": "输出 ({type})",
    "Logic.Switcher.anyLabel": "任意{idx}",
    "Logic.Switcher.anyLabelSelected": "▶ 任意{idx}",

    // === Converter ===
    "Logic.Converter.resultLabel": "转换结果",
    "Logic.Converter.Source": "来源",
    "Logic.Converter.STR": "字符串",
    "Logic.Converter.INT": "整数",
    "Logic.Converter.FLOAT": "浮点",
    "Logic.Converter.BOOL": "布尔",

    // === Preview ===
    "Logic.Preview.textLabel": "预览文本",
    "Logic.Preview.audioLabel": "预览音频",

    // === PreviewType ===
    "Logic.PreviewType.typeLabel": "类型显示",

    // === Math ===
    "Logic.Math.resultLabel": "计算结果",
    "Logic.Math.expressionError": "表达式错误",
    "Logic.Math.FLOAT": "浮点",
    "Logic.Math.INT": "整数",
    "Logic.Math.BOOL": "布尔",

    // === Video ===
    "Logic.VideoDecompose.infoLabel": "视频信息",
    "Logic.VideoCompose.infoLabel": "合成信息",

    // === Looper ===
    "Logic.Looper.Waiting": "等待中...",
    "Logic.Looper.Processing": "处理中...",
    "Logic.Looper.Done": "完成 ✓",
    "Logic.Looper.Progress": "循环进度",

    // === 通用 ===
    "Logic.common.Resolution": "分辨率",
    "Logic.common.Duration": "时长",
    "Logic.common.FPS": "帧率",
    "Logic.common.Frames": "帧数",
    "Logic.common.Audio": "音频",
    "Logic.common.Yes": "是",
    "Logic.common.No": "否",

    // === 类型名 ===
    "Logic.type.IMAGE": "图像",
    "Logic.type.MASK": "遮罩",
    "Logic.type.LATENT": "潜空间",
    "Logic.type.STRING": "字符串",
    "Logic.type.INT": "整数",
    "Logic.type.FLOAT": "浮点数",
    "Logic.type.BOOLEAN": "布尔",
    "Logic.type.DICT": "字典",
    "Logic.type.LIST": "列表",
    "Logic.type.NONE": "空",
    "Logic.type.CONDITIONING": "条件",
    "Logic.type.AUDIO": "音频",
    "Logic.type.TENSOR": "张量",
    "Logic.type.IMAGE_LIST": "图像列表",
    "Logic.type.MASK_LIST": "遮罩列表",
    "Logic.type.INT_LIST": "整数列表",
    "Logic.type.FLOAT_LIST": "浮点数列表",
    "Logic.type.BOOLEAN_LIST": "布尔列表",
    "Logic.type.STRING_LIST": "字符串列表",
    "Logic.type.TENSOR_LIST": "张量列表",
    "Logic.type.DICT_LIST": "字典列表",
    "Logic.type.NESTED_LIST": "嵌套列表",
    "Logic.type.TENSOR_1D": "一维张量",
    "Logic.type.TENSOR_2D": "二维张量",

    // === 详情标签 ===
    "Logic.detail.noInput": "无输入",
    "Logic.detail.batch": "批次",
    "Logic.detail.size": "尺寸",
    "Logic.detail.ch": "通道",
    "Logic.detail.count": "数量",
    "Logic.detail.empty": "空",
    "Logic.detail.keys": "键",
    "Logic.detail.value": "值",
    "Logic.detail.length": "长度",
    "Logic.detail.shape": "形状",

    // === 布尔字面量 ===
    "Literal.True": "真",
    "Literal.False": "假",
};
