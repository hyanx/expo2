#!/bin/bash

url="https://chikoroko.art/zh"
output_file="response.txt"

# 发送GET请求并将响应保存到文件
curl -o "$output_file" "$url"

echo "请求已发送，响应已保存到 $output_file"   
