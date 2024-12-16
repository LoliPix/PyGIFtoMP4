# GIF to MP4 Converter

这个项目提供了一个简单的命令行工具，用于将 GIF 文件批量转换为 MP4 视频文件。

### 使用前准备

1. **确保 `ffmpeg` 已安装**：请根据您的操作系统安装 `ffmpeg`。对于 Windows 用户，建议将 `ffmpeg.exe` 放置在脚本所在的目录中。

2. **Python 环境**：确保您的系统中已安装 Python 3.6 或更高版本，并已安装了所有必要的依赖项。

## 使用

### 命令行用法

```sh
python gtm.py "input_path" "output_dir"
```

或如果您已将脚本打包成 `.exe` 文件：

```sh
gtm "input_path" "output_dir"
```

- **input_path**: 需要转换的 GIF 文件或包含 GIF 文件的目录。
- **output_dir**: 输出的 MP4 文件保存目录。

### 示例

- 转换单个 GIF 文件：
  ```sh
  gtm "path/to/your/file.gif" "path/to/output/directory"
  ```

- 转换目录中的所有 GIF 文件：
  ```sh
  gtm "path/to/directory/with/gifs" "path/to/output/directory"
  ```
