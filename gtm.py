import sys
import os
import time
from tqdm import tqdm
from PIL import Image, ImageSequence
import subprocess

def convert_gif_to_mp4(input_path, output_dir):
    if os.path.isfile(input_path):
        files = [input_path]
    elif os.path.isdir(input_path):
        files = [os.path.join(input_path, f) for f in os.listdir(input_path) if f.endswith('.gif')]
    else:
        print(f"错误: {input_path} 不是一个有效的文件或目录")
        return

    for gif_file in tqdm(files, desc="处理GIF文件", unit="file"):
        try:
            # 创建输出目录如果它不存在
            os.makedirs(output_dir, exist_ok=True)
            
            # 读取 GIF 文件
            gif = Image.open(gif_file)
            frames = []

            for frame in ImageSequence.Iterator(gif):
                frames.append(frame.convert('RGB'))

            # 准备临时帧输出目录
            temp_dir = os.path.join(output_dir, 'temp_frames')
            os.makedirs(temp_dir, exist_ok=True)

            # 保存帧为 PNG 文件
            for i, frame in enumerate(frames):
                frame.save(os.path.join(temp_dir, f'frame_{i}.png'))

            # 调整视频大小
            subprocess.run([
                'ffmpeg.exe',
                '-framerate', '10',
                '-i', os.path.join(temp_dir, 'frame_%d.png'),
                '-vf', 'scale=1980:-1',  # 调整宽度为1980，高度自动调整
                '-c:v', 'libx264',
                '-pix_fmt', 'yuv420p',
                os.path.join(temp_dir, 'adjusted_video.mp4')
            ], check=True)

            # 使用调整后的视频转换为最终的 MP4
            output_mp4 = os.path.join(output_dir, os.path.splitext(os.path.basename(gif_file))[0] + '.mp4')
            subprocess.run([
                'ffmpeg.exe', 
                '-i', os.path.join(temp_dir, 'adjusted_video.mp4'),
                '-c:v', 'libx264',
                '-pix_fmt', 'yuv420p',
                output_mp4
            ], check=True)

            # 删除临时帧文件和调整后的视频文件
            for file in os.listdir(temp_dir):
                os.remove(os.path.join(temp_dir, file))
            os.rmdir(temp_dir)

        except subprocess.CalledProcessError as e:
            print(f"\n错误: 子进程执行失败，命令: {e.cmd}, 返回状态码 {e.returncode}")
            print(f"子进程标准输出: {e.stdout}")
            print(f"子进程标准错误: {e.stderr}")
        except Exception as e:
            print(f"\n错误: 处理文件 {gif_file} 时发生错误: {str(e)}")

def main():
    if len(sys.argv) != 3:
        print("""用法: gtm "input_path" "output_dir"
        参数:
          input_path:  需要转换的 GIF 文件或包含 GIF 文件的目录。
          output_dir:  输出的 MP4 文件保存目录。
        
        示例:
          gtm "path/to/gifs" "path/to/output"
          gtm "path/to/single.gif" "path/to/output"
        """)
        sys.exit(1)

    input_path = sys.argv[1]
    output_dir = sys.argv[2]

    convert_gif_to_mp4(input_path, output_dir)

if __name__ == "__main__":
    main()
