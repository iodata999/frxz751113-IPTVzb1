<?php
// 设置响应头为 JSON 格式
header('Content-Type: application/json');

// 模拟数据
$data = [
    'message' => 'https://mengxianshengaaa.com/json.json',
    'timestamp' => time(),
    'status' => 'success'
];

// 将数据编码为 JSON 并输出
echo json_encode($data);
?>
