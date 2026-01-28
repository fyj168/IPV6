# 山西组播源自动更新

本项目自动从指定网站获取山西组播源，每12小时更新一次。

## 文件说明

- `shanxi-multicast.m3u` - 最新山西组播源文件
- `.github/workflows/` - GitHub Actions工作流配置
- `scripts/update_shanxi_sources.py` - 更新脚本

## 使用说明

1. 最新组播源会自动更新在 `shanxi-multicast.m3u` 文件中
2. 更新每12小时自动运行一次
3. 也可以手动触发更新

## 手动更新

在GitHub仓库的Actions标签页中，可以手动运行工作流。

## 注意事项

- 源文件来自第三方网站，请遵守相关法律法规
- 频道可用性可能随时间变化
- 建议定期检查更新
